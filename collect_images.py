# collect_images.py
import requests
from config import NEIGHBORHOODS, GOOGLE_MAPS_API_KEY
import time
import os

def download_image(lat, lon, name, heading=0):
    url = "https://maps.googleapis.com/maps/api/streetview"
    params = {
        "size": "400x400",
        "location": f"{lat},{lon}",
        "heading": heading,
        "key": GOOGLE_MAPS_API_KEY
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        filename = f"data/raw/images/{name}_{heading}.jpg"
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"  ✓ {heading}°")
        return True
    else:
        print(f"  ✗ {heading}° failed")
        return False

# Create images folder
os.makedirs("data/raw/images", exist_ok=True)

print("🏙️  Downloading Street View images...")
print(f"📸 Total: {len(NEIGHBORHOODS) * 4} images\n")

# Get 4 directions per neighborhood (20 images total)
for i, hood in enumerate(NEIGHBORHOODS, 1):
    print(f"[{i}/{len(NEIGHBORHOODS)}] {hood['name']}")
    for heading in [0, 90, 180, 270]:
        download_image(hood['lat'], hood['lon'], hood['name'], heading)
        time.sleep(0.3)

print("\n✅ Downloaded 20 street view images!")
print("📁 Location: data/raw/images/")
