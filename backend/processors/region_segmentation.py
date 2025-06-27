import cv2
import numpy as np
from .base import BaseProcessor
from skimage.segmentation import flood_fill
from skimage.morphology import flood

class RegionSegmentationProcessor(BaseProcessor):
    @staticmethod
    def region_growing(image: np.ndarray, parameters: dict) -> np.ndarray:
        """Apply region growing segmentation."""
        gray = RegionSegmentationProcessor.ensure_grayscale(image)
        
        # Get parameters
        threshold = float(parameters.get('threshold', 20.0))
        min_size = int(parameters.get('min_size', 100))
        
        # Initialize output image
        output = np.zeros_like(gray)
        visited = np.zeros_like(gray, dtype=bool)
        
        # Get seed points (local minima)
        kernel_size = 5
        local_min = cv2.erode(gray, np.ones((kernel_size, kernel_size)))
        seed_points = np.where(gray == local_min)
        
        # Process each seed point
        for y, x in zip(*seed_points):
            if visited[y, x]:
                continue
                
            # Start region growing from this seed
            region = flood_fill(
                gray,
                (y, x),
                gray[y, x],
                tolerance=threshold,
                connectivity=1
            )
            
            # Update visited pixels
            visited[region != 0] = True
            
            # Add region to output if it's large enough
            if np.sum(region != 0) >= min_size:
                output[region != 0] = gray[y, x]
        
        return RegionSegmentationProcessor.ensure_color(output)

    @staticmethod
    def split_merge(image: np.ndarray, parameters: dict) -> np.ndarray:
        """Apply splitting and merging segmentation."""
        gray = RegionSegmentationProcessor.ensure_grayscale(image)
        
        # Get parameters
        threshold = float(parameters.get('threshold', 20.0))
        min_size = int(parameters.get('min_size', 4))
        
        def split_region(region, level=0):
            if level >= 4:  # Maximum recursion depth
                return region
                
            h, w = region.shape
            if h <= min_size or w <= min_size:
                return region
                
            # Calculate region statistics
            mean = np.mean(region)
            std = np.std(region)
            
            if std <= threshold:
                return np.full_like(region, mean)
                
            # Split into four sub-regions
            h2, w2 = h // 2, w // 2
            regions = [
                split_region(region[:h2, :w2], level + 1),
                split_region(region[:h2, w2:], level + 1),
                split_region(region[h2:, :w2], level + 1),
                split_region(region[h2:, w2:], level + 1)
            ]
            
            # Merge regions if they are similar
            merged = np.zeros_like(region)
            merged[:h2, :w2] = regions[0]
            merged[:h2, w2:] = regions[1]
            merged[h2:, :w2] = regions[2]
            merged[h2:, w2:] = regions[3]
            
            return merged
        
        # Apply splitting and merging
        segmented = split_region(gray)
        
        # Convert to uint8
        segmented = np.uint8(segmented)
        
        return RegionSegmentationProcessor.ensure_color(segmented)

    @classmethod
    def process(cls, image: np.ndarray, algorithm: str, parameters: dict) -> np.ndarray:
        """Process image with the specified region segmentation algorithm."""
        if algorithm == 'region-growing':
            return cls.region_growing(image, parameters)
        elif algorithm == 'split-merge':
            return cls.split_merge(image, parameters)
        else:
            raise ValueError(f"Unknown region segmentation algorithm: {algorithm}") 