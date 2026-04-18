# 🌾 Streamlit Dashboard - Demo Instructions

## Quick Start

### 1. Install Dependencies
Open terminal and run:
```bash
pip install -r requirements.txt
```

### 2. Run the App
```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

---

## What's in the Demo?

### 📊 Tab 1: Recommendations
- **Top 10 Crops by Yield Potential** - Best for productivity
- **Top 10 Crops by Profitability** - Best for market returns
- Side-by-side visualizations comparing yield vs profit

### 📈 Tab 2: Yield Analysis
- Detailed yield statistics and trends
- Search and filter crops by name and minimum score
- Scatter plot showing relationship between area cultivated vs yield
- Interactive data table

### 💰 Tab 3: Profit Analysis
- Market profitability rankings
- Average price, median price, and price variations
- Search by crop name or minimum price
- Visualizations of price vs yield correlation
- Revenue potential charts

### 🔮 Tab 4: Prediction Tool
- **Interactive Crop Recommendation Engine**
- Adjust soil conditions:
  - Nitrogen, Phosphorus, Potassium levels
  - Soil pH type
  - Organic matter content
- Adjust climate preferences:
  - Temperature range
  - Rainfall range
  - Humidity level
  - Season selection
- See real-time suitability scores for all crops

---

## Features

✅ **Three Ranking Systems**
- Yield Potential (historical productivity)
- Profit Proxy (price × yield market opportunity)
- Suitability Score (ML-based with real-time constraints)

✅ **Interactive Visualizations**
- Bar charts for top crops
- Scatter plots for relationships
- Dynamic filtering and search

✅ **Demo-Ready**
- Beautiful, professional UI
- Fully responsive
- No ML model training needed (uses pre-computed results)
- Fast loading (caches data automatically)

---

## Troubleshooting

**Issue:** "Module not found" error
```bash
pip install --upgrade streamlit pandas numpy matplotlib seaborn scikit-learn
```

**Issue:** "Data path not found"
- Make sure the data is in: `c:\Users\tanis\Documents\Project 2\Project---2\Data\`
- Modify the `data_path` in `app.py` if your folder structure is different

**Issue:** App running slowly
- The first run loads all data (takes ~10-20 seconds)
- Subsequent runs use cache (very fast)
- Use small screens or reload if needed

---

## For Your Demo

### Suggested Talking Points:

1. **Show Recommendations Tab**
   - "These are the top crops recommended for Thanjavur based on historical yield and profitability data"
   - Highlight the top 3-5 crops in both rankings

2. **Show Profit Analysis Tab**
   - "This shows which crops give the best market returns"
   - Point out high-profit crops with price volatility data

3. **Interactive Prediction Tool Demo**
   - Adjust soil conditions and show how recommendations change
   - "If we adjust nitrogen levels, we get different recommendations"
   - This shows the ML model is responsive to real conditions

4. **Key Takeaways**
   - Model uses 3 ranking systems (not just one factor)
   - Combines soil science + market economics + ML predictions
   - Designed for Thanjavur's specific climate and soil

---

## Next Steps

Want to enhance further?
- Add exports (CSV/PDF downloads)
- Add soil/weather data input forms
- Deploy to cloud (Streamlit Cloud, Heroku)
- Add more districts
- Include real-time weather API integration

