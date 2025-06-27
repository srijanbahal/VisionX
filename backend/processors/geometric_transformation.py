import cv2
import numpy as np
from .base import BaseProcessor

class GeometricTransformationProcessor(BaseProcessor):
    @staticmethod
    def affine_transform(image: np.ndarray, parameters: dict) -> np.ndarray:
        """Apply affine transformation to the image."""
        height, width = image.shape[:2]
        
        # Get transformation parameters
        scale_x = float(parameters.get('scale_x', 1.0))
        scale_y = float(parameters.get('scale_y', 1.0))
        rotation = float(parameters.get('rotation', 0.0))
        tx = float(parameters.get('tx', 0.0))
        ty = float(parameters.get('ty', 0.0))
        
        # Calculate the center of the image
        center = (width / 2, height / 2)
        
        # Create rotation matrix
        rotation_matrix = cv2.getRotationMatrix2D(center, rotation, 1.0)
        
        # Add translation to the rotation matrix
        rotation_matrix[0, 2] += tx
        rotation_matrix[1, 2] += ty
        
        # Apply scaling
        rotation_matrix[0, 0] *= scale_x
        rotation_matrix[1, 1] *= scale_y
        
        # Apply the transformation
        transformed = cv2.warpAffine(
            image,
            rotation_matrix,
            (width, height),
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=(0, 0, 0)
        )
        
        return transformed

    @classmethod
    def process(cls, image: np.ndarray, algorithm: str, parameters: dict) -> np.ndarray:
        """Process image with the specified geometric transformation algorithm."""
        if algorithm == 'affine':
            return cls.affine_transform(image, parameters)
        else:
            raise ValueError(f"Unknown geometric transformation algorithm: {algorithm}") 