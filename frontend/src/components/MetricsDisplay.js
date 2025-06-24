import React from "react";
import { Box, Typography, Table, TableBody, TableCell, TableRow, Paper } from "@mui/material";

export default function MetricsDisplay({ metrics }) {
  if (!metrics) return null;
  const { accuracy, auc, report } = metrics;
  return (
    <Box sx={{ width: "100%", mb: 2 }}>
      <Paper sx={{ p: 2 }}>
        <Typography variant="h6">Results</Typography>
        <Typography variant="body2">Accuracy: {accuracy}</Typography>
        <Typography variant="body2">AUC: {auc}</Typography>
        <Typography variant="subtitle2" sx={{ mt: 1 }}>
          Classification Report
        </Typography>
        <Table size="small">
          <TableBody>
            {["0", "1"].map((cls) =>
              report[cls] ? (
                <TableRow key={cls}>
                  <TableCell>{cls === "0" ? "Healthy" : "Impaired"}</TableCell>
                  <TableCell>Precision: {report[cls].precision}</TableCell>
                  <TableCell>Recall: {report[cls].recall}</TableCell>
                  <TableCell>F1: {report[cls]["f1-score"]}</TableCell>
                </TableRow>
              ) : null
            )}
          </TableBody>
        </Table>
      </Paper>
    </Box>
  );
}
