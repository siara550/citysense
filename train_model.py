# train_model.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib

print("=" * 60)
print("🤖 CITYSENSE ML MODEL TRAINING")
print("=" * 60)

# Load data
data = pd.read_csv("data/processed/combined_features.csv")

print(f"\n📊 Dataset: {len(data)} neighborhoods")
print(f"📋 Features: {data.shape[1]} columns\n")

# Separate features and target
feature_cols = [
    'total_complaints', 'noise_complaints', 'street_condition', 
    'graffiti', 'heat_hot_water', 'complaints_per_km2',
    'avg_brightness', 'avg_green_ratio', 'avg_blue_ratio', 
    'avg_color_variance', 'avg_brightness_variance'
]

X = data[feature_cols]
y = data['category']

print("🎯 Target distribution:")
print(y.value_counts())
print()

# Normalize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train Random Forest (works better with small datasets)
print("🔬 Training Random Forest model...\n")

model = RandomForestClassifier(
    n_estimators=100, 
    max_depth=3, 
    random_state=42,
    min_samples_split=2
)

model.fit(X_scaled, y)

# Feature importance
importances = pd.DataFrame({
    'feature': feature_cols,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("⭐ Top 5 Most Important Features:")
for idx, row in importances.head(5).iterrows():
    bar = "█" * int(row['importance'] * 50)
    print(f"  {row['feature']:25s} {bar} {row['importance']:.3f}")

# Make predictions on training data
predictions = model.predict(X_scaled)
data['predicted_category'] = predictions

# Show results
print("\n📋 Predictions vs Reality:")
correct = 0
for idx, row in data.iterrows():
    actual = row['category']
    predicted = row['predicted_category']
    match = "✓" if actual == predicted else "✗"
    if actual == predicted:
        correct += 1
    print(f"  {match} {row['name']:20s} Actual: {actual:8s} → Predicted: {predicted:8s}")

# Calculate accuracy
accuracy = correct / len(data)
print(f"\n🎯 Training Accuracy: {accuracy:.1%} ({correct}/{len(data)} correct)")

# Show prediction confidence
print("\n🔮 Prediction Probabilities:")
probs = model.predict_proba(X_scaled)
class_names = model.classes_

for i, row in data.iterrows():
    print(f"\n  {row['name']}:")
    for j, class_name in enumerate(class_names):
        prob = probs[i][j]
        bar = "█" * int(prob * 30)
        print(f"    {class_name:8s} {bar} {prob:.1%}")

# Save everything
import os
os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/atmosphere_model.pkl")
joblib.dump(scaler, "models/scaler.pkl")
joblib.dump(feature_cols, "models/feature_columns.pkl")
data.to_csv("data/processed/predictions.csv", index=False)

print("\n💾 Saved:")
print("  • models/atmosphere_model.pkl")
print("  • models/scaler.pkl")
print("  • data/processed/predictions.csv")

print("\n" + "=" * 60)
print("🎉 MODEL TRAINING COMPLETE!")
print(f"📊 Final Stats:")
print(f"   • {len(feature_cols)} features used")
print(f"   • {len(data)} neighborhoods analyzed")
print(f"   • {accuracy:.1%} accuracy achieved")
print("=" * 60)
print("\n🚀 Ready for Day 4: Create Interactive Map!")
