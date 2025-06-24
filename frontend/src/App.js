import React, { useState } from "react";
import {
  Box,
  Button,
  Container,
  Typography,
  LinearProgress,
  Stack,
  Paper,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
} from "@mui/material";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import AutoGraphIcon from "@mui/icons-material/AutoGraph";
import VisibilityIcon from "@mui/icons-material/Visibility";
import InsertDriveFileIcon from "@mui/icons-material/InsertDriveFile";
import MetricsDisplay from "./components/MetricsDisplay";

function App() {
  const [files, setFiles] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(false);
  const [xaiResult, setXaiResult] = useState(null);
  const [uploadMsg, setUploadMsg] = useState("");
  const [modelTrained, setModelTrained] = useState(false);
  const [xaiGenerated, setXaiGenerated] = useState(false);

  // File selection
  const handleFileChange = (e) => {
    setFiles([...e.target.files]);
    setUploadMsg("");
  };

  // Upload files
  const handleUpload = async () => {
    if (!files.length) return;
    setLoading(true);
    setUploadMsg("");
    const formData = new FormData();
    files.forEach((file) => formData.append("files", file));
    try {
      const res = await fetch("/upload", {
        method: "POST",
        body: formData,
      });
      if (!res.ok) throw new Error("Upload failed");
      const data = await res.json();
      setUploadMsg(`Uploaded:\n${data.saved.join("\n")}`);
    } catch (err) {
      setUploadMsg("Upload failed. Please try again.");
    }
    setLoading(false);
  };

  // Model training
  const handleTrain = async () => {
    setLoading(true);
    setMetrics(null);
    setModelTrained(false);
    setXaiGenerated(false);
    try {
      const res = await fetch("/train", { method: "POST" });
      if (!res.ok) throw new Error("Training failed");
      const data = await res.json();
      setMetrics(data.train_metrics);
      setModelTrained(true);
    } catch (err) {
      alert("Model training failed. Check server logs.");
    }
    setLoading(false);
  };

  // XAI generation
  const handleXai = async () => {
    setLoading(true);
    setXaiResult(null);
    setXaiGenerated(false);
    try {
      const res = await fetch("/xai", { method: "POST" });
      if (!res.ok) throw new Error("XAI generation failed");
      const data = await res.json();
      setXaiResult(data.xai_result);
      setXaiGenerated(true);
    } catch (err) {
      alert("XAI generation failed.");
    }
    setLoading(false);
  };

  // List render helpers
  const renderFileList = (fileArray) => (
    <List dense>
      {fileArray.map((file, idx) => (
        <ListItem key={idx}>
          <ListItemIcon>
            <InsertDriveFileIcon fontSize="small" />
          </ListItemIcon>
          <ListItemText primary={typeof file === "string" ? file : file.name} />
        </ListItem>
      ))}
    </List>
  );

  // Only show result images if available and after relevant operations
  const FeatureImportanceImg = () =>
    modelTrained ? (
      <img
        src="/outputs/feature_importance.png"
        alt="Feature Importance"
        style={{ width: "100%", maxWidth: 400, margin: "16px 0" }}
        onError={(e) => (e.target.style.display = "none")}
      />
    ) : null;

  const ConfusionMatrixImg = () =>
    modelTrained ? (
      <img
        src="/outputs/confusion_matrix.png"
        alt="Confusion Matrix"
        style={{ width: "100%", maxWidth: 400, margin: "16px 0" }}
        onError={(e) => (e.target.style.display = "none")}
      />
    ) : null;

  return (
    <Container maxWidth="sm" sx={{ py: 4 }}>
      <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
        <Typography variant="h4" align="center" gutterBottom>
          OFIDS Prototype UI
        </Typography>
        <Box display="flex" flexDirection="column" alignItems="center">
          {/* File input */}
          <input
            type="file"
            multiple
            onChange={handleFileChange}
            style={{ display: "none" }}
            id="video-upload"
            accept="video/*"
          />
          <label htmlFor="video-upload">
            <Button
              variant="contained"
              color="primary"
              component="span"
              startIcon={<CloudUploadIcon />}
              sx={{ mb: 2 }}
              disabled={loading}
            >
              Choose Videos
            </Button>
          </label>
          {/* Show selected files */}
          {files.length > 0 && (
            <>
              <Typography variant="subtitle2" sx={{ mt: 1 }}>
                Selected files:
              </Typography>
              {renderFileList(files)}
            </>
          )}

          {/* Upload button */}
          <Button
            variant="contained"
            color="secondary"
            startIcon={<CloudUploadIcon />}
            sx={{ mb: 1, mt: 1 }}
            onClick={handleUpload}
            disabled={loading || !files.length}
          >
            Upload
          </Button>
          {/* Uploaded file list */}
          {uploadMsg && (
            <>
              <Typography variant="subtitle2" sx={{ mt: 2 }}>
                Uploaded files:
              </Typography>
              <Paper variant="outlined" sx={{ p: 1, mt: 1, mb: 2, width: "100%" }}>
                {uploadMsg.split("\n").map((line, idx) =>
                  line.trim() && !line.startsWith("Uploaded") ? (
                    <div key={idx}>{line}</div>
                  ) : null
                )}
              </Paper>
            </>
          )}
          <Divider sx={{ my: 2 }} />
          {/* Training/XAI buttons */}
          <Stack direction="row" spacing={2} sx={{ mb: 2 }}>
            <Button
              variant="contained"
              color="success"
              startIcon={<AutoGraphIcon />}
              onClick={handleTrain}
              disabled={loading}
            >
              Model Training
            </Button>
            <Button
              variant="contained"
              color="info"
              startIcon={<VisibilityIcon />}
              onClick={handleXai}
              disabled={loading}
            >
              XAI Generation
            </Button>
          </Stack>
          {loading && <LinearProgress sx={{ width: "100%", mb: 2 }} />}
          {/* Metrics display */}
          <MetricsDisplay metrics={metrics} />
          {/* Only show images after model training */}
          <FeatureImportanceImg />
          <ConfusionMatrixImg />
          {/* XAI output */}
          {xaiResult && (
            <Box mt={2}>
              <Typography variant="subtitle1">XAI Results:</Typography>
              <pre style={{ whiteSpace: "pre-wrap" }}>
                {typeof xaiResult === "string"
                  ? xaiResult
                  : JSON.stringify(xaiResult, null, 2)}
              </pre>
            </Box>
          )}
        </Box>
      </Paper>
    </Container>
  );
}

export default App;
