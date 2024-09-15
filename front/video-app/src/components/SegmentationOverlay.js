import React, { useRef, useEffect, useState } from 'react';
import styled from '@emotion/styled';

const OverlayImage = styled('img')({
  position: 'absolute',
  top: 0,
  left: 0,
  width: '100%',
  height: '100%',
  pointerEvents: 'none',
});

const SegmentationOverlay = ({ segmentationData, onHover, onClick }) => {
  const [colorMap, setColorMap] = useState({});
  const canvasRef = useRef(null);
  const imageRef = useRef(null);

  useEffect(() => {
    if (segmentationData) {
      const map = {};
      segmentationData.labels.forEach(label => {
        const hexCode = Object.keys(label)[0];
        map[hexCode.toLowerCase()] = label[hexCode];
      });
      setColorMap(map);
    }
  }, [segmentationData]);

  useEffect(() => {
    const canvas = canvasRef.current;
    const image = imageRef.current;
    if (canvas && image && image.complete) {
      const ctx = canvas.getContext('2d');
      canvas.width = image.width;
      canvas.height = image.height;
      ctx.drawImage(image, 0, 0, image.width, image.height);
    }
  }, [segmentationData]);

  const handleMouseMove = (event) => {
    const canvas = canvasRef.current;
    if (canvas) {
      const rect = canvas.getBoundingClientRect();
      const x = Math.floor((event.clientX - rect.left) / rect.width * canvas.width);
      const y = Math.floor((event.clientY - rect.top) / rect.height * canvas.height);
      
      const ctx = canvas.getContext('2d');
      const pixelData = ctx.getImageData(x, y, 1, 1).data;
      const hexColor = `#${pixelData[0].toString(16).padStart(2, '0')}${pixelData[1].toString(16).padStart(2, '0')}${pixelData[2].toString(16).padStart(2, '0')}`;
      
      const label = colorMap[hexColor.toLowerCase()] || '';
      onHover(label);
    }
  };

  const handleClick = (event) => {
    const canvas = canvasRef.current;
    if (canvas) {
      const rect = canvas.getBoundingClientRect();
      const x = Math.floor((event.clientX - rect.left) / rect.width * canvas.width);
      const y = Math.floor((event.clientY - rect.top) / rect.height * canvas.height);
      
      const ctx = canvas.getContext('2d');
      const pixelData = ctx.getImageData(x, y, 1, 1).data;
      const hexColor = `#${pixelData[0].toString(16).padStart(2, '0')}${pixelData[1].toString(16).padStart(2, '0')}${pixelData[2].toString(16).padStart(2, '0')}`;
      
      const label = colorMap[hexColor.toLowerCase()] || '';
      onClick(event, label);
    }
  };

  return (
    <>
      <OverlayImage
        ref={imageRef}
        src={segmentationData.data_url}
        alt="Segmentation overlay"
        style={{ opacity: 0 }}
        onLoad={() => canvasRef.current.getContext('2d').drawImage(imageRef.current, 0, 0)}
      />
      <canvas
        ref={canvasRef}
        onMouseMove={handleMouseMove}
        onClick={handleClick}
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          pointerEvents: 'auto',
        }}
      />
    </>
  );
};

export default SegmentationOverlay;
