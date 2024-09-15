import React, { useState } from 'react';

function FileUpload() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      setStatus('Please select a file first.');
      return;
    }

    setStatus('Preparing upload...');

    try {
      // Step 1: Get the presigned URL from your server
      const presignedUrlResponse = await fetch('/presigned_url/video', {
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

      const { presignedUrl, filename } = await presignedUrlResponse.json();

      // Step 2: Use the presigned URL to upload the file directly to R2
      setStatus('Uploading...');
      const uploadResponse = await fetch(presignedUrl, {
        method: 'PUT',
        body: file,
        headers: {
          'Content-Type': file.type
        }
      });

      if (!uploadResponse.ok) {
        throw new Error('Upload failed');
      }

      setStatus('Upload successful!');
    } catch (error) {
      console.error('Error:', error);
      setStatus(`Upload failed: ${error.message}`);
    }
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
      <p>{status}</p>
    </div>
  );
}

export default FileUpload;
