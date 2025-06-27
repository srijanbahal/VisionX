import cv2
import numpy as np
from .base import BaseProcessor

class ImageEnhancementProcessor(BaseProcessor):
    @staticmethod
    def histogram_equalization(image: np.ndarray, parameters: dict) -> np.ndarray:
        """Apply histogram equalization to enhance image contrast."""
        if len(image.shape) == 3:
            # Convert to LAB color space
            lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
            
            # Split the LAB image into L, A, and B channels
            l, a, b = cv2.split(lab)
            
            # Apply histogram equalization to the L channel
            clahe = cv2.createCLAHE(
                clipLimit=float(parameters.get('clip_limit', 2.0)),
                tileGridSize=(8, 8)
            )
            l = clahe.apply(l)
            
            # Merge the channels
            lab = cv2.merge((l, a, b))
            
            # Convert back to BGR
            return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        else:
            # For grayscale images
            clahe = cv2.createCLAHE(
                clipLimit=float(parameters.get('clip_limit', 2.0)),
                tileGridSize=(8, 8)
            )
            return clahe.apply(image)

    @classmethod
    def process(cls, image: np.ndarray, algorithm: str, parameters: dict) -> np.ndarray:
        """Process image with the specified enhancement algorithm."""
        if algorithm == 'histogram':
            return cls.histogram_equalization(image, parameters)
        else:
            raise ValueError(f"Unknown enhancement algorithm: {algorithm}") 