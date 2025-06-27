import cv2
import numpy as np
from typing import Dict, Any, Tuple
import base64
from io import BytesIO
from PIL import Image

class BaseProcessor:
    @staticmethod
    def decode_image(image_data: str) -> np.ndarray:
        """Decode base64 image data to numpy array."""
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        return cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    @staticmethod
    def encode_image(image: np.ndarray) -> str:
        """Encode numpy array to base64 image data."""
        _, buffer = cv2.imencode('.png', image)
        return f"data:image/png;base64,{base64.b64encode(buffer).decode('utf-8')}"

    @staticmethod
    def validate_parameters(parameters: Dict[str, Any], required_params: list) -> Tuple[bool, str]:
        """Validate that all required parameters are present and valid."""
        for param in required_params:
            if param not in parameters:
                return False, f"Missing required parameter: {param}"
        return True, ""

    @staticmethod
    def ensure_grayscale(image: np.ndarray) -> np.ndarray:
        """Convert image to grayscale if it's not already."""
        if len(image.shape) == 3:
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image

    @staticmethod
    def ensure_color(image: np.ndarray) -> np.ndarray:
        """Convert image to color if it's grayscale."""
        if len(image.shape) == 2:
            return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        return image 