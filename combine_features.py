# combine_features.py
import pandas as pd

print("🔗 Combining all features...\n")

# Load all feature sets
features_311 = pd.read_csv("data/processed/features_311.csv")
features_images = pd.read_csv("data/processed/features_images.csv")
labels = pd.read_csv("data/processed/labels.csv")

print("✓ Loaded 311 features")
print("✓ Loaded image features")
print("✓ Loaded labels")

# Merge everything
combined = features_311.merge(features_images, on='name')
combined = combined.merge(labels, on='name')

print(f"\n📊 Combined dataset shape: {combined.shape}")
print(f"   {combined.shape[0]} neighborhoods")
print(f"   {combined.shape[1]} total columns")

print("\n📋 Features:")
print(combined.columns.tolist())

print("\n🎯 First few rows:")
print(combined.head())

# Save
combined.to_csv("data/processed/combined_features.csv", index=False)
print("\n✅ Saved to data/processed/combined_features.csv")
print("\n🎉 Feature engineering complete!")
print("🚀 Ready for Day 3: Train ML Model!")
