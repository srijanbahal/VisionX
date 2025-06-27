import React, { useState, useEffect } from 'react';
import { useImageStore } from '../store/imageStore';
import { processImage } from '../services/api';
import { Card } from "../components/ui/card";
import { Button } from "../components/ui/button";
import { Slider } from "../components/ui/slider";
import { Loader2 } from "lucide-react";

interface ImageProcessorProps {
  algorithm: string;
}

interface AlgorithmParam {
  name: string;
  min: number;
  max: number;
  default: number;
  step?: number;
}

const ImageProcessor = ({ algorithm }: ImageProcessorProps) => {
  const { originalImage, processedImage, setProcessedImage } = useImageStore();
  const [parameters, setParameters] = useState<Record<string, number>>({});
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const algorithmParams: Record<string, AlgorithmParam[]> = {
    canny: [
      { name: 'threshold1', min: 0, max: 255, default: 100 },
      { name: 'threshold2', min: 0, max: 255, default: 200 },
    ],
    log: [
      { name: 'kernel_size', min: 1, max: 31, default: 5, step: 2 },
      { name: 'sigma', min: 0.1, max: 5, default: 1, step: 0.1 },
    ],
    // Add more algorithm parameters as needed
  };

  useEffect(() => {
    // Initialize parameters when algorithm changes
    const params = algorithmParams[algorithm as keyof typeof algorithmParams] || [];
    const initialParams = params.reduce((acc, param) => ({
      ...acc,
      [param.name]: param.default,
    }), {});
    setParameters(initialParams);
  }, [algorithm]);

  const handleParameterChange = (name: string, value: number) => {
    setParameters(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleProcessImage = async () => {
    if (!originalImage) return;

    setIsProcessing(true);
    setError(null);

    try {
      const response = await processImage(algorithm, parameters, originalImage);
      setProcessedImage(response.processedImage);
    } catch (error) {
      console.error('Processing failed:', error);
      setError('Failed to process image. Please try again.');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="p-4">
          <h3 className="text-lg font-semibold mb-4">Original Image</h3>
          {originalImage ? (
            <img
              src={originalImage}
              alt="Original"
              className="w-full h-[300px] object-contain rounded-lg bg-gray-50"
            />
          ) : (
            <div className="w-full h-[300px] bg-gray-50 rounded-lg flex items-center justify-center">
              <p className="text-gray-500">No image selected</p>
            </div>
          )}
        </Card>

        <Card className="p-4">
          <h3 className="text-lg font-semibold mb-4">Processed Image</h3>
          {processedImage ? (
            <img
              src={processedImage}
              alt="Processed"
              className="w-full h-[300px] object-contain rounded-lg bg-gray-50"
            />
          ) : (
            <div className="w-full h-[300px] bg-gray-50 rounded-lg flex items-center justify-center">
              <p className="text-gray-500">Processed image will appear here</p>
            </div>
          )}
        </Card>
      </div>

      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-6">Parameters</h3>
        <div className="space-y-6">
          {algorithmParams[algorithm as keyof typeof algorithmParams]?.map((param) => (
            <div key={param.name} className="space-y-2">
              <div className="flex justify-between items-center">
                <label className="text-sm font-medium text-gray-700">
                  {param.name}
                </label>
                <span className="text-sm text-gray-500">
                  {parameters[param.name] || param.default}
                </span>
              </div>
              <Slider
                min={param.min}
                max={param.max}
                step={param.step || 1}
                value={[parameters[param.name] || param.default]}
                onValueChange={(value) => handleParameterChange(param.name, value[0])}
                disabled={isProcessing}
                className="w-full"
              />
              <div className="flex justify-between text-xs text-gray-500">
                <span>{param.min}</span>
                <span>{param.max}</span>
              </div>
            </div>
          ))}
        </div>

        {error && (
          <p className="mt-4 text-sm text-red-500">{error}</p>
        )}

        <Button
          onClick={handleProcessImage}
          disabled={isProcessing || !originalImage}
          className="w-full mt-6"
          variant="default"
        >
          {isProcessing ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              Processing...
            </>
          ) : (
            'Process Image'
          )}
        </Button>
      </Card>
    </div>
  );
};

export default ImageProcessor; 