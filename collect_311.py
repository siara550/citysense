import pandas as pd
import requests
import time

def fetch_real_311_data():
    """Fetch REAL NYC 311 data using a working endpoint"""
    print("🚀 Fetching REAL NYC 311 complaints...\n")
    
    # This is the more reliable endpoint
    base_url = "https://data.cityofnewyork.us/resource/erm2-nwe9.json"
    
    all_data = []
    
    # Fetch in chunks (API has limits)
    for offset in range(0, 50000, 10000):
        print(f"Fetching records {offset} to {offset+10000}...")
        
        params = {
            "$limit": 10000,
            "$offset": offset,
            "$order": "created_date DESC",
            "$select": "unique_key,created_date,complaint_type,latitude,longitude,borough",
            "$where": "latitude IS NOT NULL AND longitude IS NOT NULL"
        }
        
        try:
            response = requests.get(base_url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if len(data) == 0:
                    print("  No more data available")
                    break
                all_data.extend(data)
                print(f"  ✓ Got {len(data)} records")
            else:
                print(f"  ✗ Error {response.status_code}: {response.text[:100]}")
                break
                
        except Exception as e:
            print(f"  ✗ Error: {e}")
            break
        
        time.sleep(1)  # Be nice to the API
    
    if len(all_data) == 0:
        print("\n❌ No data retrieved. API might be down.")
        print("Would you like to:")
        print("  1. Use sample data for now")
        print("  2. Try downloading a CSV file instead")
        return None
    
    df = pd.DataFrame(all_data)
    
    # Clean data
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    df = df.dropna(subset=['latitude', 'longitude'])
    
    # Save
    df.to_csv("data/raw/311_complaints.csv", index=False)
    
    print(f"\n✅ SUCCESS! Collected {len(df):,} REAL complaints")
    print(f"📁 Saved to: data/raw/311_complaints.csv")
    
    if 'complaint_type' in df.columns:
        print(f"\n📊 Top 10 complaint types:")
        print(df['complaint_type'].value_counts().head(10))
    
    return df

if __name__ == "__main__":
    fetch_real_311_data()
