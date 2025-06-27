from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    processing_history = relationship("ProcessingHistory", back_populates="user")

class ProcessingHistory(Base):
    __tablename__ = "processing_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    original_image = Column(String)  # Path to original image
    processed_image = Column(String)  # Path to processed image
    algorithm = Column(String)  # Name of the algorithm used
    parameters = Column(JSON)  # Algorithm parameters used
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="processing_history") 