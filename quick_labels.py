# quick_labels.py - Auto-generate labels from data
import pandas as pd
import numpy as np
from config import NEIGHBORHOODS

print("🤖 AUTO-GENERATING LABELS FROM DATA...\n")

# Load features
features_311 = pd.read_csv("data/processed/features_311.csv")
features_images = pd.read_csv("data/processed/features_images.csv")

# Merge
data = features_311.merge(features_images, on='name')

labels = []

for _, row in data.iterrows():
    # SAFETY: Fewer complaints = safer
    max_complaints = data['total_complaints'].max()
    complaint_ratio = row['total_complaints'] / max_complaints if max_complaints > 0 else 0
    safety = 5 - int(complaint_ratio * 4)
    safety = max(1, min(5, safety))
    
    # LIVELINESS: More noise = more lively (but cap it)
    max_noise = data['noise_complaints'].max()
    noise_ratio = row['noise_complaints'] / max_noise if max_noise > 0 else 0
    liveliness = 2 + int(noise_ratio * 3)
    liveliness = max(2, min(5, liveliness))
    
    # CLEANLINESS: Less graffiti/street issues = cleaner
    max_graffiti = data['graffiti'].max()
    max_street = data['street_condition'].max()
    
    graffiti_ratio = row['graffiti'] / max_graffiti if max_graffiti > 0 else 0
    street_ratio = row['street_condition'] / max_street if max_street > 0 else 0
    
    cleanliness = 5 - int((graffiti_ratio + street_ratio) * 2)
    cleanliness = max(1, min(5, cleanliness))
    
    # Calculate overall
    overall = (safety + liveliness + cleanliness) / 3
    
    # Categorize
    if overall >= 3.5:
        category = 'positive'
    elif overall >= 2.5:
        category = 'neutral'
    else:
        category = 'negative'
    
    emoji = "😊" if category == 'positive' else "😐" if category == 'neutral' else "😟"
    
    print(f"{emoji} {row['name']:25s} → S:{safety} L:{liveliness} C:{cleanliness} = {category}")
    
    labels.append({
        'name': row['name'],
        'safety': safety,
        'liveliness': liveliness,
        'cleanliness': cleanliness,
        'overall_score': overall,
        'category': category
    })

df = pd.DataFrame(labels)
df.to_csv("data/processed/labels.csv", index=False)

print(f"\n✅ Auto-generated labels for {len(df)} neighborhoods!")
print(f"📁 Saved to: data/processed/labels.csv")

# Show distribution
print(f"\n📊 Category Distribution:")
print(df['category'].value_counts())
