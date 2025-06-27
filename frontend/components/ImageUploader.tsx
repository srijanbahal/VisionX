import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { useImageStore } from '../store/imageStore';
import { uploadImage } from '../services/api';

const ImageUploader = () => {
  const { setOriginalImage } = useImageStore();
  const [error, setError] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);

  // const onDrop = useCallback(async (acceptedFiles: File[]) => {
  //   const file = acceptedFiles[0];
  //   if (!file) return;
  
  //   setIsUploading(true);
  //   setError(null);
  
  //   try {
  //     // Preview URL for image display only
  //     const previewUrl = URL.createObjectURL(file);
  //     setOriginalImage(previewUrl);
  
  //     // Get base64 string
  //     const base64Image = await uploadImage(file);
  
  //     // Store in Zustand or pass directly to processing
  //     // Example: await processImage("canny", { threshold1: 50, threshold2: 100 }, base64Image);
  //   } catch (error) {
  //     console.error('Upload failed:', error);
  //     setError('Failed to upload image. Please try again.');
  //     setOriginalImage(null);
  //   } finally {
  //     setIsUploading(false);
  //   }
  // }, [setOriginalImage]);
  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (!file) return;
  
    setIsUploading(true);
    setError(null);
  
    try {
      const base64Image = await uploadImage(file);  // ✅ get base64 string
      setOriginalImage(base64Image);                // ✅ store base64 in Zustand
  
      console.log("📷 Base64 Length:", base64Image.length);
      console.log("📷 Base64 Prefix:", base64Image.slice(0, 50));
  
      try {
        const base64Data = base64Image.split(',')[1];
        atob(base64Data);  // JS base64 decode — will throw error if invalid
        console.log("✅ Base64 is valid in frontend.");
      } catch (err) {
        console.error("❌ Invalid base64 in frontend:", err);
      }
  
    } catch (error) {
      console.error('Upload failed:', error);
      setError('Failed to upload image. Please try again.');
      setOriginalImage(null);
    } finally {
      setIsUploading(false);
    }
  }, [setOriginalImage]);
  

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.gif']
    },
    maxFiles: 1
  });

  return (
    <div
      {...getRootProps()}
      className={`max-w-md mx-auto border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors
        ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-blue-400'}
        ${isUploading ? 'opacity-50 cursor-not-allowed' : ''}`}
    >
      <input {...getInputProps()} disabled={isUploading} />
      <div className="space-y-4 flex flex-col items-center justify-center">
        <svg
          className="mx-auto h-16 w-16 text-gray-400"
          stroke="currentColor"
          fill="none"
          viewBox="0 0 48 48"
          aria-hidden="true"
        >
          <path
            d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
            strokeWidth={2}
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
        <div className="text-gray-600">
          {isUploading ? (
            <p>Uploading...</p>
          ) : isDragActive ? (
            <p>Drop the image here ...</p>
          ) : (
            <>
              <p className="font-medium">Drag and drop an image here, or click to select one</p>
              <p className="text-xs text-gray-400 mt-1">Supported formats: PNG, JPG, GIF up to 10MB</p>
            </>
          )}
        </div>
        {error && (
          <p className="text-sm text-red-500">{error}</p>
        )}
      </div>
    </div>
  );
};

export default ImageUploader; 