from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Event(Base):
    __tablename__ = "events"
    
    event_id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=False)
    total_seats = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Hold(Base):
    __tablename__ = "holds"
    
    hold_id = Column(String(36), primary_key=True)
    event_id = Column(String(36), ForeignKey("events.event_id"), nullable=False)
    qty = Column(Integer, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    payment_token = Column(String(36), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(String(36), primary_key=True)
    hold_id = Column(String(36), ForeignKey("holds.hold_id"), nullable=False)
    event_id = Column(String(36), ForeignKey("events.event_id"), nullable=False)
    qty = Column(Integer, nullable=False)
    payment_token = Column(String(36), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
