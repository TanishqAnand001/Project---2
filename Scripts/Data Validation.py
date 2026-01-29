import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime


class AgriculturalDataValidator:
    def __init__(self, data):
        """
        Initialize the validator with agricultural data

        Parameters:
        data: DataFrame or file path to CSV
        """
        if isinstance(data, str):
            self.df = pd.read_csv(data, header=None)
        else:
            self.df = data

        # Define column names
        self.columns = [
            'district', 'year', 'season', 'N', 'P', 'K', 'pH', 'EC', 'OC', 'S', 'Zn',
            'Fe', 'Cu', 'Mn', 'B', 'temp', 'max_temp', 'min_temp', 'humidity',
            'rainfall', 'crop', 'yield'
        ]
        self.df.columns = self.columns

        # Define expected ranges
        self.ranges = {
            'N': (0, 500), 'P': (0, 200), 'K': (0, 500),
            'pH': (3, 10), 'EC': (0, 5), 'OC': (0, 5),
            'S': (0, 50), 'Zn': (0, 10), 'Fe': (0, 10),
            'Cu': (0, 5), 'Mn': (0, 10), 'B': (0, 20),
            'temp': (15, 45), 'max_temp': (20, 50), 'min_temp': (10, 35),
            'humidity': (20, 100), 'rainfall': (0, 5000), 'yield': (0, 200)
        }

        self.validation_results = {}

    def check_missing_values(self):
        """Check for missing values in the dataset"""
        missing = self.df.isnull().sum()
        missing_pct = (missing / len(self.df)) * 100

        self.validation_results['missing_values'] = {
            'count': missing[missing > 0],
            'percentage': missing_pct[missing_pct > 0]
        }

        print("=" * 60)
        print("MISSING VALUES ANALYSIS")
        print("=" * 60)
        if missing.sum() == 0:
            print("✓ No missing values found")
        else:
            print(f"Total missing values: {missing.sum()}")
            print("\nMissing values by column:")
            for col in missing[missing > 0].index:
                print(f"  {col}: {missing[col]} ({missing_pct[col]:.2f}%)")
        print()

    def check_duplicates(self):
        """Check for duplicate rows"""
        duplicates = self.df.duplicated().sum()
        duplicate_rows = self.df[self.df.duplicated(keep=False)]

        self.validation_results['duplicates'] = {
            'count': duplicates,
            'rows': duplicate_rows
        }

        print("=" * 60)
        print("DUPLICATE ROWS ANALYSIS")
        print("=" * 60)
        if duplicates == 0:
            print("✓ No duplicate rows found")
        else:
            print(f"✗ Found {duplicates} duplicate rows")
            print("\nSample duplicates:")
            print(duplicate_rows.head(10))
        print()

    def check_value_ranges(self):
        """Check if values are within expected ranges"""
        print("=" * 60)
        print("VALUE RANGE VALIDATION")
        print("=" * 60)

        out_of_range = {}

        for col, (min_val, max_val) in self.ranges.items():
            below_min = self.df[self.df[col] < min_val]
            above_max = self.df[self.df[col] > max_val]

            if len(below_min) > 0 or len(above_max) > 0:
                out_of_range[col] = {
                    'below_min': len(below_min),
                    'above_max': len(above_max),
                    'expected_range': (min_val, max_val),
                    'actual_range': (self.df[col].min(), self.df[col].max())
                }
                print(f"\n✗ {col}:")
                print(f"  Expected: [{min_val}, {max_val}]")
                print(f"  Actual: [{self.df[col].min()}, {self.df[col].max()}]")
                if len(below_min) > 0:
                    print(f"  Below minimum: {len(below_min)} values")
                if len(above_max) > 0:
                    print(f"  Above maximum: {len(above_max)} values")
            else:
                print(f"✓ {col}: All values within range [{min_val}, {max_val}]")

        self.validation_results['out_of_range'] = out_of_range
        print()

    def check_categorical_values(self):
        """Check categorical columns for unexpected values"""
        print("=" * 60)
        print("CATEGORICAL VALUES VALIDATION")
        print("=" * 60)

        # Expected values
        expected_districts = ['Tuticorin', 'Vellore', 'Villupuram', 'Virudhunagar']
        expected_seasons = ['Kharif', 'Rabi', 'Summer']
        expected_years = list(range(2020, 2026))

        # Check districts
        unique_districts = self.df['district'].unique()
        unexpected_districts = set(unique_districts) - set(expected_districts)

        print(f"\nDistricts:")
        print(f"  Expected: {expected_districts}")
        print(f"  Found: {list(unique_districts)}")
        if unexpected_districts:
            print(f"  ✗ Unexpected: {list(unexpected_districts)}")
        else:
            print(f"  ✓ All districts valid")

        # Check seasons
        unique_seasons = self.df['season'].unique()
        unexpected_seasons = set(unique_seasons) - set(expected_seasons)

        print(f"\nSeasons:")
        print(f"  Expected: {expected_seasons}")
        print(f"  Found: {list(unique_seasons)}")
        if unexpected_seasons:
            print(f"  ✗ Unexpected: {list(unexpected_seasons)}")
        else:
            print(f"  ✓ All seasons valid")

        # Check years
        unique_years = self.df['year'].unique()
        unexpected_years = set(unique_years) - set(expected_years)

        print(f"\nYears:")
        print(f"  Expected: {expected_years}")
        print(f"  Found: {sorted(unique_years)}")
        if unexpected_years:
            print(f"  ✗ Unexpected: {list(unexpected_years)}")
        else:
            print(f"  ✓ All years valid")

        # Check crops
        print(f"\nCrops found: {sorted(self.df['crop'].unique())}")
        print(f"  Total unique crops: {self.df['crop'].nunique()}")

        print()

    def check_logical_consistency(self):
        """Check for logical inconsistencies"""
        print("=" * 60)
        print("LOGICAL CONSISTENCY CHECKS")
        print("=" * 60)

        issues = []

        # Check: max_temp >= temp >= min_temp
        temp_issues = self.df[
            (self.df['max_temp'] < self.df['temp']) |
            (self.df['min_temp'] > self.df['temp']) |
            (self.df['max_temp'] < self.df['min_temp'])
            ]

        if len(temp_issues) > 0:
            issues.append(f"Temperature inconsistency: {len(temp_issues)} rows")
            print(f"✗ Temperature inconsistency found in {len(temp_issues)} rows")
        else:
            print("✓ Temperature values are logically consistent")

        # Check: NPK values
        npk_zero = self.df[(self.df['N'] == 0) | (self.df['P'] == 0) | (self.df['K'] == 0)]
        if len(npk_zero) > 0:
            issues.append(f"Zero NPK values: {len(npk_zero)} rows")
            print(f"⚠ Warning: {len(npk_zero)} rows have zero NPK values")
        else:
            print("✓ All NPK values are non-zero")

        # Check: Yield values
        zero_yield = self.df[self.df['yield'] == 0]
        if len(zero_yield) > 0:
            issues.append(f"Zero yield: {len(zero_yield)} rows")
            print(f"⚠ Warning: {len(zero_yield)} rows have zero yield")
        else:
            print("✓ All yield values are non-zero")

        self.validation_results['logical_issues'] = issues
        print()

    def generate_summary_statistics(self):
        """Generate summary statistics"""
        print("=" * 60)
        print("SUMMARY STATISTICS")
        print("=" * 60)

        print(f"\nDataset shape: {self.df.shape}")
        print(f"Total records: {len(self.df)}")
        print(f"Time period: {self.df['year'].min()} - {self.df['year'].max()}")
        print(f"Districts: {self.df['district'].nunique()}")
        print(f"Crops: {self.df['crop'].nunique()}")

        print("\nNumerical columns statistics:")
        print(self.df[['N', 'P', 'K', 'pH', 'temp', 'humidity', 'rainfall', 'yield']].describe())

        print("\nRecords per district:")
        print(self.df['district'].value_counts())

        print("\nRecords per season:")
        print(self.df['season'].value_counts())

        print("\nRecords per crop:")
        print(self.df['crop'].value_counts())
        print()

    def visualize_data_quality(self):
        """Create visualizations for data quality"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))

        # Plot 1: Missing values
        missing = self.df.isnull().sum()
        if missing.sum() > 0:
            missing[missing > 0].plot(kind='bar', ax=axes[0, 0], color='red')
            axes[0, 0].set_title('Missing Values by Column')
            axes[0, 0].set_ylabel('Count')
        else:
            axes[0, 0].text(0.5, 0.5, 'No Missing Values',
                            ha='center', va='center', fontsize=14)
            axes[0, 0].set_title('Missing Values')

        # Plot 2: Distribution of yields
        self.df['yield'].hist(bins=30, ax=axes[0, 1], edgecolor='black')
        axes[0, 1].set_title('Distribution of Crop Yields')
        axes[0, 1].set_xlabel('Yield')
        axes[0, 1].set_ylabel('Frequency')

        # Plot 3: Records per district
        self.df['district'].value_counts().plot(kind='bar', ax=axes[1, 0], color='skyblue')
        axes[1, 0].set_title('Records per District')
        axes[1, 0].set_ylabel('Count')
        axes[1, 0].tick_params(axis='x', rotation=45)

        # Plot 4: Records per crop
        self.df['crop'].value_counts().plot(kind='bar', ax=axes[1, 1], color='lightgreen')
        axes[1, 1].set_title('Records per Crop')
        axes[1, 1].set_ylabel('Count')
        axes[1, 1].tick_params(axis='x', rotation=45)

        plt.tight_layout()
        plt.savefig('data_quality_report.png', dpi=300, bbox_inches='tight')
        plt.show()
        print("✓ Visualization saved as 'data_quality_report.png'")

    def run_full_validation(self):
        """Run all validation checks"""
        print("\n" + "=" * 60)
        print("AGRICULTURAL DATA VALIDATION REPORT")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60 + "\n")

        self.check_missing_values()
        self.check_duplicates()
        self.check_value_ranges()
        self.check_categorical_values()
        self.check_logical_consistency()
        self.generate_summary_statistics()

        print("=" * 60)
        print("VALIDATION COMPLETE")
        print("=" * 60)

        return self.validation_results


# Usage example
if __name__ == "__main__":
    # Load your data
    # Option 1: From CSV file
    # validator = AgriculturalDataValidator('your_data.csv')

    # Option 2: From DataFrame (paste your data here)
    from io import StringIO

    # Your data here (sample - replace with full dataset)
    data_string = """Tuticorin,2022,Rabi,131.0,32.6,123.0,7.8,0.4,0.4,20.8,1.1,0.8,1.0,4.4,5.1,26.3,37.0,20.1,77.4,644.0,pulses,80
Tuticorin,2022,Summer,131.0,32.6,123.0,7.8,0.4,0.4,20.8,1.1,0.8,1.0,4.4,5.1,29.1,37.9,22.1,69.4,168.0,rice,90"""

    # Create DataFrame
    df = pd.read_csv(StringIO(data_string), header=None)

    # Run validation
    validator = AgriculturalDataValidator("../data/tn_crop_recommendation_scored.csv")
    results = validator.run_full_validation()

    # Generate visualizations
    validator.visualize_data_quality()
