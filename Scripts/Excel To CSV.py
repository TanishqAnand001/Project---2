import os
import glob
import pandas as pd
from pathlib import Path


def convert_xlsx_to_csv(xlsx_path: str, output_dir: str = None, encoding: str = "utf-8") -> list[str]:
    """
    Convert a single XLSX file (all sheets) to CSV file(s).

    Args:
        xlsx_path   : Path to the .xlsx file.
        output_dir  : Directory to save CSV(s). Defaults to the same folder as the XLSX.
        encoding    : CSV encoding (default utf-8).

    Returns:
        List of paths to the generated CSV files.
    """
    xlsx_path = str(Path(xlsx_path).resolve())
    if not xlsx_path.exists():
        raise FileNotFoundError(f"File not found: {xlsx_path}")

    output_dir = Path(output_dir).resolve() if output_dir else xlsx_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    xl = pd.ExcelFile(xlsx_path)
    sheet_names = xl.sheet_names
    generated = []

    for sheet in sheet_names:
        df = xl.parse(sheet)

        # Build output filename
        if len(sheet_names) == 1:
            csv_name = f"{xlsx_path.stem}.csv"
        else:
            safe_sheet = sheet.replace("/", "-").replace("\\", "-").replace(":", "-")
            csv_name = f"{xlsx_path.stem}_{safe_sheet}.csv"

        csv_path = Path(output_dir) / csv_name
        df.to_csv(csv_path, index=False, encoding=encoding)
        generated.append(str(csv_path))
        print(f"  ✔  {xlsx_path.name}  →  Sheet '{sheet}'  →  {csv_path}")

    return generated


def convert_folder(folder_path: str, output_dir: str = None,
                   recursive: bool = False, encoding: str = "utf-8") -> list[str]:
    """
    Convert all XLSX files inside a folder to CSV.

    Args:
        folder_path : Path to the folder containing XLSX files.
        output_dir  : Directory to save CSVs. Defaults to same folder as each XLSX.
        recursive   : If True, search sub-folders as well.
        encoding    : CSV encoding (default utf-8).

    Returns:
        List of all generated CSV file paths.
    """
    folder_path = Path(folder_path).resolve()
    pattern = str(folder_path / ("**/*.xlsx" if recursive else "*.xlsx"))
    xlsx_files = glob.glob(pattern, recursive=recursive)

    if not xlsx_files:
        print(f"No XLSX files found in: {folder_path}")
        return []

    all_generated = []
    for xlsx_file in xlsx_files:
        # If a global output_dir is given use it, otherwise put CSV next to the XLSX
        dest = output_dir if output_dir else None
        try:
            generated = convert_xlsx_to_csv(xlsx_file, output_dir=dest, encoding=encoding)
            all_generated.extend(generated)
        except Exception as exc:
            print(f"  ✘  Failed to convert {xlsx_file}: {exc}")

    return all_generated


# ──────────────────────────────────────────────────────────────────────────────
# Interactive CLI
# ──────────────────────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("        XLSX  →  CSV  Converter")
    print("=" * 60)
    print("\nConversion modes:")
    print("  1. Convert a single XLSX file")
    print("  2. Convert all XLSX files in a folder")
    print("  3. Convert all XLSX files in this project's Data folder")
    print()

    mode = input("Select mode (1 / 2 / 3): ").strip()

    # Optional: custom output directory
    out_input = input("\nOutput directory (leave blank = same as source): ").strip()
    output_dir = out_input if out_input else None

    encoding = input("CSV encoding (leave blank for utf-8): ").strip() or "utf-8"

    print()

    if mode == "1":
        xlsx_path = input("Enter the full path to the XLSX file: ").strip().strip('"')
        convert_xlsx_to_csv(xlsx_path, output_dir=output_dir, encoding=encoding)

    elif mode == "2":
        folder_path = input("Enter the full path to the folder: ").strip().strip('"')
        recursive = input("Include sub-folders? (y/n, default n): ").strip().lower() == "y"
        results = convert_folder(folder_path, output_dir=output_dir,
                                 recursive=recursive, encoding=encoding)
        print(f"\nTotal files created: {len(results)}")

    elif mode == "3":
        # Automatically target the project's Excel Format folder
        project_root = Path(__file__).resolve().parent
        data_folder = project_root / "Data" / "Soil Data ( District Wise)" / "Excel Format"
        print(f"Targeting: {data_folder}\n")
        results = convert_folder(str(data_folder), output_dir=output_dir,
                                 recursive=False, encoding=encoding)
        print(f"\nTotal files created: {len(results)}")

    else:
        print("Invalid selection. Please run the script again and choose 1, 2, or 3.")
        return

    print("\nDone! ✔")


if __name__ == "__main__":
    main()
