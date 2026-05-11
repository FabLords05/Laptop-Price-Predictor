# 💻 Laptop Price Predictor

An interactive web application that predicts laptop prices based on specifications using machine learning.

## Features

✨ **Real-time Predictions** - Get instant price estimates as you adjust specs
📊 **Interactive Dashboard** - Tabs for summary, detailed specs, and price comparisons
🎨 **Modern UI** - Clean, responsive design with metrics and visualizations
🔧 **Comprehensive Inputs** - 40+ specification parameters
📈 **Price Analytics** - Price-per-GB RAM, price-per-kg, and more

## Installation

### Local Setup

1. **Clone/Download the project**
```bash
cd "Laptop Price Predictor App"
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the app**
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Deployment

### Deploy to Streamlit Cloud (Recommended)

1. Push your project to GitHub
2. Go to [Streamlit Cloud](https://share.streamlit.io)
3. Click "New app"
4. Connect your GitHub repo
5. Select this app file and deploy

### Deploy to Heroku

1. Create `Procfile`:
```
web: streamlit run app.py --logger.level=error
```

2. Deploy:
```bash
heroku create your-app-name
git push heroku main
```

### Deploy to AWS/Azure

- Use Docker with the provided configuration
- Deploy to App Service (Azure) or EC2 (AWS)
- Ensure model file (`laptop_price_model.pkl`) is included

## Project Structure

```
Laptop Price Predictor App/
├── app.py                    # Main Streamlit application
├── laptop_price_model.pkl    # Trained ML model
├── requirements.txt          # Python dependencies
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## Model Features

The predictor uses 43 features including:
- **Display**: Screen size, resolution, PPI, touchscreen, IPS panel
- **Hardware**: CPU frequency, RAM, weight, SSD/HDD storage
- **Processor**: Intel or AMD architecture
- **Graphics**: GPU manufacturer (ARM, Intel, Nvidia)
- **Brand**: 18 major laptop manufacturers
- **Type**: Gaming, Netbook, Notebook, Ultrabook, Workstation
- **OS**: Windows, Mac, Linux, Other

## Usage Tips

1. **For Budget Laptops**: Select lower specs (RAM, storage, screen size)
2. **For Gaming**: Choose Gaming type with Nvidia GPU
3. **For Professionals**: Ultrabook/Workstation with high specs
4. **For Portability**: Lower weight and smaller screen size

## Technical Details

- **Algorithm**: Random Forest Regressor
- **Training Data**: Laptop specifications dataset
- **Output**: Price in Euros
- **Accuracy**: Model trained on historical laptop data

## Requirements

- Python 3.8+
- Streamlit 1.0+
- scikit-learn 1.4+
- pandas 2.0+
- joblib 1.3+

## Contributing

Feel free to improve the model or UI! Areas for enhancement:
- Additional laptop brands
- More hardware configurations
- Price comparison with real marketplaces
- Historical price trends
- Depreciation calculator

## License

MIT License - Feel free to use and modify

## Support

For issues or questions:
1. Check the specifications are realistic
2. Ensure `laptop_price_model.pkl` is in the project directory
3. Verify all dependencies are installed: `pip install -r requirements.txt`

---

**Made with ❤️ using Streamlit**
# Laptop-Price-Predictor
