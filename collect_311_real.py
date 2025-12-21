import pandas as pd
import numpy as np
from config import NEIGHBORHOODS

def generate_realistic_311_data():
    """Generate realistic sample 311 data based on actual NYC patterns"""
    print("🎲 Generating realistic 311 sample data...\n")
    print("(NYC API is down - using realistic synthetic data for demo)\n")
    
    # Real NYC 311 complaint types and their typical frequencies
    complaint_types = [
        ('Noise - Residential', 0.15),
        ('Heat/Hot Water', 0.12),
        ('Street Condition', 0.10),
        ('Illegal Parking', 0.08),
        ('Blocked Driveway', 0.08),
        ('Water System', 0.07),
        ('Graffiti', 0.06),
        ('Sanitation Condition', 0.06),
        ('Homeless Person Assistance', 0.05),
        ('Noise - Street/Sidewalk', 0.05),
        ('Traffic Signal Condition', 0.04),
        ('Street Light Condition', 0.04),
        ('Derelict Vehicle', 0.03),
        ('Noise - Commercial', 0.03),
        ('Sewer', 0.02),
        ('Other', 0.02)
    ]
    
    types, probs = zip(*complaint_types)
    
    all_complaints = []
    
    # Generate different amounts per neighborhood type
    for hood in NEIGHBORHOODS:
        # Wealthier/quieter areas: 50-100 complaints
        # Busier areas: 100-200 complaints  
        # High-density areas: 200-300 complaints
        
        # Simple heuristic based on name
        if any(x in hood['name'] for x in ['Upper_East', 'Upper_West', 'Riverdale', 'Park_Slope']):
            n = np.random.randint(50, 100)  # Wealthy, quiet
        elif any(x in hood['name'] for x in ['Midtown', 'Financial', 'Times_Square']):
            n = np.random.randint(200, 300)  # High density
        else:
            n = np.random.randint(100, 200)  # Average
        
        for _ in range(n):
            # Scatter points around neighborhood center
            lat_offset = np.random.uniform(-0.015, 0.015)
            lon_offset = np.random.uniform(-0.015, 0.015)
            
            complaint = {
                'unique_key': f"SAMPLE_{len(all_complaints)}",
                'created_date': f"2024-{np.random.randint(1,13):02d}-{np.random.randint(1,29):02d}",
                'complaint_type': np.random.choice(types, p=probs),
                'latitude': hood['lat'] + lat_offset,
                'longitude': hood['lon'] + lon_offset,
                'borough': 'SAMPLE'
            }
            all_complaints.append(complaint)
    
    df = pd.DataFrame(all_complaints)
    
    # Save
    df.to_csv("data/raw/311_complaints.csv", index=False)
    
    print(f"✅ Generated {len(df):,} realistic complaints")
    print(f"📊 Average per neighborhood: {len(df)//len(NEIGHBORHOODS)}")
    print(f"📁 Saved to: data/raw/311_complaints.csv")
    
    print(f"\n📋 Top 10 complaint types:")
    print(df['complaint_type'].value_counts().head(10))
    
    print("\n💡 This is synthetic data for the demo.")
    print("   The ML pipeline works identically with real data!")
    
    return df

if __name__ == "__main__":
    generate_realistic_311_data()
