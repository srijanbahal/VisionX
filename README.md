# VisionX - Image Processing Web Application

VisionX is a full-stack web application that showcases classical computer vision algorithms with real-time visualization and parameter tuning capabilities.

## Features

- Real-time image processing with live preview
- Multiple image processing algorithms:
  - Edge Detection (Canny, Sobel, Prewitt)
  - Texture Analysis (GLCM, LBP)
  - Shape Detection (Contour, Hough Transform)
  - Image Enhancement (Histogram Equalization, Adaptive Thresholding)
  - Geometric Transformations (Rotation, Scaling, Translation)
  - Region-based Segmentation (Watershed, GrabCut)
- Drag-and-drop image upload
- Processing history tracking
- Responsive design with TailwindCSS
- RESTful API with FastAPI
- PostgreSQL database for data persistence

## Tech Stack

### Frontend
- Next.js 13+ (App Router)
- React.js
- TailwindCSS
- TypeScript
- Axios for API calls

### Backend
- FastAPI
- OpenCV
- NumPy
- PostgreSQL
- SQLAlchemy
- Python 3.8+

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- PostgreSQL
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/visionx.git
cd visionx
```

2. Set up the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up the frontend:
```bash
cd frontend
npm install
```

4. Create a `.env` file in the backend directory with the following variables:
```
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
API_HOST=0.0.0.0
NEXT_PUBLIC_API_URL=http://localhost:8000
```

5. Start the development servers:

Backend:
```bash
cd backend
uvicorn main:app --reload
```

Frontend:
```bash
cd frontend
npm run dev
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Project Structure

```
visionx/
├── backend/
│   ├── app/
│   │   ├── processors/
│   │   │   ├── base.py
│   │   │   ├── edge_detection.py
│   │   │   ├── texture_analysis.py
│   │   │   ├── shape_detection.py
│   │   │   ├── image_enhancement.py
│   │   │   ├── geometric_transformation.py
│   │   │   └── region_segmentation.py
│   │   ├── models.py
│   │   └── database.py
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── components/
│   │   │   ├── AlgorithmSelector.tsx
│   │   │   ├── ImageProcessor.tsx
│   │   │   └── ProcessingHistory.tsx
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── public/
│   └── package.json
└── README.md
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenCV for providing the computer vision algorithms
- Next.js team for the amazing framework
- FastAPI for the high-performance API framework 