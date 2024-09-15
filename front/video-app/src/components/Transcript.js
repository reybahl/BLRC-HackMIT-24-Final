import React, { useRef, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  ImageList,
  ImageListItem,
  Modal,
  styled
} from '@mui/material';

const TranscriptContainer = styled(Paper)(({ theme }) => ({
  maxHeight: '500px',
  overflowY: 'auto',
  position: 'relative',
  padding: theme.spacing(1), // Reduced padding
}));

const TranscriptTitle = styled(Typography)(({ theme }) => ({
  position: 'sticky',
  top: 0,
  backgroundColor: theme.palette.background.paper,
  zIndex: 1,
  paddingBottom: theme.spacing(1),
  marginTop: -theme.spacing(3), // Negative margin to remove gap at the top
  marginBottom: theme.spacing(1),
}));

const TranscriptContent = styled(Box)({
  display: 'grid',
  gridTemplateColumns: 'auto 1fr',
  columnGap: '8px', // Reduced horizontal gap
  rowGap: '4px', // Reduced vertical gap between lines
});

const TimestampBox = styled(Box)({
  display: 'flex',
  alignItems: 'flex-start', // Align to top instead of center
  color: 'gray',
  fontSize: '0.8rem',
  paddingTop: '4px', // Add a small top padding to align with text
});

const ContentBox = styled(Box)({
  display: 'flex',
  flexDirection: 'column',
});

const StyledImageList = styled(ImageList)(({ theme }) => ({
  marginBottom: theme.spacing(1),
}));

const Transcript = ({ transcriptData, currentTime }) => {
  const [openImage, setOpenImage] = React.useState(null);
  const transcriptRef = useRef(null);

  const handleOpenImage = (url) => setOpenImage(url);
  const handleCloseImage = () => setOpenImage(null);

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    return date.toISOString().substr(11, 8);
  };

  // Sort transcript data by start time
  const sortedTranscript = [...transcriptData.elements].sort((a, b) => 
    new Date(a.timestamp_start) - new Date(b.timestamp_start)
  );

  useEffect(() => {
    const activeElement = transcriptRef.current?.querySelector('.active');
    if (activeElement) {
      activeElement.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  }, [currentTime]);

  return (
    <TranscriptContainer ref={transcriptRef}>
      <TranscriptTitle variant="h6">Transcript</TranscriptTitle>
      <TranscriptContent>
        {sortedTranscript.map((item, index) => {
          const startTime = new Date(item.timestamp_start).getTime() / 1000;
          const endTime = new Date(item.timestamp_end).getTime() / 1000;
          const isActive = currentTime >= startTime && currentTime < endTime;

          return (
            <React.Fragment key={index}>
              <TimestampBox>
                {formatTimestamp(item.timestamp_start)}
              </TimestampBox>
              <ContentBox
                className={isActive ? 'active' : ''}
                sx={{
                  backgroundColor: isActive ? 'action.selected' : 'background.paper',
                  padding: '4px',
                  borderRadius: '4px',
                }}
              >
                {item.photo_urls && (
                  <StyledImageList cols={3} rowHeight={100}>
                    {item.photo_urls.map((url, imgIndex) => (
                      <ImageListItem key={imgIndex} onClick={() => handleOpenImage(url)}>
                        <img src={url} alt={`Thumbnail ${imgIndex + 1}`} loading="lazy" />
                      </ImageListItem>
                    ))}
                  </StyledImageList>
                )}
                <Typography variant="body2"> {/* Changed to body2 for slightly smaller text */}
                  {item.content}
                </Typography>
              </ContentBox>
            </React.Fragment>
          );
        })}
      </TranscriptContent>
      <Modal
        open={!!openImage}
        onClose={handleCloseImage}
        aria-labelledby="image-modal"
        aria-describedby="expanded image"
      >
        <Box sx={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          maxWidth: '90%',
          maxHeight: '90%',
        }}>
          <img src={openImage} alt="Expanded view" style={{ width: '100%', height: 'auto' }} />
        </Box>
      </Modal>
    </TranscriptContainer>
  );
};

export default Transcript;
