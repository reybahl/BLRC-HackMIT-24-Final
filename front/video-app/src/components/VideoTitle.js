import React from 'react';
import { Typography, Box } from '@mui/material';

const VideoTitle = ({ title, description }) => (
  <Box sx={{ mb: 2 }}>
    <Typography variant="h4" gutterBottom>
      {title}
    </Typography>
    <Typography variant="body1" paragraph>
      {description}
    </Typography>
  </Box>
);

export default VideoTitle;
