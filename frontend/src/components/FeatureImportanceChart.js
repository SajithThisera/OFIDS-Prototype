import { Paper, Typography, Box } from "@mui/material";
import React from "react";

export default function FeatureImportanceChart({ importances }) {
  if (!importances) return null;
  return (
    <Paper variant="outlined" sx={{ my: 2, p: 2 }}>
      <Typography variant="h6" gutterBottom>Feature Importances (XAI)</Typography>
      <Box>
        <ul>
          {importances.map((imp, i) => (
            <li key={i}>Feature {i + 1}: {imp.toFixed(4)}</li>
          ))}
        </ul>
      </Box>
    </Paper>
  );
}
