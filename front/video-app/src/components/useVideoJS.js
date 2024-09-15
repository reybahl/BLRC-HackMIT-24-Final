// useVideoJS.js
import { useEffect, useRef } from 'react';
import videojs from 'video.js';

export const useVideoJS = (videoJsOptions) => {
  const videoRef = useRef(null);
  const playerRef = useRef(null);

  useEffect(() => {
    if (!playerRef.current) {
      const videoElement = videoRef.current;
      if (!videoElement) return;

      playerRef.current = videojs(videoElement, videoJsOptions);
    }

    return () => {
      if (playerRef.current) {
        playerRef.current.dispose();
        playerRef.current = null;
      }
    };
  }, [videoJsOptions]);

  return videoRef;
};
