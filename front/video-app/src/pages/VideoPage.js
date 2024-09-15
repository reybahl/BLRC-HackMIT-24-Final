import React, { useState, useEffect } from 'react';
import { useParams, useLocation } from 'react-router-dom';
import { Box, Grid, CircularProgress, Typography, Button, Alert } from '@mui/material';
import VideoTitle from '../components/VideoTitle';
import VideoPlayer from '../components/VideoPlayer';
import Transcript from '../components/Transcript';
import ChatBot from '../components/chatbox';

const VideoPage = () => {
  const { videoId } = useParams();
  const location = useLocation();
  const { videoSrc } = location.state || {};
  const [currentTime, setCurrentTime] = useState(0);
  const [transcriptData, setTranscriptData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [timeoutReached, setTimeoutReached] = useState(false);
  const [thumbnailImage, setThumbnailImage] = useState(null);
  const [croppedImage, setCroppedImage] = useState(null);
  console.log(videoId);

  // Mock data for title and description
  const title = "Uploaded Video";
  const description = "This is the video you just uploaded.";

  const fetchTranscriptData = async () => {
    try {
      // remove extension from videoId if it exists
      const videoIdNoExtension = videoId.replace(/\.[^/.]+$/, "");
      const response = await fetch(`/api/transcript/get/${videoIdNoExtension}`);
      if (response.ok) {
        const data = await response.json();
        setTranscriptData(data);
        setLoading(false);
        setError(null);
      } else if (response.status === 404) {
        // If 404, we'll retry in 2 seconds
        setTimeout(fetchTranscriptData, 2000);
      } else {
        throw new Error(`Failed to fetch transcript data: ${response.statusText}`);
      }
    } catch (error) {
      console.error('Error fetching transcript data:', error);
      setError(error.message);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTranscriptData();

    // Set a timeout for 30 seconds
    const timeoutId = setTimeout(() => {
      setTimeoutReached(true);
      setLoading(false);
    }, 30000);

    return () => clearTimeout(timeoutId);
  }, [videoId]);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTime(prevTime => prevTime + 0.5);
    }, 500);

    return () => clearInterval(interval);
  }, []);

  const handleTimeUpdate = (e) => {
    setCurrentTime(e.target.currentTime);
  };

  useEffect(() => {
    if (croppedImage) {
      console.log(croppedImage);
    }
  }, [croppedImage]);

  const handleRetry = () => {
    setLoading(true);
    setTimeoutReached(false);
    setError(null);
    fetchTranscriptData();
  };

  const renderTranscriptSection = () => {
    if (loading && !timeoutReached) {
      return (
        <Box display="flex" flexDirection="column" alignItems="center" justifyContent="center" height="100%">
          <CircularProgress />
          <Typography variant="body1" sx={{ mt: 2 }}>
            Waiting for results to finish...
          </Typography>
        </Box>
      );
    }

    if (error) {
      return (
        <Alert severity="error" sx={{ mt: 2 }}>
          {error}
          <Button color="inherit" size="small" onClick={handleRetry} sx={{ ml: 2 }}>
            Retry
          </Button>
        </Alert>
      );
    }

    if (timeoutReached && !transcriptData) {
      return (
        <Box display="flex" flexDirection="column" alignItems="center" justifyContent="center" height="100%">
          <Typography variant="body1" sx={{ mb: 2 }}>
            Transcript processing, please check back later.
          </Typography>
          <Button variant="contained" onClick={handleRetry}>
            Retry Now
          </Button>
        </Box>
      );
    }

    return <Transcript transcriptData={transcriptData} currentTime={currentTime} />;
  };

  return (
    <Box sx={{ pt: 8 }}>
      <Box sx={{ maxWidth: 1200, margin: 'auto', p: 2 }}>
        <VideoTitle title={title} description={description} />
        <Grid container spacing={2}>
          <Grid item xs={12} md={7}>
            <VideoPlayer src={videoSrc} onTimeUpdate={handleTimeUpdate} setParentThumbnailImage={setThumbnailImage} setParentCroppedImage={setCroppedImage} />
          </Grid>
          <Grid item xs={12} md={5}>
            {renderTranscriptSection()}
          </Grid>
        </Grid>
      </Box>
      <Box display="flex" justifyContent="center">
        <ChatBot croppedImage={croppedImage} />
      </Box>
    </Box>
    
  );
};

export default VideoPage;
