"""
Consolidate Split Crop CSV Files
=================================
Combines crop CSV files that are split by year ranges into single consolidated files.
For example: Paddy-2015-2019.csv + Paddy-2019-2022.csv + Paddy-2022-2025.csv → Paddy.csv
"""

import pandas as pd
import glob
from pathlib import Path
from collections import defaultdict
import os

# ============================================================================
# 1. SETUP
# ============================================================================
data_path = Path(r'c:\Users\tanis\Documents\Project 2\Project---2\Data\3_Cleaned CSVs')
output_path = Path(r'c:\Users\tanis\Documents\Project 2\Project---2\Data\3_Cleaned CSVs\Consolidated')

# Create output directory if it doesn't exist
output_path.mkdir(parents=True, exist_ok=True)

print("="*80)
print("CONSOLIDATING SPLIT CROP CSV FILES")
print("="*80)
print(f"\nInput directory: {data_path}")
print(f"Output directory: {output_path}")

# ============================================================================
# 2. IDENTIFY SPLIT FILES
# ============================================================================
print("\n" + "="*80)
print("STEP 1: IDENTIFYING SPLIT CROP FILES")
print("="*80)

# Get all CSV files
all_csv_files = glob.glob(str(data_path / '*.csv'))
print(f"\nTotal CSV files found: {len(all_csv_files)}")

# Extract base crop names and group by them
crop_groups = defaultdict(list)
year_patterns = ['-2015-2019', '-2019-2022', '-2022-2025', '-2024-2025', '-2025', '-2024', '-2022', '-2019', '-2015']

for csv_file in all_csv_files:
    filename = Path(csv_file).stem
    
    # Find the base crop name
    base_crop = filename
    for year_pattern in year_patterns:
        if year_pattern in filename:
            base_crop = filename.replace(year_pattern, '')
            break
    
    crop_groups[base_crop].append(csv_file)

# Find crops that have multiple files (split crops)
split_crops = {crop: files for crop, files in crop_groups.items() if len(files) > 1}
single_crops = {crop: files for crop, files in crop_groups.items() if len(files) == 1}

print(f"\n📊 FILE CLASSIFICATION:")
print(f"   • Split crops (multiple files): {len(split_crops)}")
print(f"   • Single crops (one file): {len(single_crops)}")

print(f"\n🔀 SPLIT CROPS TO CONSOLIDATE:")
for crop_name in sorted(split_crops.keys()):
    files = split_crops[crop_name]
    print(f"\n   {crop_name}:")
    for f in sorted(files):
        filename = Path(f).name
        print(f"      • {filename}")

# ============================================================================
# 3. CONSOLIDATE SPLIT FILES
# ============================================================================
print("\n" + "="*80)
print("STEP 2: CONSOLIDATING SPLIT FILES")
print("="*80)

consolidated_files = {}

for crop_name, file_list in sorted(split_crops.items()):
    print(f"\n🔗 Consolidating: {crop_name}")
    
    # Load and combine all files for this crop
    dfs = []
    total_records_before = 0
    
    for csv_file in sorted(file_list):
        try:
            df = pd.read_csv(csv_file)
            dfs.append(df)
            total_records_before += len(df)
            filename = Path(csv_file).name
            print(f"   ✓ Loaded {filename}: {len(df):,} records")
        except Exception as e:
            print(f"   ✗ Error loading {csv_file}: {str(e)}")
    
    # Combine all dataframes
    combined_df = pd.concat(dfs, ignore_index=True)
    print(f"   → Total before deduplication: {len(combined_df):,} records")
    
    # Remove duplicates (keep first occurrence)
    combined_df_deduplicated = combined_df.drop_duplicates()
    print(f"   → Total after deduplication: {len(combined_df_deduplicated):,} records")
    
    # Save consolidated file
    output_file = output_path / f"{crop_name}.csv"
    combined_df_deduplicated.to_csv(output_file, index=False)
    print(f"   ✅ Saved: {output_file.name}")
    
    consolidated_files[crop_name] = {
        'input_files': len(file_list),
        'total_records': len(combined_df_deduplicated),
        'duplicates_removed': len(combined_df) - len(combined_df_deduplicated),
        'output_file': output_file
    }

# ============================================================================
# 4. COPY SINGLE CROP FILES
# ============================================================================
print("\n" + "="*80)
print("STEP 3: COPYING SINGLE CROP FILES (NO CONSOLIDATION NEEDED)")
print("="*80)

for crop_name, file_list in sorted(single_crops.items()):
    csv_file = file_list[0]
    try:
        df = pd.read_csv(csv_file)
        output_file = output_path / Path(csv_file).name
        df.to_csv(output_file, index=False)
        print(f"   ✓ Copied {Path(csv_file).name}: {len(df):,} records")
    except Exception as e:
        print(f"   ✗ Error copying {csv_file}: {str(e)}")

# ============================================================================
# 5. SUMMARY REPORT
# ============================================================================
print("\n" + "="*80)
print("SUMMARY REPORT")
print("="*80)

print(f"\n✅ CONSOLIDATION COMPLETE!")
print(f"\n📊 RESULTS:")
print(f"   • Split crops consolidated: {len(consolidated_files)}")
print(f"   • Single crops copied: {len(single_crops)}")
print(f"   • Total crops in output: {len(consolidated_files) + len(single_crops)}")

print(f"\n📈 CONSOLIDATION DETAILS:")
for crop_name in sorted(consolidated_files.keys()):
    info = consolidated_files[crop_name]
    print(f"\n   {crop_name}:")
    print(f"      • Input files: {info['input_files']}")
    print(f"      • Total records: {info['total_records']:,}")
    print(f"      • Duplicates removed: {info['duplicates_removed']:,}")
    print(f"      • Output: {info['output_file'].name}")

print(f"\n💾 OUTPUT LOCATION:")
print(f"   {output_path}")

print(f"\n📁 OUTPUT FILES:")
output_files = sorted(output_path.glob('*.csv'))
for i, file in enumerate(output_files, 1):
    df = pd.read_csv(file)
    print(f"   {i:2d}. {file.name:30s} - {len(df):,} records")

print("\n" + "="*80)
print("✨ ALL CONSOLIDATED FILES READY TO USE!")
print("="*80 + "\n")
