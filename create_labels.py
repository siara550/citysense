# create_labels.py
import pandas as pd
from config import NEIGHBORHOODS

print("=" * 60)
print("🏷️  NEIGHBORHOOD LABELING")
print("=" * 60)
print("\nRate each neighborhood on a scale of 1-5 for:")
print("  • Safety (1=unsafe, 5=very safe)")
print("  • Liveliness (1=dead, 5=very lively)")
print("  • Cleanliness (1=dirty, 5=very clean)")
print("\nTip: Google the neighborhood if you're not sure!\n")
print("=" * 60)

labels = []

for hood in NEIGHBORHOODS:
    print(f"\n📍 {hood['name']}")
    print(f"   Location: {hood['lat']}, {hood['lon']}")
    
    safety = int(input("   Safety (1-5): "))
    liveliness = int(input("   Liveliness (1-5): "))
    cleanliness = int(input("   Cleanliness (1-5): "))
    
    overall = (safety + liveliness + cleanliness) / 3
    
    # Categorize
    if overall >= 3.5:
        category = 'positive'
    elif overall >= 2.5:
        category = 'neutral'
    else:
        category = 'negative'
    
    labels.append({
        'name': hood['name'],
        'safety': safety,
        'liveliness': liveliness,
        'cleanliness': cleanliness,
        'overall_score': overall,
        'category': category
    })

df = pd.DataFrame(labels)

print("\n" + "=" * 60)
print("📊 YOUR LABELS:")
print("=" * 60)
print(df)
print("\n📁 Saving to data/processed/labels.csv")

df.to_csv("data/processed/labels.csv", index=False)
print("✅ Done!")
