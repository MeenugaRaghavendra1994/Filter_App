import os
import io
import zipfile
import traceback
import pandas as pd
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

app = FastAPI()

# Enable CORS so React frontend can call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend at http://localhost:3000
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/filter-excel/")
async def filter_excel(data_file: UploadFile = File(...), sku_file: UploadFile = File(...)):
    try:
        # === Load SKU List ===
        sku_df = pd.read_excel(sku_file.file, engine="openpyxl")
        if "SKU Code" not in [c.strip() for c in sku_df.columns]:
            return JSONResponse(
                status_code=400,
                content={"error": f"'SKU Code' column not found in SKU file. Found: {list(sku_df.columns)}"}
            )
        sku_list = sku_df["SKU Code"].dropna().astype(str).str.strip().str.upper().tolist()

        # === Load Data File(s) ===
        dfs = []

        # If ZIP file uploaded
        if data_file.filename.endswith(".zip"):
            with zipfile.ZipFile(io.BytesIO(await data_file.read())) as z:
                for name in z.namelist():
                    if name.endswith(".xlsx") or name.endswith(".xls"):
                        with z.open(name) as f:
                            try:
                                xls = pd.ExcelFile(f, engine="openpyxl")
                                for sh in xls.sheet_names:
                                    df = pd.read_excel(xls, sheet_name=sh)
                                    df.columns = [str(c).strip() for c in df.columns]
                                    df["__file__"] = os.path.basename(name)
                                    df["__sheet__"] = sh
                                    dfs.append(df)
                            except Exception as e:
                                print(f"⚠️ Skipping {name}: {e}")

        # If single Excel file uploaded
        elif data_file.filename.endswith((".xlsx", ".xls")):
            xls = pd.ExcelFile(data_file.file, engine="openpyxl")
            for sh in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=sh)
                df.columns = [str(c).strip() for c in df.columns]
                df["__file__"] = os.path.basename(data_file.filename)
                df["__sheet__"] = sh
                dfs.append(df)
        else:
            return JSONResponse(status_code=400, content={"error": "Unsupported file format. Upload Excel or ZIP."})

        if not dfs:
            return JSONResponse(status_code=400, content={"error": "No valid Excel sheets found."})

        data = pd.concat(dfs, ignore_index=True)

        # === Apply Filter ===
        colnames = [c.strip().lower() for c in data.columns]
        if "sku code" not in colnames:
            return JSONResponse(
                status_code=400,
                content={"error": f"'SKU Code' column not found in data file. Available columns: {list(data.columns)}"}
            )

        sku_colname = data.columns[colnames.index("sku code")]
        data["__sku_str__"] = data[sku_colname].astype(str).str.strip().str.upper()

        filtered = data[data["__sku_str__"].isin(sku_list)]

        # Debugging logs
        print(f"🔍 SKU List count: {len(sku_list)}")
        print(f"🔍 Data rows: {len(data)}")
        print(f"🔍 Filtered rows: {len(filtered)}")

        if filtered.empty:
            return JSONResponse(status_code=200, content={"message": "No matching rows found for given SKU list."})

        # === Save Result File ===
        output_path = "Filtered_Result.xlsx"
        filtered.to_excel(output_path, index=False)

        return FileResponse(output_path, filename="Filtered_Result.xlsx")

    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        return JSONResponse(status_code=500, content={"error": str(e)})
