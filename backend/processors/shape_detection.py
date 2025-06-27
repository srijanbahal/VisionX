import cv2
import numpy as np
from .base import BaseProcessor

class ShapeDetectionProcessor(BaseProcessor):
    @staticmethod
    def hough_transform(image: np.ndarray, parameters: dict) -> np.ndarray:
        """Apply Hough Transform for line detection."""
        gray = ShapeDetectionProcessor.ensure_grayscale(image)
        
        # Edge detection
        edges = cv2.Canny(gray, 50, 150)
        
        # Hough Transform
        rho = float(parameters.get('rho', 1))
        theta = float(parameters.get('theta', np.pi/180))
        threshold = int(parameters.get('threshold', 100))
        
        lines = cv2.HoughLines(edges, rho, theta, threshold)
        
        # Create output image
        output = image.copy()
        
        if lines is not None:
            for line in lines:
                rho, theta = line[0]
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000*(-b))
                y1 = int(y0 + 1000*(a))
                x2 = int(x0 - 1000*(-b))
                y2 = int(y0 - 1000*(a))
                cv2.line(output, (x1, y1), (x2, y2), (0, 0, 255), 2)
        
        return output

    @staticmethod
    def chain_code(image: np.ndarray, parameters: dict) -> np.ndarray:
        """Apply Chain Code for contour detection and representation."""
        gray = ShapeDetectionProcessor.ensure_grayscale(image)
        
        # Threshold the image
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        
        # Find contours
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Create output image
        output = image.copy()
        
        # Draw contours and their chain codes
        for contour in contours:
            # Draw contour
            cv2.drawContours(output, [contour], -1, (0, 255, 0), 2)
            
            # Calculate chain code
            chain_code = []
            for i in range(len(contour)):
                current = contour[i][0]
                next_point = contour[(i + 1) % len(contour)][0]
                dx = next_point[0] - current[0]
                dy = next_point[1] - current[1]
                
                # Convert to chain code (0-7)
                if dx == 1 and dy == 0:
                    code = 0
                elif dx == 1 and dy == 1:
                    code = 1
                elif dx == 0 and dy == 1:
                    code = 2
                elif dx == -1 and dy == 1:
                    code = 3
                elif dx == -1 and dy == 0:
                    code = 4
                elif dx == -1 and dy == -1:
                    code = 5
                elif dx == 0 and dy == -1:
                    code = 6
                else:
                    code = 7
                
                chain_code.append(code)
            
            # Draw chain code values
            for i, point in enumerate(contour):
                cv2.putText(
                    output,
                    str(chain_code[i]),
                    tuple(point[0]),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 0, 0),
                    1
                )
        
        return output

    @classmethod
    def process(cls, image: np.ndarray, algorithm: str, parameters: dict) -> np.ndarray:
        """Process image with the specified shape detection algorithm."""
        if algorithm == 'hough':
            return cls.hough_transform(image, parameters)
        elif algorithm == 'chain':
            return cls.chain_code(image, parameters)
        else:
            raise ValueError(f"Unknown shape detection algorithm: {algorithm}") 