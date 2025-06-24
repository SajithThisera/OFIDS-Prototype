import { List, ListItem, ListItemIcon, ListItemText, Paper, Typography } from "@mui/material";
import VideoLibraryIcon from "@mui/icons-material/VideoLibrary";
import React from "react";

export default function FileList({ files }) {
  if (!files.length) return null;
  return (
    <Paper variant="outlined" sx={{ my: 2, p: 2 }}>
      <Typography variant="subtitle1" gutterBottom>Uploaded Files</Typography>
      <List>
        {files.map((name, i) => (
          <ListItem key={i}>
            <ListItemIcon>
              <VideoLibraryIcon />
            </ListItemIcon>
            <ListItemText primary={name} />
          </ListItem>
        ))}
      </List>
    </Paper>
  );
}
