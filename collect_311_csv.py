import pandas as pd
import requests

def download_311_csv():
    """Download 311 data as CSV directly"""
    print("📥 Downloading NYC 311 data as CSV...\n")
    print("This might take 2-3 minutes for a large file...\n")
    
    # Direct CSV export from NYC Open Data
    # This gets the most recent 100k records
    url = "https://data.cityofnewyork.us/resource/erm2-nwe9.csv?$limit=100000&$where=latitude IS NOT NULL"
    
    print("⏳ Downloading...")
    
    try:
        df = pd.read_csv(url)
        
        print(f"✅ Downloaded {len(df):,} records!")
        
        # Clean and filter
        df = df[['unique_key', 'created_date', 'complaint_type', 'latitude', 'longitude', 'borough']].copy()
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
        df = df.dropna(subset=['latitude', 'longitude'])
        
        # Save
        df.to_csv("data/raw/311_complaints.csv", index=False)
        
        print(f"✅ Saved {len(df):,} clean records")
        print(f"📁 Location: data/raw/311_complaints.csv")
        print(f"\n📊 Top 10 complaint types:")
        print(df['complaint_type'].value_counts().head(10))
        
        return df
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nThe API might be rate-limiting or down.")
        return None

if __name__ == "__main__":
    download_311_csv()
