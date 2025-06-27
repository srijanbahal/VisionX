from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import cv2
import numpy as np
from PIL import Image
import io
import base64
from typing import Optional, Dict, Any
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
import re

from .database import get_db, engine
from .processors.edge_detection import EdgeDetectionProcessor
from .processors.texture_analysis import TextureAnalysisProcessor
from .processors.shape_detection import ShapeDetectionProcessor
from .processors.image_enhancement import ImageEnhancementProcessor
from .processors.geometric_transformation import GeometricTransformationProcessor
from .processors.region_segmentation import RegionSegmentationProcessor
from . import models, schemas

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Load environment variables
load_dotenv()

app = FastAPI(
    title="VisionX API",
    description="API for VisionX - Interactive Computer Vision Web Application",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory if it doesn't exist
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
async def root():
    return {"message": "Welcome to VisionX API"}

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Read and validate image
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        # Save image
        filename = f"{UPLOAD_DIR}/{file.filename}"
        cv2.imwrite(filename, img)
        
        return {"filename": file.filename, "message": "Image uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process")
async def process_image(payload: schemas.ProcessImageRequest, db: Session = Depends(get_db)):
    print(f"[RAW BASE64] First 100 chars: {payload.image[:100]}")
    print(f"[RAW BASE64] Length: {len(payload.image)}")

    try:
        algorithm = payload.algorithm
        parameters = payload.parameters
        image = payload.image
        # print("tired af")
        
                
        if ',' in image:
            image = image.split(',')[1]

        # Fix padding issues: base64 strings must be length % 4 == 0
        image = image.strip().replace('\n', '').replace('\r', '')
        image = re.sub(r'[^A-Za-z0-9+/=]', '', image)

        # Pad if needed
        missing_padding = len(image) % 4
        if missing_padding != 0:
            image += '=' * (4 - missing_padding)
        try:
            image_bytes = base64.b64decode(image, validate=True)
        except Exception as e:
            print("---- BASE64 DECODE FAILED ----")
            print(f"Image Length: {len(image)}")
            print(f"Base64 Error: {e}")
            with open("failed_base64.txt", "w") as f:
                f.write(image)  # Save for analysis
            raise HTTPException(status_code=400, detail="Base64 decode error.")
        # print("iski mkc")
        # Step 4: Decode image
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        # print(img)
        if img is None:
            # Save broken image to debug (optional)
            with open("broken_image.png", "wb") as f:
                print("hoiii")
                f.write(image_bytes)
                print(image_bytes)
            raise HTTPException(status_code=400, detail="cv2.imdecode failed: Invalid image bytes")

        # Process image (same as before)
        if algorithm in ['canny', 'log', 'dog']:
            processed = EdgeDetectionProcessor.process(img, algorithm, parameters)
        elif algorithm == 'glcm':
            processed = TextureAnalysisProcessor.process(img, algorithm, parameters)
        elif algorithm in ['hough', 'chain']:
            processed = ShapeDetectionProcessor.process(img, algorithm, parameters)
        elif algorithm == 'histogram':
            processed = ImageEnhancementProcessor.process(img, algorithm, parameters)
        elif algorithm == 'affine':
            processed = GeometricTransformationProcessor.process(img, algorithm, parameters)
        elif algorithm in ['region-growing', 'split-merge']:
            processed = RegionSegmentationProcessor.process(img, algorithm, parameters)
        else:
            raise HTTPException(status_code=400, detail=f"Unknown algorithm: {algorithm}")

        _, buffer = cv2.imencode('.png', processed)
        processed_base64 = base64.b64encode(buffer).decode('utf-8')

        history = models.ProcessingHistory(
            original_image=image,
            processed_image=processed_base64,
            algorithm=algorithm,
            parameters=parameters
        )
        db.add(history)
        db.commit()

        return {
            "processedImage": f"data:image/png;base64,{processed_base64}",
            "message": "Image processed successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
async def get_history(db: Session = Depends(get_db)):
    try:
        history = db.query(models.ProcessingHistory).all()
        return {
            "history": [
                {
                    "id": h.id,
                    "algorithm": h.algorithm,
                    "parameters": h.parameters,
                    "created_at": h.created_at.isoformat(),
                    "original_image": h.original_image,
                    "processed_image": h.processed_image
                }
                for h in history
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 