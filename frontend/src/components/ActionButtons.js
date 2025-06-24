import { Stack, Button } from "@mui/material";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import VisibilityIcon from "@mui/icons-material/Visibility";
import React from "react";

export default function ActionButtons({ onTrain, onXAI, disabled }) {
  return (
    <Stack direction="row" spacing={2} my={2}>
      <Button
        variant="contained"
        color="primary"
        onClick={onTrain}
        disabled={disabled}
        startIcon={<PlayArrowIcon />}
      >
        Model Training
      </Button>
      <Button
        variant="outlined"
        color="secondary"
        onClick={onXAI}
        disabled={disabled}
        startIcon={<VisibilityIcon />}
      >
        XAI Generation
      </Button>
    </Stack>
  );
}
