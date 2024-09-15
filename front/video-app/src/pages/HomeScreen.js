import React, { useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDropzone } from 'react-dropzone';
import { Box, Typography, CircularProgress, styled } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { motion } from 'framer-motion';

const UploadBox = styled(motion.div)(({ theme }) => ({
  padding: theme.spacing(4),
  textAlign: 'center',
  cursor: 'pointer',
  border: '2px dashed',
  borderRadius: theme.shape.borderRadius,
  transition: 'all 0.3s ease-in-out',
}));

const HomeScreen = () => {
  const [uploading, setUploading] = useState(false);
  const navigate = useNavigate();

  const onDrop = useCallback(async (acceptedFiles) => {
    setUploading(true);
    const file = acceptedFiles[0];

    try {
      // Step 1: Get the presigned URL from your server
      const presignedUrlResponse = await fetch('/api/video', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          filename: file.name,
          fileType: file.type
        }),
      });

      if (!presignedUrlResponse.ok) {
        throw new Error('Failed to get presigned URL');
      }

      const { presignedUrl, filename, objectKey } = await presignedUrlResponse.json();

      // Step 2: Use the presigned URL to upload the file directly to R2
      const uploadResponse = await fetch(presignedUrl, {
        method: 'PUT',
        body: file,
        headers: {
          'Content-Type': file.type
        }
      });

      if (!uploadResponse.ok) {
        throw new Error('Upload to R2 failed');
      }

      // Step 3: Construct the final URL for the uploaded file
      const finalUrl = `https://hackmit2024.lilbillbiscuit.com/uploads/${filename}`;

      // Navigate to the video player with the final URL
      navigate(`/video/${filename}`, { 
        state: { 
          videoSrc: finalUrl
        } 
      });
    } catch (error) {
      console.error('Upload failed:', error);
      // Handle error (e.g., show error message to user)
    } finally {
      setUploading(false);
    }
  }, [navigate]);

  const { getRootProps, getInputProps, isDragActive, isDragAccept, isDragReject } = useDropzone({
    onDrop,
    accept: { 'video/*': [] },
    multiple: false
  });

  const getColor = () => {
    if (isDragAccept) return '#00e676';
    if (isDragReject) return '#ff1744';
    if (isDragActive) return '#2196f3';
    return '#eeeeee';
  }

  return (
    <Box sx={{ pt: 8 }}>
      <Box sx={{ maxWidth: 600, margin: 'auto', p: 4 }}>
        <Typography variant="h4" gutterBottom>
          Welcome to Video Uploader
        </Typography>
        <Typography variant="body1" paragraph>
          Upload your video file by dragging and dropping it into the box below, or click to select a file.
        </Typography>
        <UploadBox
          {...getRootProps()}
          initial={{ scale: 1 }}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          animate={{
            borderColor: getColor(),
            backgroundColor: isDragActive ? 'rgba(0, 0, 0, 0.05)' : 'transparent'
          }}
          transition={{ duration: 0.3 }}
        >
          <input {...getInputProps()} />
          {uploading ? (
            <CircularProgress />
          ) : (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
            >
              <CloudUploadIcon sx={{ fontSize: 48, mb: 2 }} />
              <Typography variant="h6">
                {isDragActive
                  ? isDragAccept
                    ? "Drop the video here"
                    : "This file type is not accepted"
                  : "Drag 'n' drop a video file here, or click to select"}
              </Typography>
            </motion.div>
          )}
        </UploadBox>
      </Box>
    </Box>
  );
};

export default HomeScreen;
