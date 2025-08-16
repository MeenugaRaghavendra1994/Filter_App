import React, { useState } from "react";
import axios from "axios";
import { motion } from "framer-motion";
import "./App.css";

function App() {
  const [dataFile, setDataFile] = useState(null);
  const [skuFile, setSkuFile] = useState(null);
  const [progress, setProgress] = useState(0);
  const [loading, setLoading] = useState(false);
  const [downloadUrl, setDownloadUrl] = useState(null);

  const handleSubmit = async () => {
    if (!dataFile || !skuFile) {
      alert("Please upload both files!");
      return;
    }

    setLoading(true);
    setProgress(10); // Start with 10%

    const formData = new FormData();
    formData.append("data_file", dataFile);
    formData.append("sku_file", skuFile);

    try {
      const response = await axios.post("http://localhost:8000/filter-excel/", formData, {
        responseType: "blob",
        headers: { "Content-Type": "multipart/form-data" },
        onUploadProgress: (progressEvent) => {
          if (progressEvent.total) {
            let percent = Math.round((progressEvent.loaded * 100) / progressEvent.total);
            setProgress(Math.min(percent, 95)); // max 95% until backend finishes
          }
        }
      });

      // When backend finishes, mark 100%
      setProgress(100);

      const url = window.URL.createObjectURL(new Blob([response.data]));
      setDownloadUrl(url);
    } catch (error) {
      alert("Error uploading files!");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <motion.div
        className="card"
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="title">📊 Excel SKU Filter</h1>

        <div className="file-input">
          <label>Data File (Excel / ZIP)</label>
          <input type="file" onChange={(e) => setDataFile(e.target.files[0])} />
        </div>

        <div className="file-input">
          <label>SKU File (Excel)</label>
          <input type="file" onChange={(e) => setSkuFile(e.target.files[0])} />
        </div>

        <button className="upload-btn" onClick={handleSubmit} disabled={loading}>
          {loading ? "Processing..." : "🚀 Upload & Filter"}
        </button>

        {loading && (
          <div className="progress-container">
            <div className="progress-bar" style={{ width: `${progress}%` }} />
            <p>{progress}%</p>
          </div>
        )}

        {downloadUrl && (
          <a className="download-link" href={downloadUrl} download="Filtered_Result.xlsx">
            ⬇️ Download Result
          </a>
        )}
      </motion.div>
    </div>
  );
}

export default App;
