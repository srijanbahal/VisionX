'use client';

import React, { useState } from 'react';
import ImageUploader from '../components/ImageUploader';
import ImageProcessor from '../components/ImageProcessor';
import AlgorithmSelector from '../components/AlgorithmSelector';
import ProcessingHistory from '../components/ProcessingHistory';
import { useImageStore } from '../store/imageStore';
import { Card } from '../components/ui/card';
import { Separator } from '../components/ui/separator';
import { UploadCloud, Settings2 } from 'lucide-react';

export default function Home() {
  const { originalImage } = useImageStore();

  const [selectedAlgorithm, setSelectedAlgorithm] = useState<string>('canny');

  return (
    <div className="min-h-screen bg-background py-10 px-2">
      <div className="max-w-4xl mx-auto space-y-10">
         Upload Section
        <Card className="max-w-xl mx-auto p-6 flex flex-col items-center justify-center border-dashed border-2 border-primary/40 bg-muted/50 shadow-lg">
          <div className="flex items-center gap-3 mb-4">
            <UploadCloud className="h-7 w-7 text-primary" />
            <h2 className="text-xl font-semibold tracking-tight">Upload Image</h2>
          </div>
          <ImageUploader />
        </Card>

        {/* Processing Options */}
        <Card className="max-w-xl mx-auto p-6 flex flex-col items-center justify-center shadow-lg">
          <div className="flex items-center gap-3 mb-4">
            <Settings2 className="h-7 w-7 text-primary" />
            <h2 className="text-xl font-semibold tracking-tight">Processing Options</h2>
          </div>
          <AlgorithmSelector
            selectedAlgorithm={selectedAlgorithm}
            onSelect={setSelectedAlgorithm}
          />
        </Card>

        {/* Image Processing */}
        {originalImage && (
          <Card className="p-6 shadow-lg">
            <h2 className="text-xl font-semibold mb-4">Image Processing</h2>
            <ImageProcessor algorithm={selectedAlgorithm} />
          </Card>
        )}

        {/* Processing History */}
        <Card className="p-6 shadow-lg">
          <h2 className="text-xl font-semibold mb-4">Processing History</h2>
          <ProcessingHistory />
        </Card>

      </div>
    </div>
  );
} 