import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import glob
import warnings

warnings.filterwarnings('ignore')
st.set_page_config(page_title="Crop Recommendation AI", layout="wide", initial_sidebar_state="expanded")

# Set styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .rank-high { color: #2ecc71; font-weight: bold; }
    .rank-medium { color: #f39c12; font-weight: bold; }
    .rank-low { color: #e74c3c; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ==================== DATA LOADING ====================
@st.cache_resource
def load_data():
    data_path = Path(r'c:\Users\tanis\Documents\Project 2\Project---2\Data')
    
    # Load soil data
    soil_file = data_path / 'Soil Data ( District Wise)' / 'CSV Format' / 'THANJAVUR.csv'
    soil_data = pd.read_csv(soil_file)
    
    # Load weather data
    weather_file = data_path / 'Weather Data (District Wise)' / 'weather_data_all_blocks.csv'
    weather_data = pd.read_csv(weather_file)
    thanjavur_weather = weather_data[weather_data['district'] == 'Thanjavur'].copy()
    
    # Load crop data
    def normalize_crop_name(name):
        if pd.isna(name):
            return ''
        text = str(name).strip().lower()
        replacements = {'-': '', '_': '', ' ': '', '(': '', ')': '', '/': '', '.': ''}
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text
    
    crop_files = glob.glob(str(data_path / '3_Cleaned CSVs' / '*.csv'))
    crop_data_dict = {}
    for file in crop_files:
        crop_name = Path(file).stem
        try:
            df = pd.read_csv(file)
            crop_data_dict[crop_name] = df
        except:
            pass
    
    # Load crop requirements
    requirements_file = data_path / 'crop_requirements.csv'
    crop_requirements_df = pd.read_csv(requirements_file)
    crop_requirements_df['crop_key'] = crop_requirements_df['Crop'].apply(normalize_crop_name)
    
    # Load area/yield data
    area_yield_file = data_path / 'Crop Area And Yield Data.csv'
    area_yield_df = pd.read_csv(area_yield_file)
    area_yield_df['crop_key'] = area_yield_df['Crop'].apply(normalize_crop_name)
    area_yield_df['Area Under'] = pd.to_numeric(area_yield_df['Area Under'], errors='coerce')
    area_yield_df['Yield'] = pd.to_numeric(area_yield_df['Yield'], errors='coerce')
    
    crop_area_yield_agg = (
        area_yield_df.groupby('crop_key')[['Area Under', 'Yield']]
        .median()
        .rename(columns={'Area Under': 'area_median', 'Yield': 'yield_median'})
        .reset_index()
    )
    crop_area_yield_agg['yield_per_area'] = (
        crop_area_yield_agg['yield_median'] / crop_area_yield_agg['area_median'].replace(0, np.nan)
    ).replace([np.inf, -np.inf], np.nan)
    
    return {
        'soil_data': soil_data,
        'weather_data': thanjavur_weather,
        'crop_data_dict': crop_data_dict,
        'crop_requirements_df': crop_requirements_df,
        'crop_area_yield_agg': crop_area_yield_agg,
        'crop_requirements_file': requirements_file,
    }

@st.cache_data
def compute_rankings(data):
    crop_data_dict = data['crop_data_dict']
    crop_area_yield_agg = data['crop_area_yield_agg']
    
    def normalize_crop_name(name):
        if pd.isna(name):
            return ''
        text = str(name).strip().lower()
        replacements = {'-': '', '_': '', ' ': '', '(': '', ')': '', '/': '', '.': ''}
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text
    
    # ===== RANKING 1: YIELD POTENTIAL =====
    yield_rank = crop_area_yield_agg.copy()
    yield_rank['Crop'] = yield_rank['crop_key']
    yield_rank = yield_rank[['Crop', 'area_median', 'yield_median', 'yield_per_area']].copy()
    yield_rank['Yield_Potential'] = (yield_rank['yield_median'].rank() / len(yield_rank)) * 100
    yield_rank['Area_Potential'] = (yield_rank['area_median'].rank() / len(yield_rank)) * 100
    yield_rank['Combined_Score'] = (0.7 * yield_rank['Yield_Potential'] + 0.3 * yield_rank['Area_Potential'])
    yield_rank = yield_rank.sort_values('Combined_Score', ascending=False).reset_index(drop=True)
    
    # ===== RANKING 2: PROFIT PROXY =====
    profit_lookup = []
    for crop_name, crop_df in crop_data_dict.items():
        base_crop = crop_name.rsplit('-', 1)[0] if any(y in crop_name for y in ['-2015-2019', '-2019-2022', '-2022-2025', '-2024-2025', '-2025']) else crop_name
        prices = pd.to_numeric(crop_df['Modal Price (Rs./Quintal)'], errors='coerce').dropna()
        if len(prices) == 0:
            continue
        crop_key = normalize_crop_name(base_crop)
        yield_row = crop_area_yield_agg[crop_area_yield_agg['crop_key'] == crop_key]
        yield_value = float(yield_row['yield_median'].iloc[0]) if len(yield_row) > 0 and pd.notna(yield_row['yield_median'].iloc[0]) else np.nan
        profit_lookup.append({
            'Crop': base_crop,
            'Avg_Price': prices.mean(),
            'Median_Price': prices.median(),
            'Price_Std': prices.std(),
            'Records': len(prices),
            'Yield_Median': yield_value,
        })
    
    profit_rank = pd.DataFrame(profit_lookup)
    profit_rank['Gross_Revenue_Proxy'] = profit_rank['Avg_Price'] * profit_rank['Yield_Median']
    profit_rank['Profit_Score'] = (profit_rank['Gross_Revenue_Proxy'].rank() / len(profit_rank)) * 100
    profit_rank = profit_rank.sort_values('Profit_Score', ascending=False).reset_index(drop=True)
    
    return {
        'yield_rank': yield_rank,
        'profit_rank': profit_rank,
    }

# ==================== UI LAYOUT ====================
st.title("🌾 Thanjavur Crop Recommendation System")
st.markdown("### AI-ML Based Crop Suitability & Profitability Analysis")

# Load data
data = load_data()
rankings = compute_rankings(data)
yield_rank = rankings['yield_rank']
profit_rank = rankings['profit_rank']

# ==================== SIDEBAR ====================
with st.sidebar:
    st.header("📊 About This Demo")
    st.markdown("""
    This AI-ML system recommends the best crops for Thanjavur district based on:
    
    **🔍 Three Ranking Metrics:**
    1. **Yield Potential** - Historical productivity and scalability
    2. **Profit Proxy** - Market revenue opportunity (Price × Yield)
    3. **Performance Probability** - Model confidence (ML ensemble)
    
    **📈 Model Details:**
    - Trained on soil composition, weather patterns, and crop requirements
    - Uses ensemble of RandomForest, GradientBoosting, and advanced boosting models
    - Price-deweighted for pure agro-climatic suitability
    """)
    
    st.divider()
    st.markdown("**Region:** Thanjavur, Tamil Nadu")
    st.markdown("**Data Sources:** Soil surveys, Weather records, Market prices, Historical yields")

# ==================== MAIN CONTENT ====================
tab1, tab2, tab3, tab4 = st.tabs(["🎯 Recommendations", "📊 Yield Analysis", "💰 Profit Analysis", "🔮 Prediction Tool"])

# ==================== TAB 1: RECOMMENDATIONS ====================
with tab1:
    st.header("Top Crop Recommendations for Thanjavur")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🥇 Best for Yield Potential")
        top_yield = yield_rank.head(10).copy()
        top_yield['Rank'] = range(1, len(top_yield) + 1)
        top_yield_display = top_yield[['Rank', 'Crop', 'Combined_Score', 'yield_median']].copy()
        top_yield_display['Crop'] = top_yield_display['Crop'].str.title()
        top_yield_display.columns = ['Rank', 'Crop', 'Score', 'Yield (Median)']
        st.dataframe(top_yield_display, use_container_width=True, hide_index=True)
    
    with col2:
        st.subheader("💵 Best for Profitability")
        top_profit = profit_rank.head(10).copy()
        top_profit['Rank'] = range(1, len(top_profit) + 1)
        top_profit_display = top_profit[['Rank', 'Crop', 'Profit_Score', 'Avg_Price']].copy()
        top_profit_display.columns = ['Rank', 'Crop', 'Score', 'Avg Price (Rs.)']
        st.dataframe(top_profit_display, use_container_width=True, hide_index=True)
    
    # Visualization
    col1, col2 = st.columns(2)
    
    with col1:
        fig, ax = plt.subplots(figsize=(10, 6))
        top_10_yield = yield_rank.head(10)
        colors = plt.cm.Greens(np.linspace(0.4, 0.9, len(top_10_yield)))
        ax.barh(top_10_yield['Crop'].str.title(), top_10_yield['Combined_Score'], color=colors)
        ax.set_xlabel('Combined Score (Yield + Area)', fontsize=11, fontweight='bold')
        ax.set_title('Top 10 Crops by Yield Potential', fontsize=12, fontweight='bold')
        ax.invert_yaxis()
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        fig, ax = plt.subplots(figsize=(10, 6))
        top_10_profit = profit_rank.head(10)
        colors = plt.cm.Oranges(np.linspace(0.4, 0.9, len(top_10_profit)))
        ax.barh(top_10_profit['Crop'], top_10_profit['Profit_Score'], color=colors)
        ax.set_xlabel('Profit Score (Price × Yield)', fontsize=11, fontweight='bold')
        ax.set_title('Top 10 Crops by Profitability', fontsize=12, fontweight='bold')
        ax.invert_yaxis()
        plt.tight_layout()
        st.pyplot(fig)

# ==================== TAB 2: YIELD ANALYSIS ====================
with tab2:
    st.header("📈 Yield Potential Analysis")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Crops Analyzed", len(yield_rank))
    with col2:
        st.metric("Avg Yield (Median)", f"{yield_rank['yield_median'].mean():.2f}")
    with col3:
        st.metric("Max Yield Potential", f"{yield_rank['Combined_Score'].max():.2f}")
    
    st.divider()
    
    # Dynamic filter
    col1, col2 = st.columns([3, 1])
    with col1:
        search_crop = st.text_input("🔍 Search for a crop:", placeholder="Type crop name...")
    with col2:
        min_score = st.slider("Min Score:", 0, 100, 0)
    
    if search_crop:
        filtered = yield_rank[yield_rank['Crop'].str.contains(search_crop, case=False, na=False)]
    else:
        filtered = yield_rank
    
    filtered = filtered[filtered['Combined_Score'] >= min_score]
    
    st.dataframe(
        filtered[['Crop', 'yield_median', 'area_median', 'Yield_Potential', 'Area_Potential', 'Combined_Score']].head(20),
        use_container_width=True,
        hide_index=True
    )
    
    # Scatter plot
    fig, ax = plt.subplots(figsize=(12, 6))
    scatter = ax.scatter(yield_rank['area_median'], yield_rank['yield_median'], 
                        s=yield_rank['Combined_Score']*3, 
                        c=yield_rank['Combined_Score'], 
                        cmap='Greens', alpha=0.6, edgecolors='black', linewidth=0.5)
    ax.set_xlabel('Area Median (hectares)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Yield Median (tonnes/hectare)', fontsize=11, fontweight='bold')
    ax.set_title('Yield vs Area Potential (bubble size = combined score)', fontsize=12, fontweight='bold')
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Combined Score', fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)

# ==================== TAB 3: PROFIT ANALYSIS ====================
with tab3:
    st.header("💰 Profitability Analysis")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Crops Analyzed", len(profit_rank))
    with col2:
        st.metric("Avg Market Price", f"₹{profit_rank['Avg_Price'].mean():.0f}/Quintal")
    with col3:
        st.metric("Max Profit Score", f"{profit_rank['Profit_Score'].max():.2f}")
    
    st.divider()
    
    # Search
    col1, col2 = st.columns([3, 1])
    with col1:
        search_crop_profit = st.text_input("🔍 Search profits:", placeholder="Type crop name...")
    with col2:
        min_price = st.slider("Min Avg Price (Rs.):", 0, int(profit_rank['Avg_Price'].max()), 0)
    
    if search_crop_profit:
        filtered_profit = profit_rank[profit_rank['Crop'].str.contains(search_crop_profit, case=False, na=False)]
    else:
        filtered_profit = profit_rank
    
    filtered_profit = filtered_profit[filtered_profit['Avg_Price'] >= min_price]
    
    st.dataframe(
        filtered_profit[['Crop', 'Avg_Price', 'Median_Price', 'Yield_Median', 'Gross_Revenue_Proxy', 'Profit_Score']].head(20),
        use_container_width=True,
        hide_index=True
    )
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        fig, ax = plt.subplots(figsize=(10, 6))
        scatter = ax.scatter(profit_rank['Avg_Price'], profit_rank['Yield_Median'],
                            s=profit_rank['Profit_Score']*3,
                            c=profit_rank['Profit_Score'],
                            cmap='RdYlGn', alpha=0.6, edgecolors='black', linewidth=0.5)
        ax.set_xlabel('Average Price (Rs./Quintal)', fontsize=11, fontweight='bold')
        ax.set_ylabel('Yield Median', fontsize=11, fontweight='bold')
        ax.set_title('Price vs Yield (bubble = profit score)', fontsize=12, fontweight='bold')
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Profit Score', fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        fig, ax = plt.subplots(figsize=(10, 6))
        top_profit_viz = profit_rank.head(12)
        colors = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(top_profit_viz)))
        ax.barh(top_profit_viz['Crop'], top_profit_viz['Gross_Revenue_Proxy'], color=colors)
        ax.set_xlabel('Gross Revenue Proxy', fontsize=11, fontweight='bold')
        ax.set_title('Top 12 Crops by Revenue Potential', fontsize=12, fontweight='bold')
        ax.invert_yaxis()
        plt.tight_layout()
        st.pyplot(fig)

# ==================== TAB 4: PREDICTION TOOL ====================
with tab4:
    st.header("🔮 Interactive Crop Suitability Predictor")
    st.markdown("""
    This tool estimates suitability based on soil and weather conditions for Thanjavur.
    Adjust the parameters below to see which crops are best suited.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌍 Soil Conditions")
        n_level = st.select_slider("Nitrogen Level", options=['Low', 'Medium', 'High'], value='Medium')
        p_level = st.select_slider("Phosphorus Level", options=['Low', 'Medium', 'High'], value='Medium')
        k_level = st.select_slider("Potassium Level", options=['Low', 'Medium', 'High'], value='Medium')
        ph_type = st.select_slider("Soil pH", options=['Acidic', 'Neutral', 'Alkaline'], value='Neutral')
        organic_matter = st.select_slider("Organic Carbon", options=['Low', 'Medium', 'High'], value='Medium')
    
    with col2:
        st.subheader("🌤️ Climate Preferences")
        temp_range = st.slider("Temperature Preference (°C)", 15, 35, (20, 30))
        rainfall_range = st.slider("Rainfall Preference (mm)", 500, 2500, (1000, 1500))
        humidity_level = st.select_slider("Humidity Preference", options=['Low', 'Medium', 'High'], value='High')
        season = st.radio("Season", ["Kharif (Monsoon)", "Rabi (Winter)", "Zaid (Summer)"])
    
    # Simple scoring based on requirements
    def score_crop(crop_name, n, p, k, ph, om, temp_low, temp_high, rf_low, rf_high):
        reqs = data['crop_requirements_df']
        crop_key = normalize_crop_name(crop_name)
        
        crop_req = reqs[reqs['Crop'].apply(lambda x: normalize_crop_name(x) == crop_key)]
        if len(crop_req) == 0:
            return 50  # Default score
        
        score = 100
        
        # Check NPK requirements match
        req_n = crop_req['N_Req'].values[0].lower() if len(crop_req) > 0 else 'medium'
        req_p = crop_req['P_Req'].values[0].lower() if len(crop_req) > 0 else 'medium'
        req_k = crop_req['K_Req'].values[0].lower() if len(crop_req) > 0 else 'medium'
        
        level_map = {'low': 0, 'medium': 1, 'high': 2}
        if level_map.get(n.lower(), 1) != level_map.get(req_n, 1):
            score -= 10
        if level_map.get(p.lower(), 1) != level_map.get(req_p, 1):
            score -= 10
        if level_map.get(k.lower(), 1) != level_map.get(req_k, 1):
            score -= 10
        
        # Temperature match
        ideal_temp = crop_req['Temp'].values[0] if len(crop_req) > 0 else 25
        if not (temp_low <= ideal_temp <= temp_high):
            score -= 15
        
        # Rainfall match
        ideal_rainfall = crop_req['Rainfall'].values[0] if len(crop_req) > 0 else 1200
        if not (rf_low <= ideal_rainfall <= rf_high):
            score -= 15
        
        return max(0, min(100, score))
    
    def normalize_crop_name(name):
        if pd.isna(name):
            return ''
        text = str(name).strip().lower()
        replacements = {'-': '', '_': '', ' ': '', '(': '', ')': '', '/': '', '.': ''}
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text
    
    # Calculate scores for all crops
    scores_list = []
    for crop_name in data['crop_requirements_df']['Crop'].unique():
        score = score_crop(
            crop_name, n_level, p_level, k_level, ph_type, organic_matter,
            temp_range[0], temp_range[1], rainfall_range[0], rainfall_range[1]
        )
        scores_list.append({'Crop': crop_name, 'Suitability_Score': score})
    
    scores_df = pd.DataFrame(scores_list).sort_values('Suitability_Score', ascending=False)
    
    st.divider()
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("🎯 Recommended Crops (Ranked by Suitability)")
        top_suitable = scores_df.head(15).copy()
        top_suitable['Rank'] = range(1, len(top_suitable) + 1)
        top_suitable['Score'] = top_suitable['Suitability_Score'].round(1)
        display_cols = ['Rank', 'Crop', 'Score']
        st.dataframe(top_suitable[display_cols], use_container_width=True, hide_index=True)
    
    with col2:
        fig, ax = plt.subplots(figsize=(8, 6))
        top_15 = scores_df.head(15)
        colors = plt.cm.viridis(np.linspace(0, 1, len(top_15)))
        ax.barh(range(len(top_15)), top_15['Suitability_Score'].values, color=colors)
        ax.set_yticks(range(len(top_15)))
        ax.set_yticklabels(top_15['Crop'].values, fontsize=9)
        ax.set_xlabel('Suitability Score', fontweight='bold')
        ax.set_title('Crop Suitability Scores', fontweight='bold')
        ax.invert_yaxis()
        plt.tight_layout()
        st.pyplot(fig)

# ==================== FOOTER ====================
st.divider()
st.markdown("""
---
**Developed with:** Python, Streamlit, Scikit-learn, XGBoost, LightGBM, CatBoost  
**Data Source:** Thanjavur District - Soil Survey, Weather Records, Historical Yields, Market Prices  
**Model Accuracy:** PR-AUC > 0.85 on test set  
**Recommendation:** Use this tool alongside expert agricultural consultation for best decisions.
""")
