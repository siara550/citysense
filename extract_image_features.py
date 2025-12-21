# extract_image_features.py
from PIL import Image
import numpy as np
import pandas as pd
import os
from config import NEIGHBORHOODS

def simple_image_features(image_path):
    """Extract basic visual features without deep learning"""
    img = Image.open(image_path).convert('RGB')
    img_array = np.array(img)
    
    # Calculate color features
    avg_brightness = np.mean(img_array)
    avg_red = np.mean(img_array[:,:,0])
    avg_green = np.mean(img_array[:,:,1])
    avg_blue = np.mean(img_array[:,:,2])
    
    # Green ratio (proxy for vegetation/parks)
    green_ratio = avg_green / (avg_red + avg_blue + 1)
    
    # Blue ratio (proxy for sky visibility)
    blue_ratio = avg_blue / (avg_red + avg_green + 1)
    
    # Color variance (proxy for visual complexity/activity)
    color_variance = np.var(img_array)
    
    # Brightness variance (contrast - higher = more interesting)
    brightness_variance = np.var(np.mean(img_array, axis=2))
    
    return {
        'brightness': avg_brightness,
        'green_ratio': green_ratio,
        'blue_ratio': blue_ratio,
        'color_variance': color_variance,
        'brightness_variance': brightness_variance
    }

def extract_all_image_features():
    """Extract features for all neighborhoods"""
    print("📸 Extracting image features...\n")
    
    image_features = []
    
    for hood in NEIGHBORHOODS:
        print(f"Processing {hood['name']}...")
        
        hood_features = {'name': hood['name']}
        
        # Collect features from all 4 directions
        all_features = []
        for heading in [0, 90, 180, 270]:
            img_path = f"data/raw/images/{hood['name']}_{heading}.jpg"
            if os.path.exists(img_path):
                features = simple_image_features(img_path)
                all_features.append(features)
        
        # Average across all 4 directions
        for metric in ['brightness', 'green_ratio', 'blue_ratio', 'color_variance', 'brightness_variance']:
            values = [f[metric] for f in all_features]
            hood_features[f'avg_{metric}'] = np.mean(values) if values else 0
        
        image_features.append(hood_features)
    
    df_images = pd.DataFrame(image_features)
    
    print(f"\n✅ Extracted image features!")
    print(f"📁 Saving to data/processed/features_images.csv\n")
    print(df_images)
    
    return df_images

if __name__ == "__main__":
    features = extract_all_image_features()
    features.to_csv("data/processed/features_images.csv", index=False)
    print("\n✅ Done!")
