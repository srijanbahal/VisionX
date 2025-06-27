import cv2
import numpy as np
from .base import BaseProcessor

class EdgeDetectionProcessor(BaseProcessor):
    @staticmethod
    def canny(image: np.ndarray, parameters: dict) -> np.ndarray:
        """Apply Canny edge detection."""
        gray = EdgeDetectionProcessor.ensure_grayscale(image)
        edges = cv2.Canny(
            gray,
            threshold1=int(parameters['threshold1']),
            threshold2=int(parameters['threshold2'])
        )
        return EdgeDetectionProcessor.ensure_color(edges)

    @staticmethod
    def log(image: np.ndarray, parameters: dict) -> np.ndarray:
        """Apply Laplacian of Gaussian edge detection."""
        gray = EdgeDetectionProcessor.ensure_grayscale(image)
        kernel_size = int(parameters['kernel_size'])
        sigma = float(parameters['sigma'])
        
        # Ensure kernel size is odd
        if kernel_size % 2 == 0:
            kernel_size += 1
            
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (kernel_size, kernel_size), sigma)
        
        # Apply Laplacian
        laplacian = cv2.Laplacian(blurred, cv2.CV_64F)
        
        # Normalize and convert to uint8
        edges = np.uint8(np.absolute(laplacian))
        return EdgeDetectionProcessor.ensure_color(edges)

    @staticmethod
    def dog(image: np.ndarray, parameters: dict) -> np.ndarray:
        """Apply Difference of Gaussians edge detection."""
        gray = EdgeDetectionProcessor.ensure_grayscale(image)
        sigma1 = float(parameters.get('sigma1', 1.0))
        sigma2 = float(parameters.get('sigma2', 2.0))
        
        # Apply two Gaussian blurs with different sigmas
        g1 = cv2.GaussianBlur(gray, (0, 0), sigma1)
        g2 = cv2.GaussianBlur(gray, (0, 0), sigma2)
        
        # Compute difference
        dog = g1 - g2
        
        # Normalize and convert to uint8
        dog = np.uint8(np.absolute(dog))
        return EdgeDetectionProcessor.ensure_color(dog)

    @classmethod
    def process(cls, image: np.ndarray, algorithm: str, parameters: dict) -> np.ndarray:
        """Process image with the specified edge detection algorithm."""
        if algorithm == 'canny':
            return cls.canny(image, parameters)
        elif algorithm == 'log':
            return cls.log(image, parameters)
        elif algorithm == 'dog':
            return cls.dog(image, parameters)
        else:
            raise ValueError(f"Unknown edge detection algorithm: {algorithm}") 