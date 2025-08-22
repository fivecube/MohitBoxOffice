from datetime import datetime

from pydantic import BaseModel


class EventCreate(BaseModel):
    name: str
    total_seats: int

class EventResponse(BaseModel):
    event_id: str
    total_seats: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class HoldRequest(BaseModel):
    event_id: str
    qty: int

class HoldResponse(BaseModel):
    hold_id: str
    event_id: str
    qty: int
    expires_at: datetime
    payment_token: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class BookingRequest(BaseModel):
    hold_id: str
    payment_token: str

class BookingResponse(BaseModel):
    id: str
    event_id: str
    qty: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class EventStatus(BaseModel):
    total: int
    available: int
    held: int
    booked: int
