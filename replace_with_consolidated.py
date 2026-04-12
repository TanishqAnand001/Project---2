"""
Remove Fragmented Crop CSV Files and Replace with Consolidated Versions
=========================================================================
Deletes split/fragmented crop files and replaces them with consolidated versions.
For example: Removes Paddy-2015-2019.csv, Paddy-2019-2022.csv, Paddy-2022-2025.csv
            and replaces with single Paddy.csv
"""

import shutil
from pathlib import Path
import os

# ============================================================================
# 1. SETUP
# ============================================================================
original_path = Path(r'c:\Users\tanis\Documents\Project 2\Project---2\Data\3_Cleaned CSVs')
consolidated_path = Path(r'c:\Users\tanis\Documents\Project 2\Project---2\Data\3_Cleaned CSVs\Consolidated')

print("="*80)
print("REPLACING FRAGMENTED FILES WITH CONSOLIDATED VERSIONS")
print("="*80)

# ============================================================================
# 2. IDENTIFY FRAGMENTED FILES
# ============================================================================
print("\nSTEP 1: IDENTIFYING FRAGMENTED FILES TO REMOVE")
print("-" * 80)

year_patterns = ['-2015-2019', '-2019-2022', '-2022-2025', '-2024-2025', '-2025', '-2024', '-2022', '-2019', '-2015']
fragmented_files = []

# Find all fragmented files in original directory
for csv_file in original_path.glob('*.csv'):
    filename = csv_file.name
    for year_pattern in year_patterns:
        if year_pattern in filename:
            fragmented_files.append(csv_file)
            break

print(f"\n✓ Found {len(fragmented_files)} fragmented files to remove:")
for f in sorted(fragmented_files):
    print(f"   • {f.name}")

# ============================================================================
# 3. COPY CONSOLIDATED FILES TO ORIGINAL LOCATION
# ============================================================================
print("\n" + "="*80)
print("STEP 2: COPYING CONSOLIDATED FILES")
print("-" * 80)

consolidated_files = list(consolidated_path.glob('*.csv'))
print(f"\n✓ Found {len(consolidated_files)} consolidated files to copy:")

copied_count = 0
for consolidated_file in sorted(consolidated_files):
    try:
        destination = original_path / consolidated_file.name
        shutil.copy2(consolidated_file, destination)
        print(f"   ✓ {consolidated_file.name}")
        copied_count += 1
    except Exception as e:
        print(f"   ✗ Error copying {consolidated_file.name}: {str(e)}")

print(f"\n✅ Copied {copied_count} consolidated files to {original_path.name}")

# ============================================================================
# 4. DELETE FRAGMENTED FILES
# ============================================================================
print("\n" + "="*80)
print("STEP 3: DELETING FRAGMENTED FILES")
print("-" * 80)

deleted_count = 0
for fragmented_file in sorted(fragmented_files):
    try:
        os.remove(fragmented_file)
        print(f"   ✓ Deleted {fragmented_file.name}")
        deleted_count += 1
    except Exception as e:
        print(f"   ✗ Error deleting {fragmented_file.name}: {str(e)}")

print(f"\n✅ Deleted {deleted_count} fragmented files")

# ============================================================================
# 5. SUMMARY AND VERIFICATION
# ============================================================================
print("\n" + "="*80)
print("STEP 4: VERIFICATION")
print("-" * 80)

remaining_files = list(original_path.glob('*.csv'))
print(f"\n📊 FINAL SUMMARY:")
print(f"   • Fragmented files removed: {deleted_count}")
print(f"   • Consolidated files copied: {copied_count}")
print(f"   • Total CSV files remaining: {len(remaining_files)}")

# Verify no fragmented files remain
fragmented_remaining = []
for csv_file in remaining_files:
    filename = csv_file.name
    for year_pattern in year_patterns:
        if year_pattern in filename:
            fragmented_remaining.append(csv_file)
            break

if fragmented_remaining:
    print(f"\n⚠️  WARNING: {len(fragmented_remaining)} fragmented files still exist:")
    for f in fragmented_remaining:
        print(f"      • {f.name}")
else:
    print(f"\n✅ VERIFICATION PASSED: No fragmented files remaining!")

# ============================================================================
# 6. LIST FINAL FILES
# ============================================================================
print("\n" + "="*80)
print("FINAL CSV FILES IN ORIGINAL DIRECTORY")
print("="*80)

final_files = sorted(original_path.glob('*.csv'))
print(f"\nTotal: {len(final_files)} files\n")

for i, file in enumerate(final_files, 1):
    size_mb = file.stat().st_size / (1024 * 1024)
    print(f"{i:2d}. {file.name:30s} - {size_mb:8.2f} MB")

# ============================================================================
# 7. CHECK CONSOLIDATED DIRECTORY
# ============================================================================
print("\n" + "="*80)
print("CONSOLIDATED DIRECTORY (BACKUP)")
print("="*80)
print(f"\n📁 Location: {consolidated_path}")
print(f"✅ All consolidated files are backed up in this directory")
print(f"   Total files: {len(list(consolidated_path.glob('*.csv')))}")

print("\n" + "="*80)
print("✨ CLEANUP COMPLETE! Your CSV files are now consolidated.")
print("="*80 + "\n")
