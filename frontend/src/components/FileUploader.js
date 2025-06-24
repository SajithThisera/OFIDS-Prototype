import { Button, Box } from "@mui/material";
import UploadIcon from "@mui/icons-material/Upload";
import React from "react";

export default function FileUploader({ onFilesSelected, uploading }) {
  const handleChange = (e) => {
    onFilesSelected(e.target.files);
    e.target.value = "";
  };
  return (
    <Box my={2}>
      <Button
        variant="contained"
        component="label"
        startIcon={<UploadIcon />}
        disabled={uploading}
      >
        Upload Video(s)
        <input type="file" hidden multiple accept="video/*" onChange={handleChange} />
      </Button>
    </Box>
  );
}
