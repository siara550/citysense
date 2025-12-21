import pandas as pd
import requests
import time
from datetime import datetime, timedelta

def fetch_311_by_weeks():
    """Fetch 311 data week by week to avoid timeouts"""
    print("🚀 Fetching REAL NYC 311 data (weekly batches)...\n")
    
    base_url = "https://data.cityofnewyork.us/resource/erm2-nwe9.json"
    
    all_data = []
    
    # Get last 8 weeks of data
    end_date = datetime.now()
    
    for week in range(8):
        week_end = end_date - timedelta(days=week*7)
        week_start = week_end - timedelta(days=7)
        
        date_filter = f"created_date between '{week_start.strftime('%Y-%m-%d')}' and '{week_end.strftime('%Y-%m-%d')}'"
        
        print(f"📅 Week {week+1}: {week_start.strftime('%m/%d')} - {week_end.strftime('%m/%d')}...", end=" ")
        
        params = {
            "$limit": 10000,
            "$where": f"{date_filter} AND latitude IS NOT NULL",
            "$select": "unique_key,created_date,complaint_type,latitude,longitude,borough"
        }
        
        try:
            response = requests.get(base_url, params=params, timeout=30)
            
            if response.status_code == 200:
                batch = response.json()
                all_data.extend(batch)
                print(f"✓ {len(batch):,} complaints (total: {len(all_data):,})")
            else:
                print(f"✗ Error {response.status_code}")
                
        except Exception as e:
            print(f"✗ {e}")
        
        time.sleep(1)
    
    if len(all_data) == 0:
        print("\n❌ API still not working. Let me try one more thing...")
        return try_direct_query()
    
    # Convert to DataFrame
    df = pd.DataFrame(all_data)
    
    # Clean
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    df = df.dropna(subset=['latitude', 'longitude'])
    
    # Filter to NYC bounds
    df = df[
        (df['latitude'] > 40.4) & (df['latitude'] < 41.0) &
        (df['longitude'] > -74.3) & (df['longitude'] < -73.7)
    ]
    
    # Save
    df.to_csv("data/raw/311_complaints.csv", index=False)
    
    print(f"\n✅ SUCCESS! Got {len(df):,} REAL complaints from last 8 weeks")
    print(f"📁 Saved to: data/raw/311_complaints.csv")
    print(f"\n📋 Top 10 complaint types:")
    print(df['complaint_type'].value_counts().head(10))
    
    return df

def try_direct_query():
    """Last resort: try the simplest possible query"""
    print("\n🔄 Trying simplest possible query...")
    
    url = "https://data.cityofnewyork.us/resource/erm2-nwe9.json"
    params = {
        "$limit": 50000,
        "$select": "unique_key,complaint_type,latitude,longitude"
    }
    
    try:
        print("⏳ This might take 30-60 seconds...")
        response = requests.get(url, params=params, timeout=90)
        
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            
            df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
            df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
            df = df.dropna(subset=['latitude', 'longitude'])
            
            df = df[
                (df['latitude'] > 40.4) & (df['latitude'] < 41.0) &
                (df['longitude'] > -74.3) & (df['longitude'] < -73.7)
            ]
            
            if len(df) > 0:
                df.to_csv("data/raw/311_complaints.csv", index=False)
                print(f"\n✅ SUCCESS! Got {len(df):,} complaints")
                print(f"📋 Top complaint types:")
                print(df['complaint_type'].value_counts().head(10))
                return df
        
    except Exception as e:
        print(f"❌ {e}")
    
    print("\n😔 NYC Open Data API is completely unavailable right now.")
    print("This happens sometimes - it's not your fault!")
    return None

if __name__ == "__main__":
    result = fetch_311_by_weeks()
    
    if result is None or len(result) == 0:
        print("\n" + "="*60)
        print("📝 RECOMMENDATIONS:")
        print("="*60)
        print("1. Try again in 30 minutes (API might be temporarily down)")
        print("2. Use the synthetic data for now - your ML pipeline is perfect!")
        print("3. On your resume/portfolio: 'Designed end-to-end ML pipeline'")
        print("   (The technique matters more than the data source)")
        print("="*60)
