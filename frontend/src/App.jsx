import React, { useState } from "react";

const API_URL = "/detect";

export default function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    setError("");
    setResult(null);

    if (!file) {
      setSelectedFile(null);
      setPreviewUrl("");
      return;
    }

    setSelectedFile(file);
    setPreviewUrl(URL.createObjectURL(file));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setResult(null);

    if (!selectedFile) {
      setError("Please select an image first");
      return;
    }

    const formData = new FormData();
    formData.append("image", selectedFile);

    try {
      setLoading(true);

      const res = await fetch(API_URL, {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data?.error || "Server error");
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <header className="header">
        <div className="brand">
          <div className="brand-mark">M</div>
          <div className="brand-text">
            <h1>Mango Disease Detector</h1>
            <p>Upload a mango photo and get an instant diagnosis.</p>
          </div>
        </div>
      </header>

      <main className="container">
        <section className="card">

          <form onSubmit={handleSubmit} className="form">

            <div className="uploader">
              <input
                className="file-input"
                id="mango-image"
                type="file"
                accept="image/*"
                onChange={handleFileChange}
              />
              <label className="file-input-label" htmlFor="mango-image">
                <div className="file-input-title">
                  {selectedFile ? "Image selected" : "Choose an image"}
                </div>
                <div className="file-input-subtitle">
                  {selectedFile ? selectedFile.name : "JPG, PNG, WEBP"}
                </div>
              </label>

              {previewUrl && (
                <div className="preview">
                  <img src={previewUrl} alt="Selected mango" />
                </div>
              )}
            </div>

            <div className="actions">
              <button className="primary-btn" disabled={loading || !selectedFile}>
                {loading ? "Analyzing..." : "Detect"}
              </button>
              <button
                type="button"
                className="secondary-btn"
                onClick={() => {
                  setSelectedFile(null);
                  setPreviewUrl("");
                  setResult(null);
                  setError("");
                }}
                disabled={loading}
              >
                Reset
              </button>
            </div>

          </form>

          {loading && (
            <div className="loader">
              <div className="spinner"></div>
              <p>Analyzing Image...</p>
            </div>
          )}

          {error && <div className="alert alert-error">{error}</div>}

          {result && (
            <div className="result">

              <div className="result-head">
                <h3>Result</h3>
                <span
                  className={
                    result.predicted_disease === "Healthy"
                      ? "pill pill-ok"
                      : "pill pill-warn"
                  }
                >
                  {result.predicted_disease === "Healthy" ? "Healthy" : "Disease"}
                </span>
              </div>
              <p className="disease-name">{result.predicted_disease}</p>

              <div className="result-grid">

                <div>
                  <h4>Severity</h4>
                  <p>{result.severity}</p>
                </div>

                <div className="full-width">
                  <h4>Description</h4>
                  <p>{result.description}</p>
                </div>

                <div className="full-width">
                  <h4>Symptoms</h4>
                  <p>{result.symptoms}</p>
                </div>

                <div className="full-width">
                  <h4>Diagnosis</h4>
                  <p>{result.diagnosis}</p>
                </div>

                <div className="full-width">
                  <h4>Precautions</h4>
                  <p>{result.precautions}</p>
                </div>

              </div>

            </div>
          )}

        </section>
      </main>

      <footer className="footer">
        Mango Detection • AI Project
      </footer>
    </div>
  );
}