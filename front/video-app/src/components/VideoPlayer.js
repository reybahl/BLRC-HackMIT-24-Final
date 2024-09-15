import React, { useState, useRef, useEffect } from 'react';
import { Box, Typography, Modal } from '@mui/material';
import styled from '@emotion/styled';
import html2canvas from 'html2canvas';

const StyledVideo = styled('video')(({ theme }) => ({
  width: '100%',
  height: 'auto',
  borderRadius: theme.shape.borderRadius,
}));

const VideoContainer = styled(Box)({
  position: 'relative',
  width: '100%',
});

const SelectionBox = styled(Box)({
  position: 'absolute',
  border: '2px solid red',
  backgroundColor: 'rgba(255, 0, 0, 0.2)',
});

const VideoPlayer = ({ src, onTimeUpdate, setParentThumbnailImage, setParentCroppedImage }) => {
  const [isPaused, setIsPaused] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);
  const [selectionStart, setSelectionStart] = useState(null);
  const [selectionEnd, setSelectionEnd] = useState(null);
  const [isSelecting, setIsSelecting] = useState(false);
  const [croppedImage, setCroppedImage] = useState(null);
  const videoRef = useRef(null);
  const containerRef = useRef(null);

  const handlePlayPause = () => {
    const video = videoRef.current;
    if (video.paused) {
      video.play();
      setIsPaused(false);
    } else {
      video.pause();
      setIsPaused(true);
    }
  };

  const handleMouseDown = (event) => {
    if (isPaused) {
      const rect = containerRef.current.getBoundingClientRect();
      setSelectionStart({
        x: event.clientX - rect.left,
        y: event.clientY - rect.top,
      });
      setIsSelecting(true);
    }
  };

  const handleMouseMove = (event) => {
    if (isSelecting) {
      const rect = containerRef.current.getBoundingClientRect();
      setSelectionEnd({
        x: event.clientX - rect.left,
        y: event.clientY - rect.top,
      });
    }
  };

  const handleMouseUp = () => {
    if (isSelecting) {
      setIsSelecting(false);
      captureSelection();
    }
  };

  const captureCurrentFrame = () => {
    const video = videoRef.current;
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
    const frameDataUrl = canvas.toDataURL('image/png');
    setParentThumbnailImage(frameDataUrl);
  };

  // Effect to capture the current frame when the video is paused
  useEffect(() => {
    if (isPaused) {
      captureCurrentFrame();
    }
  }, [isPaused]);

  const captureSelection = async () => {
    if (!selectionStart || !selectionEnd) return;

    const video = videoRef.current;
    const container = containerRef.current;

    try {
      const canvas = await html2canvas(container, {
        useCORS: true,
        logging: false,
        videoState: { currentTime: video.currentTime },
        scale: 2,
      });

      // Set the parent thumbnail image (full frame)
      setParentThumbnailImage(canvas.toDataURL('image/png'));

      const scaleFactor = canvas.width / container.offsetWidth;

      const cropX = Math.min(selectionStart.x, selectionEnd.x) * scaleFactor;
      const cropY = Math.min(selectionStart.y, selectionEnd.y) * scaleFactor;
      const cropWidth = Math.abs(selectionEnd.x - selectionStart.x) * scaleFactor;
      const cropHeight = Math.abs(selectionEnd.y - selectionStart.y) * scaleFactor;

      // Check if the selection is larger than 100x100 pixels
      if (cropWidth < 100 || cropHeight < 100) {
        console.log("Selection is too small. Minimum size is 100x100 pixels.");
        return;
      }

      const croppedCanvas = document.createElement('canvas');
      croppedCanvas.width = cropWidth;
      croppedCanvas.height = cropHeight;
      const croppedCtx = croppedCanvas.getContext('2d');

      croppedCtx.drawImage(canvas, 
        cropX, cropY, cropWidth, cropHeight, 
        0, 0, cropWidth, cropHeight
      );

      const croppedDataUrl = croppedCanvas.toDataURL('image/png');
      setCroppedImage(croppedDataUrl);
      setParentCroppedImage(croppedDataUrl);  
      setModalOpen(true);
    } catch (error) {
      console.error("Error capturing selection:", error);
    }
  };

  const selectionStyle = {
    left: Math.min(selectionStart?.x || 0, selectionEnd?.x || 0),
    top: Math.min(selectionStart?.y || 0, selectionEnd?.y || 0),
    width: Math.abs((selectionEnd?.x || 0) - (selectionStart?.x || 0)),
    height: Math.abs((selectionEnd?.y || 0) - (selectionStart?.y || 0)),
  };

  return (
    <VideoContainer
      ref={containerRef}
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
      onMouseLeave={handleMouseUp}
    >
      <StyledVideo
        ref={videoRef}
        src={src}
        controls
        crossOrigin="anonymous"
        onTimeUpdate={onTimeUpdate}
        onPlay={() => setIsPaused(false)}
        onPause={() => {
          setIsPaused(true);
          captureCurrentFrame();
        }}
        onClick={handlePlayPause}
      />
      {isSelecting && <SelectionBox style={selectionStyle} />}
      <Modal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        aria-labelledby="cropped-image-modal"
        aria-describedby="shows the cropped region of the video"
      >
        <Box
          sx={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            bgcolor: 'background.paper',
            border: '2px solid #000',
            boxShadow: 24,
            p: 4,
            maxWidth: '90%',
            maxHeight: '90%',
            overflow: 'auto',
          }}
        >
          <Typography id="cropped-image-modal-title" variant="h6" component="h2">
            Cropped Region
          </Typography>
          {croppedImage && (
            <Box mt={2}>
              <img src={croppedImage} alt="Cropped region" style={{ maxWidth: '100%', height: 'auto' }} />
            </Box>
          )}
        </Box>
      </Modal>
    </VideoContainer>
  );
};

export default VideoPlayer;
