# extract_311_features.py
import pandas as pd
import numpy as np
from config import NEIGHBORHOODS

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate rough distance in km"""
    return np.sqrt((lat1-lat2)**2 + (lon1-lon2)**2) * 111

def extract_neighborhood_features(complaints_csv, neighborhoods):
    """Extract features for each neighborhood from 311 data"""
    df = pd.read_csv(complaints_csv)
    
    print(f"📊 Processing {len(df)} complaints...\n")
    
    features = []
    for hood in neighborhoods:
        print(f"Processing {hood['name']}...")
        
        # Get complaints within ~1km radius
        df['distance'] = calculate_distance(
            df['latitude'], df['longitude'], 
            hood['lat'], hood['lon']
        )
        nearby = df[df['distance'] < 1.0]
        
        # Count by type
        complaint_counts = nearby['complaint_type'].value_counts()
        
        features.append({
            'name': hood['name'],
            'lat': hood['lat'],
            'lon': hood['lon'],
            'total_complaints': len(nearby),
            'noise_complaints': complaint_counts.get('Noise', 0),
            'street_condition': complaint_counts.get('Street Condition', 0),
            'graffiti': complaint_counts.get('Graffiti', 0),
            'heat_hot_water': complaint_counts.get('Heat/Hot Water', 0),
            'complaints_per_km2': len(nearby) / 3.14,  # rough area calculation
        })
    
    df_features = pd.DataFrame(features)
    
    print(f"\n✅ Extracted 311 features!")
    print(f"📁 Saving to data/processed/features_311.csv\n")
    print(df_features)
    
    return df_features

if __name__ == "__main__":
    import os
    os.makedirs("data/processed", exist_ok=True)
    
    features = extract_neighborhood_features(
        "data/raw/311_complaints.csv", 
        NEIGHBORHOODS
    )
    features.to_csv("data/processed/features_311.csv", index=False)
    print("\n✅ Done!")
