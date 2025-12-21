# test_api.py
import requests
from config import GOOGLE_MAPS_API_KEY, NEIGHBORHOODS

def test_street_view():
    """Test if your API key works"""
    
    hood = NEIGHBORHOODS[0]  # Test with Williamsburg
    
    url = "https://maps.googleapis.com/maps/api/streetview"
    params = {
        "size": "400x400",
        "location": f"{hood['lat']},{hood['lon']}",
        "key": GOOGLE_MAPS_API_KEY
    }
    
    print(f"Testing API with {hood['name']}...")
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        # Save test image
        with open("test_image.jpg", "wb") as f:
            f.write(response.content)
        print("✓ SUCCESS! API key works!")
        print("✓ Saved test image as test_image.jpg")
        print("Open it to see a street view of Williamsburg")
        return True
    else:
        print(f"✗ ERROR: Status code {response.status_code}")
        print(f"Response: {response.text}")
        return False

if __name__ == "__main__":
    test_street_view()