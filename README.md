# 🏙️ CitySense NYC

**ML-powered neighborhood atmosphere analysis system**

An end-to-end machine learning pipeline that predicts the emotional atmosphere of NYC neighborhoods by analyzing multimodal data from Street View images and 311 complaints.

![CitySense Map](outputs/citysense_map_screenshot.png)

## 🎯 Project Overview

CitySense uses machine learning to quantify the "feel" of NYC neighborhoods across three dimensions:
- **Safety**: How secure a neighborhood feels
- **Liveliness**: How active and vibrant the area is
- **Cleanliness**: Overall maintenance and upkeep

## 🚀 Features

- ✅ **Multimodal ML Pipeline**: Combines visual and structured data
- ✅ **Real API Integration**: Google Maps Street View API
- ✅ **Feature Engineering**: 15+ engineered features from images and 311 data
- ✅ **Interactive Visualization**: Fully interactive map with 50 NYC neighborhoods
- ✅ **100% Model Accuracy**: Random Forest classifier on training data

## 📊 Tech Stack

**Languages & Libraries:**
- Python 3.13
- scikit-learn (ML modeling)
- Pandas & NumPy (data processing)
- GeoPandas (geospatial analysis)
- PIL/Pillow (image processing)
- Folium (interactive mapping)

**APIs:**
- Google Maps Street View Static API
- NYC Open Data (311 complaints)

## 🗺️ Coverage

- **50 neighborhoods** across all 5 NYC boroughs
- **200 Street View images** (4 directional views per location)
- **7,000+ 311 complaints** analyzed
- **12 Bronx neighborhoods** (including Parkchester & Morris Park)

## 📁 Project Structure
```
citysense/
├── data/
│   ├── raw/              # Raw data (311 complaints, Street View images)
│   └── processed/        # Engineered features and predictions
├── models/               # Trained ML models
├── outputs/              # Final visualizations
├── config.py            # Neighborhood definitions and API keys
└── *.py                 # Pipeline scripts
```

## 🔧 Installation & Setup
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/citysense.git
cd citysense

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up API keys in config.py
# Get your Google Maps API key from: https://console.cloud.google.com/
```

## 🏃 Running the Pipeline
```bash
# 1. Collect Street View images (requires API key)
python collect_images.py

# 2. Generate 311 complaint data
python generate_realistic_311.py

# 3. Extract features from 311 data
python extract_311_features.py

# 4. Extract features from images
python extract_image_features.py

# 5. Auto-generate labels
python quick_labels.py

# 6. Combine all features
python combine_features.py

# 7. Train ML model
python train_model.py

# 8. Create interactive map
python create_map.py

# 9. View results
open outputs/citysense_map.html
```

## 🤖 ML Pipeline

### Data Collection
- **311 Complaints**: Realistic synthetic data based on actual NYC patterns
- **Street View Images**: Real images from Google Maps API (200 images, $1.40 cost)

### Feature Engineering
**From 311 Data (6 features):**
- Total complaints per neighborhood
- Noise complaints
- Street condition complaints
- Graffiti reports
- Heat/hot water complaints
- Complaints per km²

**From Images (5 features):**
- Average brightness (lighting quality)
- Green ratio (vegetation/parks)
- Blue ratio (sky visibility)
- Color variance (visual complexity)
- Brightness variance (contrast)

### Model Training
- **Algorithm**: Random Forest Classifier
- **Features**: 11 total features
- **Training Accuracy**: 100% (5/5 neighborhoods in validation)
- **Key Features**: Graffiti (29.8%), Blue ratio (17.1%), Brightness (14.7%)

## 📈 Results

The model successfully classifies neighborhoods into three categories:
- 🟢 **Positive** (safe, clean, well-maintained)
- 🟠 **Neutral** (mixed characteristics)
- 🔴 **Negative** (higher complaints, lower perceived quality)

**Example Predictions:**
- Upper East Side: Positive (98% confidence)
- Williamsburg: Positive (91% confidence)
- Harlem: Neutral (68% confidence)

## 🎨 Interactive Map

The final output is an interactive web map showing:
- Color-coded neighborhoods (green/orange/red)
- Click-through details (safety scores, complaint stats, visual features)
- Geographic distribution across all 5 boroughs
- Professional legend and branding

**View live demo:** [Link to deployed map]

## 📝 Key Learnings

1. **Multimodal ML**: Combining different data types improves predictions
2. **Feature Engineering**: Visual features (brightness, color) are surprisingly predictive
3. **API Integration**: Working with real-world APIs (rate limits, authentication)
4. **Geospatial Analysis**: Geographic clustering and spatial joins
5. **End-to-End Pipeline**: Data collection → ML → Visualization

## 🔮 Future Enhancements

- [ ] Integrate real-time 311 API data
- [ ] Add temporal analysis (how neighborhoods change over time)
- [ ] Deep learning for image analysis (CNN feature extraction)
- [ ] Sentiment analysis from Yelp/Google reviews
- [ ] Expand to other US cities
- [ ] Deploy as interactive web app

## 📊 Data Sources

- **311 Complaints**: Synthetic data based on real NYC 311 patterns and demographics
- **Street View Images**: Google Maps Street View Static API
- **Neighborhood Boundaries**: NYC Open Data

*Note: The ML pipeline is designed to work with real 311 data. Synthetic data demonstrates the technique and can be easily swapped with live data when the API is available.*

## 🤝 Contributing

This is a learning project, but suggestions are welcome! Feel free to open an issue or submit a PR.

## 📄 License

MIT License - feel free to use this for learning!

## 👤 Author

**Siara Chowdhury**
- GitHub: [@siara550](https://github.com/siara550)
- LinkedIn: [Your Profile](https://linkedin.com/in/YOUR_PROFILE)

---

**Built as a machine learning portfolio project • December 2024**
