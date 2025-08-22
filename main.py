from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import crud
import schemas
from database import engine, get_db
from models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mohit's Box Office API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/events", response_model=schemas.EventResponse)
async def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    if event.total_seats <= 0:
        raise HTTPException(status_code=400, detail="Total seats must be positive")
    
    db_event = crud.create_event(db, event)
    return db_event

@app.post("/holds", response_model=schemas.HoldResponse)
async def create_hold(hold_request: schemas.HoldRequest, db: Session = Depends(get_db)):
    if hold_request.qty <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be positive")
    
    event = crud.get_event(db, hold_request.event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    status = crud.get_event_status(db, hold_request.event_id)
    
    if status.available < hold_request.qty:
        raise HTTPException(
            status_code=400, 
            detail=f"Not enough seats available. Available: {status.available}, Requested: {hold_request.qty}"
        )
    
    expires_at = datetime.now() + timedelta(minutes=2)
    db_hold = crud.create_hold(db, hold_request, expires_at)
    
    return db_hold

@app.post("/book", response_model=schemas.BookingResponse)
async def confirm_booking(booking_request: schemas.BookingRequest, db: Session = Depends(get_db)):
    hold = crud.get_hold(db, booking_request.hold_id)
    if not hold:
        raise HTTPException(status_code=404, detail="Hold not found")
    
    if hold.expires_at <= datetime.now():
        raise HTTPException(status_code=400, detail="Hold has expired")
    
    if hold.payment_token != booking_request.payment_token:
        raise HTTPException(status_code=400, detail="Invalid payment token")
    
    existing_booking = crud.get_booking_by_hold_id(db, booking_request.hold_id)
    if existing_booking:
        return existing_booking
    
    db_booking = crud.create_booking(db, hold)
    
    db.delete(hold)
    db.commit()
    
    return db_booking

@app.get("/events/{event_id}", response_model=schemas.EventStatus)
async def get_event_status_endpoint(event_id: str, db: Session = Depends(get_db)):
    status = crud.get_event_status(db, event_id)
    if not status:
        raise HTTPException(status_code=404, detail="Event not found")
    return status

@app.get("/")
async def root():
    return {
        "message": "Welcome to Mohit's Box Office. Please go to docs by /docs",
        "endpoints": {
            "create_event": "POST /events",
            "create_hold": "POST /holds", 
            "confirm_booking": "POST /book",
            "get_status": "GET /events/{event_id}"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}



