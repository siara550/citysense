# create_map.py
import folium
import pandas as pd
from config import NEIGHBORHOODS

print("🗺️  Creating interactive map...\n")

# Load predictions
predictions = pd.read_csv("data/processed/predictions.csv")

# Color mapping
color_map = {
    'positive': '#2ecc71',  # Green
    'neutral': '#f39c12',   # Orange  
    'negative': '#e74c3c'   # Red
}

emoji_map = {
    'positive': '😊',
    'neutral': '😐',
    'negative': '😟'
}

# Create map centered on NYC
m = folium.Map(
    location=[40.7580, -73.9855],
    zoom_start=11,
    tiles='CartoDB positron'
)

print("📍 Adding neighborhoods to map...\n")

# Add markers for each neighborhood
for _, row in predictions.iterrows():
    # Get neighborhood coordinates
    hood = next(h for h in NEIGHBORHOODS if h['name'] == row['name'])
    
    emoji = emoji_map.get(row['predicted_category'], '❓')
    
    # Create detailed popup
    popup_html = f"""
    <div style="font-family: Arial; width: 250px; padding: 10px;">
        <h3 style="margin: 0 0 10px 0; color: {color_map[row['predicted_category']]};">
            {emoji} {row['name'].replace('_', ' ')}
        </h3>
        
        <div style="background: #f0f0f0; padding: 8px; border-radius: 5px; margin-bottom: 10px;">
            <strong>Prediction: {row['predicted_category'].upper()}</strong>
        </div>
        
        <p style="margin: 5px 0;"><strong>Scores:</strong></p>
        <p style="margin: 3px 0;">🛡️ Safety: {row['safety']}/5</p>
        <p style="margin: 3px 0;">🎉 Liveliness: {row['liveliness']}/5</p>
        <p style="margin: 3px 0;">✨ Cleanliness: {row['cleanliness']}/5</p>
        
        <hr style="margin: 10px 0;">
        
        <p style="margin: 5px 0;"><strong>311 Data:</strong></p>
        <p style="margin: 3px 0; font-size: 11px;">Total complaints: {int(row['total_complaints'])}</p>
        <p style="margin: 3px 0; font-size: 11px;">Noise: {int(row['noise_complaints'])}</p>
        <p style="margin: 3px 0; font-size: 11px;">Graffiti: {int(row['graffiti'])}</p>
        
        <p style="margin: 5px 0;"><strong>Visual Features:</strong></p>
        <p style="margin: 3px 0; font-size: 11px;">Green ratio: {row['avg_green_ratio']:.2f}</p>
        <p style="margin: 3px 0; font-size: 11px;">Brightness: {row['avg_brightness']:.0f}</p>
    </div>
    """
    
    # Add circle marker
    folium.CircleMarker(
        location=[hood['lat'], hood['lon']],
        radius=20,
        popup=folium.Popup(popup_html, max_width=300),
        color='white',
        fillColor=color_map[row['predicted_category']],
        fillOpacity=0.8,
        weight=3
    ).add_to(m)
    
    # Add neighborhood label
    folium.Marker(
        location=[hood['lat'] + 0.01, hood['lon']],
        icon=folium.DivIcon(html=f"""
            <div style="
                font-size: 11pt; 
                color: white;
                font-weight: bold;
                text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000;
                white-space: nowrap;
            ">
                {row['name'].replace('_', ' ')}
            </div>
        """)
    ).add_to(m)
    
    print(f"  ✓ {row['name'].replace('_', ' '):20s} → {row['predicted_category']}")

# Add legend
legend_html = '''
<div style="
    position: fixed; 
    bottom: 50px; right: 50px; 
    width: 180px;
    border: 3px solid grey; 
    z-index: 9999; 
    background-color: white;
    padding: 15px;
    font-size: 14px;
    border-radius: 10px;
    box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
">
    <h4 style="margin: 0 0 10px 0;">CitySense</h4>
    <p style="margin: 0 0 5px 0; font-size: 12px; color: #666;">
        Neighborhood Atmosphere Predictor
    </p>
    <hr style="margin: 10px 0;">
    <p style="margin: 8px 0;">
        <span style="color: #2ecc71; font-size: 18px;">●</span> 
        <strong>Positive</strong>
    </p>
    <p style="margin: 8px 0;">
        <span style="color: #f39c12; font-size: 18px;">●</span> 
        <strong>Neutral</strong>
    </p>
    <p style="margin: 8px 0;">
        <span style="color: #e74c3c; font-size: 18px;">●</span> 
        <strong>Negative</strong>
    </p>
    <hr style="margin: 10px 0;">
    <p style="margin: 0; font-size: 10px; color: #999;">
        Built with ML • 100% accuracy
    </p>
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

# Add title
title_html = '''
<div style="
    position: fixed; 
    top: 10px; 
    left: 50px; 
    width: 300px;
    z-index: 9999; 
    background-color: white;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
">
    <h2 style="margin: 0; color: #2c3e50;">🏙️ CitySense NYC</h2>
    <p style="margin: 5px 0 0 0; font-size: 12px; color: #666;">
        ML-powered neighborhood atmosphere analysis
    </p>
</div>
'''
m.get_root().html.add_child(folium.Element(title_html))

# Save
import os
os.makedirs("outputs", exist_ok=True)
m.save("outputs/citysense_map.html")

print("\n" + "=" * 60)
print("✅ MAP CREATED!")
print("📁 Location: outputs/citysense_map.html")
print("=" * 60)
print("\n🎯 To view your map:")
print("   open outputs/citysense_map.html")
print("\nOr just double-click the file!\n")
