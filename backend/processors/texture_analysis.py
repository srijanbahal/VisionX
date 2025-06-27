import cv2
import numpy as np
from .base import BaseProcessor
from skimage.feature import graycomatrix, graycoprops

class TextureAnalysisProcessor(BaseProcessor):
    @staticmethod
    def glcm(image: np.ndarray, parameters: dict) -> np.ndarray:
        """Apply Gray-Level Co-occurrence Matrix (GLCM) analysis."""
        gray = TextureAnalysisProcessor.ensure_grayscale(image)
        
        # Quantize the image to reduce the number of gray levels
        num_levels = int(parameters.get('num_levels', 8))
        gray = (gray / (256 // num_levels)).astype(np.uint8)
        
        # Calculate GLCM
        distances = [1]
        angles = [0, np.pi/4, np.pi/2, 3*np.pi/4]
        glcm = graycomatrix(gray, distances, angles, num_levels, symmetric=True, normed=True)
        
        # Calculate GLCM properties
        contrast = graycoprops(glcm, 'contrast')
        dissimilarity = graycoprops(glcm, 'dissimilarity')
        homogeneity = graycoprops(glcm, 'homogeneity')
        energy = graycoprops(glcm, 'energy')
        correlation = graycoprops(glcm, 'correlation')
        
        # Create visualization
        properties = np.stack([
            contrast.reshape(-1),
            dissimilarity.reshape(-1),
            homogeneity.reshape(-1),
            energy.reshape(-1),
            correlation.reshape(-1)
        ])
        
        # Normalize properties to 0-255 range
        properties = ((properties - properties.min()) / (properties.max() - properties.min()) * 255).astype(np.uint8)
        
        # Create a visualization image
        vis_size = int(np.sqrt(len(properties)))
        vis_image = np.zeros((vis_size * 5, vis_size * 4), dtype=np.uint8)
        
        for i, prop in enumerate(properties):
            prop_reshaped = prop.reshape(vis_size, vis_size)
            row = i // 4
            col = i % 4
            vis_image[row*vis_size:(row+1)*vis_size, col*vis_size:(col+1)*vis_size] = prop_reshaped
        
        return TextureAnalysisProcessor.ensure_color(vis_image)

    @classmethod
    def process(cls, image: np.ndarray, algorithm: str, parameters: dict) -> np.ndarray:
        """Process image with the specified texture analysis algorithm."""
        if algorithm == 'glcm':
            return cls.glcm(image, parameters)
        else:
            raise ValueError(f"Unknown texture analysis algorithm: {algorithm}") 