import { create } from 'zustand';

interface ImageState {
  originalImage: string | null;
  processedImage: string | null;
  setOriginalImage: (image: string | null) => void;
  setProcessedImage: (image: string | null) => void;
  resetImages: () => void;
}

export const useImageStore = create<ImageState>((set) => ({
  originalImage: null,
  processedImage: null,
  setOriginalImage: (image) => set({ originalImage: image }),
  setProcessedImage: (image) => set({ processedImage: image }),
  resetImages: () => set({ originalImage: null, processedImage: null }),
})); 