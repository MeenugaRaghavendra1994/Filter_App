import pandas as pd
import os
import math
from typing import List, Union


EXCEL_MAX_ROWS = 1_048_576  # Excel's per-sheet row limit


def filter_excels(
    source_files: List[str],
    sku_file: str,
    output_file: str,
    sku_column: str = "SKU Code",
    sku_list_column: str = "SKU Code",
) -> str:
    """
    Filters Excel files based on SKU list and writes output to Excel.
    
    Args:
        source_files (List[str]): List of Excel file paths to filter.
        sku_file (str): Path to SKU Excel file.
        output_file (str): Path to save the filtered result.
        sku_column (str): Column in source files containing SKU codes.
        sku_list_column (str): Column in SKU file containing valid SKU codes.

    Returns:
        str: Path to the saved output file.
    """

    # ===== LOAD SKU LIST =====
    sku_df = pd.read_excel(sku_file, engine="openpyxl")
    if sku_list_column not in sku_df.columns:
        raise ValueError(f"Column '{sku_list_column}' not found in SKU file")

    sku_values = sku_df[sku_list_column].dropna().astype(str).str.strip().tolist()
    if not sku_values:
        raise ValueError("No SKUs found in SKU list file.")

    # ===== LOAD ALL FILES & SHEETS =====
    frames = []
    for path in source_files:
        if not path.lower().endswith(".xlsx"):
            continue
        try:
            xls = pd.ExcelFile(path, engine="openpyxl")
            for sh in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=sh, engine="openpyxl")
                df.columns = [str(c).strip() for c in df.columns]
                df["__file__"] = os.path.basename(path)
                df["__sheet__"] = sh
                frames.append(df)
            xls.close()  # Explicitly close the file to prevent Windows lock
        except Exception as e:
            print(f"Skipping {path}: {e}")

    if not frames:
        raise ValueError("No sheets could be read from source files.")

    data = pd.concat(frames, ignore_index=True)

    # ===== APPLY FILTER =====
    if sku_column not in data.columns:
        raise ValueError(f"Column '{sku_column}' not found in source files. "
                         f"Available columns: {list(data.columns)}")

    filtered = data[data[sku_column].astype(str).str.strip().isin(sku_values)]

    # ===== SAVE TO MULTIPLE SHEETS =====
    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        total_rows = len(filtered)
        sheet_count = math.ceil(total_rows / EXCEL_MAX_ROWS)

        for i in range(sheet_count):
            start_row = i * EXCEL_MAX_ROWS
            end_row = min(start_row + EXCEL_MAX_ROWS, total_rows)
            sheet_df = filtered.iloc[start_row:end_row]
            sheet_name = f"Sheet{i+1}"
            sheet_df.to_excel(writer, index=False, sheet_name=sheet_name)

    return output_file


if __name__ == "__main__":
    import glob

    source_folder = r"D:\K12\24-25 Item Wise Data Eduvate"
    sku_file = r"D:\K12\Python Result Sheet\SKU List.xlsx"
    output_file = r"D:\K12\Python Result Sheet\Python Result Sheet.xlsx"

    all_files = glob.glob(os.path.join(source_folder, "*.xlsx"))

    result = filter_excels(
        source_files=all_files,
        sku_file=sku_file,
        output_file=output_file,
        sku_column="SKU Code",
        sku_list_column="SKU Code"
    )

    print(f"✅ Filtered data saved to: {result}")
