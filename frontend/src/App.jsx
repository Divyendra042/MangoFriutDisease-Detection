import React, { useState } from "react";

// Use Vite proxy (vite.config.mts) so frontend -> backend works reliably.
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
      setError("Please select a mango image first.");
      return;
    }

    const formData = new FormData();
    formData.append("image", selectedFile);

    try {
      setLoading(true);
      const response = await fetch(API_URL, {
        method: "POST",
        body: formData
      });

      if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.error || "Failed to get prediction from server.");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || "Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <header className="header">
        <h1>Mango Fruit Disease Detection</h1>
        <p>Upload a mango image and detect possible diseases using AI.</p>
      </header>

      <main className="container">
        <section className="card">
          <h2>Upload Mango Image</h2>
          <p className="subtitle">
            Choose a clear photo of a mango fruit. Supported formats: JPG, PNG.
          </p>

          <form onSubmit={handleSubmit} className="form">
            <label className="file-input-label">
              <span>Select Image</span>
              <input
                type="file"
                accept="image/*"
                onChange={handleFileChange}
              />
            </label>

            {previewUrl && (
              <div className="preview">
                <img src={previewUrl} alt="Selected mango" />
              </div>
            )}

            <button type="submit" className="primary-btn" disabled={loading}>
              {loading ? "Analyzing..." : "Detect Disease"}
            </button>
          </form>

          {error && <div className="alert alert-error">{error}</div>}

          {result && (
            <div className="result">
              <h3>Prediction Result</h3>
              <p className="disease-name">{result.predicted_disease}</p>

              <div className="result-grid">
                <div>
                  <h4>Disease Type</h4>
                  <p>{result.disease_type}</p>
                </div>
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
        <span>Mango Fruit Disease Detection • Flask + React</span>
      </footer>
    </div>
  );
}

