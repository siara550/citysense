import pandas as pd

print("🧹 Cleaning 311 data...\n")

print("📂 Loading file (this might take 1-2 minutes for large file)...")

try:
    # Use the NEW column names!
    df = pd.read_csv("data/raw/311_raw.csv", 
                     usecols=['Unique Key', 'Created Date', 
                              'Problem (formerly Complaint Type)', 
                              'Latitude', 'Longitude', 'Borough'],
                     low_memory=False)
    
    print(f"✓ Loaded {len(df):,} rows")
    
    # Rename columns to simple names
    df.columns = ['unique_key', 'created_date', 'complaint_type', 
                  'latitude', 'longitude', 'borough']
    
    # Clean coordinates
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    df = df.dropna(subset=['latitude', 'longitude'])
    
    # Filter to valid NYC coordinates
    df = df[
        (df['latitude'] > 40.4) & (df['latitude'] < 41.0) &
        (df['longitude'] > -74.3) & (df['longitude'] < -73.7)
    ]
    
    print(f"✓ Filtered to {len(df):,} valid NYC records")
    
    # Take most recent 50,000 (plenty for analysis)
    df['created_date'] = pd.to_datetime(df['created_date'], errors='coerce')
    df = df.sort_values('created_date', ascending=False).head(50000)
    
    # Save cleaned version
    df.to_csv("data/raw/311_complaints.csv", index=False)
    
    print(f"\n✅ SUCCESS! Cleaned data saved!")
    print(f"📊 Final dataset: {len(df):,} REAL complaints")
    print(f"📁 Location: data/raw/311_complaints.csv")
    
    print(f"\n📋 Top 10 complaint types:")
    print(df['complaint_type'].value_counts().head(10))
    
    print(f"\n📅 Date range:")
    print(f"   Most recent: {df['created_date'].max()}")
    print(f"   Oldest: {df['created_date'].min()}")
    
    print("\n🎉 Ready to extract features!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
