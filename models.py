from sqlalchemy import Column, Integer, String, Date, ForeignKey,func
from sqlalchemy.orm import relationship
from database import Base  # Replace with your actual SQLAlchemy Base import
from datetime import date


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    location = Column(String(200), nullable=False)
    date = Column(Date, nullable=False)
    description = Column(String(500), nullable=True)
    status = Column(String(50), nullable=False)     
    attendees = relationship("Christian", back_populates="event", cascade="all, delete-orphan")
    created_at = Column(Date, default=func.now(), nullable=False) 


class Christian(Base):
    __tablename__ = 'christians'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    phone = Column(String(15), nullable=False)
    status = Column(String(50), nullable=True)
    role = Column(String(50), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=True)
    joined_date = Column(Date, nullable=False, default=func.now())
    
    event = relationship("Event", back_populates="attendees")
