import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link as RouterLink } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import CssBaseline from '@mui/material/CssBaseline';
import LandingPage from './pages/LandingPage';
import VideoPage from './pages/VideoPage';
import HomeScreen from './pages/HomeScreen';
import 'video.js/dist/video-js.css';

const theme = createTheme({
  palette: {
    primary: {
      main: '#4c00ff', // Adjust this to match your landing page gradient
    },
    secondary: {
      main: '#00e1ff', // Adjust this to match your landing page gradient
    },
  },
});

const App = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Box sx={{ flexGrow: 1 }}>
          <AppBar position="fixed" color="transparent" elevation={0}>
            <Toolbar>
              <Typography variant="h6" component={RouterLink} to="/" sx={{ flexGrow: 1, textDecoration: 'none', color: 'inherit' }}>
                Interactive Learning
              </Typography>
              <Button color="inherit" component={RouterLink} to="/">
                Home
              </Button>
              <Button color="inherit" component={RouterLink} to="/upload">
                Upload
              </Button>
            </Toolbar>
          </AppBar>
          <Toolbar /> {/* This empty Toolbar acts as a spacer */}
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/upload" element={<HomeScreen />} />
            <Route path="/video/:videoId" element={<VideoPage />} />
          </Routes>
        </Box>
      </Router>
    </ThemeProvider>
  );
};

export default App;
