"""
Comprehensive Data Analysis Script for Thanjavur Region
=========================================================
Analyzes soil data, crop prices, and provides detailed visualizations
and statistics for the Thanjavur district in Tamil Nadu.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set style for visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10

# Define paths
BASE_PATH = Path('.')
SOIL_DATA_PATH = BASE_PATH / 'Data' / 'Soil Data ( District Wise)' / 'CSV Format' / 'THANJAVUR.csv'
CROP_DATA_PATH = BASE_PATH / 'Data' / '3_Cleaned CSVs'


class ThanjavurAnalysis:
    """Main class for analyzing Thanjavur region agricultural data"""
    
    def __init__(self):
        self.soil_data = None
        self.crop_data = {}
        self.weather_data = None
        
    def load_soil_data(self):
        """Load and process soil data for Thanjavur"""
        print("=" * 80)
        print("LOADING SOIL DATA FOR THANJAVUR REGION")
        print("=" * 80)
        
        try:
            self.soil_data = pd.read_csv(SOIL_DATA_PATH)
            print(f"✓ Soil data loaded successfully!")
            print(f"  Shape: {self.soil_data.shape}")
            print(f"  Records: {len(self.soil_data)}")
            print(f"  Blocks in Thanjavur: {self.soil_data['Block'].nunique()}")
            return True
        except FileNotFoundError:
            print(f"✗ Error: Could not find soil data at {SOIL_DATA_PATH}")
            return False
    
    def load_crop_price_data(self):
        """Load crop price data for all crops"""
        print("\n" + "=" * 80)
        print("LOADING CROP PRICE DATA")
        print("=" * 80)
        
        csv_files = list(CROP_DATA_PATH.glob('*.csv'))
        
        if not csv_files:
            print("✗ No CSV files found in crop data directory")
            return
        
        thanjavur_records = 0
        
        for csv_file in csv_files:
            try:
                df = pd.read_csv(csv_file)
                
                # Filter for Thanjavur region only
                if 'District Name' in df.columns:
                    thanjavur_df = df[df['District Name'].str.contains('Thanjavur|THANJAVUR', 
                                                                        case=False, na=False)]
                    
                    if len(thanjavur_df) > 0:
                        self.crop_data[csv_file.stem] = thanjavur_df
                        thanjavur_records += len(thanjavur_df)
                        print(f"✓ {csv_file.stem}: {len(thanjavur_df)} records")
            
            except Exception as e:
                print(f"✗ Error loading {csv_file.stem}: {str(e)}")
        
        print(f"\nTotal Thanjavur crop price records: {thanjavur_records}")
        return len(self.crop_data) > 0
    
    def analyze_soil_data(self):
        """Detailed analysis of soil characteristics"""
        print("\n" + "=" * 80)
        print("SOIL DATA ANALYSIS - THANJAVUR REGION")
        print("=" * 80)
        
        if self.soil_data is None:
            print("No soil data loaded")
            return
        
        df = self.soil_data
        
        # Basic statistics
        print(f"\n📊 BASIC STATISTICS:")
        print(f"  Total Records: {len(df)}")
        print(f"  Number of Blocks: {df['Block'].nunique()}")
        print(f"  Blocks: {', '.join(df['Block'].unique())}")
        
        # Nitrogen Analysis
        print(f"\n🌾 NITROGEN (N) STATUS:")
        n_high = df['n_High'].sum()
        n_medium = df['n_Medium'].sum()
        n_low = df['n_Low'].sum()
        print(f"  High: {n_high:.2f}% | Medium: {n_medium:.2f}% | Low: {n_low:.2f}%")
        print(f"  Analysis: {'Most soil has low nitrogen' if n_low > 50 else 'Nitrogen levels are adequate'}")
        
        # Phosphorus Analysis
        print(f"\n🌾 PHOSPHORUS (P) STATUS:")
        p_high = df['p_High'].sum()
        p_medium = df['p_Medium'].sum()
        p_low = df['p_Low'].sum()
        print(f"  High: {p_high:.2f}% | Medium: {p_medium:.2f}% | Low: {p_low:.2f}%")
        print(f"  Analysis: {'Most soil has low phosphorus' if p_low > 50 else 'Phosphorus levels are adequate'}")
        
        # Potassium Analysis
        print(f"\n🌾 POTASSIUM (K) STATUS:")
        k_high = df['k_High'].sum()
        k_medium = df['k_Medium'].sum()
        k_low = df['k_Low'].sum()
        print(f"  High: {k_high:.2f}% | Medium: {k_medium:.2f}% | Low: {k_low:.2f}%")
        
        # pH Analysis
        print(f"\n🧪 pH STATUS:")
        ph_alkaline = df['pH_Alkaline'].sum()
        ph_acidic = df['pH_Acidic'].sum()
        ph_neutral = df['pH_Neutral'].sum()
        print(f"  Alkaline: {ph_alkaline:.2f}% | Neutral: {ph_neutral:.2f}% | Acidic: {ph_acidic:.2f}%")
        
        # Organic Carbon Analysis
        print(f"\n🌱 ORGANIC CARBON (OC) STATUS:")
        oc_high = df['OC_High'].sum()
        oc_medium = df['OC_Medium'].sum()
        oc_low = df['OC_Low'].sum()
        print(f"  High: {oc_high:.2f}% | Medium: {oc_medium:.2f}% | Low: {oc_low:.2f}%")
        
        # Micronutrients
        print(f"\n⚗️ MICRONUTRIENTS STATUS:")
        print(f"  Iron (Fe)    - Sufficient: {df['Fe_Sufficient'].sum():.2f}%")
        print(f"  Zinc (Zn)    - Sufficient: {df['Zn_Sufficient'].sum():.2f}%")
        print(f"  Copper (Cu)  - Sufficient: {df['Cu_Sufficient'].sum():.2f}%")
        print(f"  Boron (B)    - Sufficient: {df['B_Sufficient'].sum():.2f}%")
        print(f"  Manganese (Mn) - Sufficient: {df['Mn_Sufficient'].sum():.2f}%")
        
        # Salinity
        print(f"\n🧂 SALINITY (EC) STATUS:")
        ec_saline = df['EC_Saline'].sum()
        ec_non_saline = df['EC_NonSaline'].sum()
        print(f"  Non-Saline: {ec_non_saline:.2f}% | Saline: {ec_saline:.2f}%")
    
    def analyze_crop_prices(self):
        """Analyze crop price data"""
        print("\n" + "=" * 80)
        print("CROP PRICE ANALYSIS - THANJAVUR REGION")
        print("=" * 80)
        
        if not self.crop_data:
            print("No crop data loaded for Thanjavur")
            return
        
        total_records = sum(len(df) for df in self.crop_data.values())
        print(f"\n📊 Total Crop Price Records: {total_records}")
        print(f"Different Crops: {len(self.crop_data)}\n")
        
        crop_analysis = []
        
        for crop_name, df in self.crop_data.items():
            records = len(df)
            
            # Price columns
            price_cols = ['Min Price (Rs./Quintal)', 'Max Price (Rs./Quintal)', 
                         'Modal Price (Rs./Quintal)']
            
            available_cols = [col for col in price_cols if col in df.columns]
            
            if available_cols:
                avg_min = df[available_cols[0]].mean() if available_cols[0] in df.columns else 0
                avg_max = df[available_cols[1]].mean() if available_cols[1] in df.columns else 0
                avg_modal = df[available_cols[2]].mean() if available_cols[2] in df.columns else 0
                
                print(f"🌾 {crop_name.upper()}")
                print(f"   Records: {records}")
                print(f"   Avg Min Price: ₹{avg_min:.2f}/Quintal")
                print(f"   Avg Max Price: ₹{avg_max:.2f}/Quintal")
                print(f"   Avg Modal Price: ₹{avg_modal:.2f}/Quintal")
                
                # Convert Price Date to datetime and find date range
                if 'Price Date' in df.columns:
                    try:
                        df['Price Date'] = pd.to_datetime(df['Price Date'])
                        date_range = f"{df['Price Date'].min().date()} to {df['Price Date'].max().date()}"
                        print(f"   Date Range: {date_range}")
                    except:
                        pass
                
                if 'Variety' in df.columns:
                    varieties = df['Variety'].nunique()
                    print(f"   Varieties: {varieties}")
                
                print()
                
                crop_analysis.append({
                    'Crop': crop_name,
                    'Records': records,
                    'Avg_Min_Price': avg_min,
                    'Avg_Max_Price': avg_max,
                    'Avg_Modal_Price': avg_modal
                })
        
        return crop_analysis
    
    def generate_soil_visualizations(self):
        """Create soil data visualizations"""
        if self.soil_data is None:
            print("No soil data for visualizations")
            return
        
        print("\n" + "=" * 80)
        print("GENERATING SOIL DATA VISUALIZATIONS")
        print("=" * 80)
        
        df = self.soil_data
        
        # Figure 1: Macronutrients Distribution
        fig, axes = plt.subplots(1, 3, figsize=(16, 5))
        fig.suptitle('Macronutrients Distribution - Thanjavur Region', fontsize=14, fontweight='bold')
        
        nutrients = [
            ('N (Nitrogen)', ['n_High', 'n_Medium', 'n_Low']),
            ('P (Phosphorus)', ['p_High', 'p_Medium', 'p_Low']),
            ('K (Potassium)', ['k_High', 'k_Medium', 'k_Low'])
        ]
        
        colors = ['#2ecc71', '#f39c12', '#e74c3c']
        
        for idx, (nutrient_name, cols) in enumerate(nutrients):
            values = [df[cols[0]].sum(), df[cols[1]].sum(), df[cols[2]].sum()]
            axes[idx].pie(values, labels=['High', 'Medium', 'Low'], autopct='%1.1f%%',
                         colors=colors, startangle=90)
            axes[idx].set_title(nutrient_name, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('soil_macronutrients.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: soil_macronutrients.png")
        plt.close()
        
        # Figure 2: pH Distribution
        fig, ax = plt.subplots(figsize=(10, 6))
        ph_values = [df['pH_Acidic'].sum(), df['pH_Neutral'].sum(), df['pH_Alkaline'].sum()]
        bars = ax.bar(['Acidic', 'Neutral', 'Alkaline'], ph_values, 
                      color=['#3498db', '#2ecc71', '#e67e22'], edgecolor='black', linewidth=1.5)
        ax.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')
        ax.set_title('Soil pH Classification - Thanjavur Region', fontsize=14, fontweight='bold')
        ax.set_ylim(0, max(ph_values) * 1.1)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('soil_pH_distribution.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: soil_pH_distribution.png")
        plt.close()
        
        # Figure 3: Micronutrients Sufficiency
        fig, ax = plt.subplots(figsize=(12, 6))
        micronutrients = ['Fe', 'Zn', 'Cu', 'B', 'Mn']
        sufficient = [
            df['Fe_Sufficient'].sum(),
            df['Zn_Sufficient'].sum(),
            df['Cu_Sufficient'].sum(),
            df['B_Sufficient'].sum(),
            df['Mn_Sufficient'].sum()
        ]
        
        bars = ax.bar(micronutrients, sufficient, color='#9b59b6', edgecolor='black', linewidth=1.5)
        ax.set_ylabel('Sufficient (%)', fontsize=12, fontweight='bold')
        ax.set_xlabel('Micronutrient', fontsize=12, fontweight='bold')
        ax.set_title('Micronutrient Sufficiency Status - Thanjavur Region', fontsize=14, fontweight='bold')
        ax.set_ylim(0, 100)
        ax.axhline(y=50, color='r', linestyle='--', alpha=0.5, label='50% threshold')
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        ax.legend()
        plt.tight_layout()
        plt.savefig('soil_micronutrients.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: soil_micronutrients.png")
        plt.close()
        
        # Figure 4: Block-wise Soil Quality Comparison
        fig, ax = plt.subplots(figsize=(14, 7))
        
        # Calculate soil quality score for each block
        block_quality = df.copy()
        block_quality['Soil_Quality_Score'] = (
            block_quality['n_Medium'] + block_quality['n_High'] +
            block_quality['p_Medium'] + block_quality['p_High'] +
            block_quality['k_Medium'] + block_quality['k_High']
        ) / 6
        
        block_quality_sorted = block_quality.sort_values('Soil_Quality_Score', ascending=True)
        
        bars = ax.barh(block_quality_sorted['Block'], block_quality_sorted['Soil_Quality_Score'],
                       color='#1abc9c', edgecolor='black', linewidth=1.5)
        ax.set_xlabel('Soil Quality Score', fontsize=12, fontweight='bold')
        ax.set_title('Soil Quality Index by Block - Thanjavur Region', fontsize=14, fontweight='bold')
        
        for idx, (bar, val) in enumerate(zip(bars, block_quality_sorted['Soil_Quality_Score'])):
            ax.text(val, bar.get_y() + bar.get_height()/2., f'{val:.1f}',
                   ha='left', va='center', fontweight='bold', fontsize=9)
        
        plt.tight_layout()
        plt.savefig('soil_block_comparison.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: soil_block_comparison.png")
        plt.close()
    
    def generate_crop_price_visualizations(self):
        """Create crop price visualizations"""
        if not self.crop_data:
            print("No crop data for visualizations")
            return
        
        print("\n" + "=" * 80)
        print("GENERATING CROP PRICE VISUALIZATIONS")
        print("=" * 80)
        
        # Combine all crop data
        all_crops = []
        
        for crop_name, df in self.crop_data.items():
            price_cols = ['Min Price (Rs./Quintal)', 'Max Price (Rs./Quintal)', 
                         'Modal Price (Rs./Quintal)']
            available_cols = [col for col in price_cols if col in df.columns]
            
            if available_cols:
                modal_price = df[available_cols[2]].mean()
                all_crops.append({
                    'Crop': crop_name.replace('_', ' ').title(),
                    'Avg_Modal_Price': modal_price,
                    'Count': len(df)
                })
        
        if all_crops:
            crop_df = pd.DataFrame(all_crops).sort_values('Avg_Modal_Price', ascending=False)
            
            # Figure 5: Crop Price Comparison
            fig, ax = plt.subplots(figsize=(14, 8))
            colors_grad = plt.cm.viridis(np.linspace(0, 1, len(crop_df)))
            bars = ax.barh(crop_df['Crop'], crop_df['Avg_Modal_Price'], color=colors_grad, edgecolor='black')
            ax.set_xlabel('Average Modal Price (Rs./Quintal)', fontsize=12, fontweight='bold')
            ax.set_title('Average Crop Prices - Thanjavur Region', fontsize=14, fontweight='bold')
            
            for bar, val in zip(bars, crop_df['Avg_Modal_Price']):
                ax.text(val, bar.get_y() + bar.get_height()/2., f'₹{val:.0f}',
                       ha='left', va='center', fontweight='bold', fontsize=9)
            
            plt.tight_layout()
            plt.savefig('crop_prices_comparison.png', dpi=300, bbox_inches='tight')
            print("✓ Saved: crop_prices_comparison.png")
            plt.close()
        
        # Figure 6: Records count by crop
        if all_crops:
            crop_df_sorted = crop_df.sort_values('Count', ascending=True)
            fig, ax = plt.subplots(figsize=(12, 8))
            bars = ax.barh(crop_df_sorted['Crop'], crop_df_sorted['Count'], 
                          color='#e74c3c', edgecolor='black', linewidth=1.5)
            ax.set_xlabel('Number of Records', fontsize=12, fontweight='bold')
            ax.set_title('Data Records by Crop - Thanjavur Region', fontsize=14, fontweight='bold')
            
            for bar, val in zip(bars, crop_df_sorted['Count']):
                ax.text(val, bar.get_y() + bar.get_height()/2., f'{int(val)}',
                       ha='left', va='center', fontweight='bold', fontsize=10)
            
            plt.tight_layout()
            plt.savefig('crop_records_count.png', dpi=300, bbox_inches='tight')
            print("✓ Saved: crop_records_count.png")
            plt.close()
    
    def generate_summary_report(self):
        """Generate comprehensive summary report"""
        print("\n" + "=" * 80)
        print("COMPREHENSIVE SUMMARY REPORT - THANJAVUR REGION")
        print("=" * 80)
        
        report = []
        
        print("\n📋 EXECUTIVE SUMMARY:")
        print("-" * 80)
        
        if self.soil_data is not None:
            print(f"\n✓ SOIL DATA:")
            print(f"   • Total blocks analyzed: {self.soil_data['Block'].nunique()}")
            print(f"   • Records: {len(self.soil_data)}")
            
            # Key soil findings
            n_deficiency = self.soil_data['n_Low'].mean()
            p_deficiency = self.soil_data['p_Low'].mean()
            k_deficiency = self.soil_data['k_Low'].mean()
            
            print(f"\n   NUTRIENT DEFICIENCY RATES:")
            print(f"   • Nitrogen deficit: {n_deficiency:.1f}% of soil")
            print(f"   • Phosphorus deficit: {p_deficiency:.1f}% of soil")
            print(f"   • Potassium deficit: {k_deficiency:.1f}% of soil")
            
            print(f"\n   pH PROFILE:")
            if self.soil_data['pH_Neutral'].mean() > 50:
                print(f"   • Soil is predominantly NEUTRAL (ideal for most crops)")
            elif self.soil_data['pH_Alkaline'].mean() > 50:
                print(f"   • Soil is predominantly ALKALINE (suitable for salt-tolerant crops)")
            else:
                print(f"   • Soil is predominantly ACIDIC (requires lime amendment)")
        
        print(f"\n✓ CROP DATA:")
        print(f"   • Crops with price data: {len(self.crop_data)}")
        print(f"   • Total price records: {sum(len(df) for df in self.crop_data.values())}")
        
        if self.crop_data:
            # Find highest and lowest average price crops
            crop_prices = []
            for crop_name, df in self.crop_data.items():
                price_cols = [col for col in ['Modal Price (Rs./Quintal)', 'Max Price (Rs./Quintal)'] 
                            if col in df.columns]
                if price_cols:
                    avg_price = df[price_cols[0]].mean()
                    crop_prices.append((crop_name, avg_price))
            
            if crop_prices:
                crop_prices_sorted = sorted(crop_prices, key=lambda x: x[1], reverse=True)
                print(f"\n   🔝 HIGHEST PRICED CROPS:")
                for i, (crop, price) in enumerate(crop_prices_sorted[:3], 1):
                    print(f"      {i}. {crop}: ₹{price:.2f}/Quintal")
                
                print(f"\n   💰 LOWEST PRICED CROPS:")
                for i, (crop, price) in enumerate(crop_prices_sorted[-3:], 1):
                    print(f"      {i}. {crop}: ₹{price:.2f}/Quintal")
        
        print("\n" + "=" * 80)
        print("✓ Analysis complete! Check generated PNG files for visualizations.")
        print("=" * 80)


def main():
    """Main execution function"""
    analyzer = ThanjavurAnalysis()
    
    # Load data
    analyzer.load_soil_data()
    analyzer.load_crop_price_data()
    
    # Perform analysis
    analyzer.analyze_soil_data()
    analyzer.analyze_crop_prices()
    
    # Generate visualizations
    analyzer.generate_soil_visualizations()
    analyzer.generate_crop_price_visualizations()
    
    # Summary report
    analyzer.generate_summary_report()


if __name__ == "__main__":
    main()
