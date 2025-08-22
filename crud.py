import uuid
from datetime import datetime

from sqlalchemy import and_
from sqlalchemy.orm import Session

import models
import schemas


def create_event(db: Session, event: schemas.EventCreate) -> models.Event:
    db_event = models.Event(
        event_id=str(uuid.uuid4()),
        name=event.name,
        total_seats=event.total_seats
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_event(db: Session, event_id: str) -> models.Event:
    return db.query(models.Event).filter(models.Event.event_id == event_id).first()

def create_hold(db: Session, hold: schemas.HoldRequest, expires_at: datetime) -> models.Hold:
    db_hold = models.Hold(
        hold_id=str(uuid.uuid4()),
        event_id=hold.event_id,
        qty=hold.qty,
        expires_at=expires_at,
        payment_token=str(uuid.uuid4())
    )
    db.add(db_hold)
    db.commit()
    db.refresh(db_hold)
    return db_hold

def get_hold(db: Session, hold_id: str) -> models.Hold:
    return db.query(models.Hold).filter(models.Hold.hold_id == hold_id).first()

def get_active_holds_for_event(db: Session, event_id: str) -> list[models.Hold]:
    current_time = datetime.now()
    return db.query(models.Hold).filter(
        and_(
            models.Hold.event_id == event_id,
            models.Hold.expires_at > current_time
        )
    ).all()

def create_booking(db: Session, hold: models.Hold) -> models.Booking:
    db_booking = models.Booking(
        id=str(uuid.uuid4()),
        hold_id=hold.hold_id,
        event_id=hold.event_id,
        qty=hold.qty,
        payment_token=hold.payment_token
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def get_booking_by_hold_id(db: Session, hold_id: str) -> models.Booking:
    return db.query(models.Booking).filter(models.Booking.hold_id == hold_id).first()

def get_bookings_for_event(db: Session, event_id: str) -> list[models.Booking]:
    return db.query(models.Booking).filter(models.Booking.event_id == event_id).all()

def get_event_status(db: Session, event_id: str) -> schemas.EventStatus:
    event = get_event(db, event_id)
    if not event:
        return None
    
    active_holds = get_active_holds_for_event(db, event_id)
    total_held = sum(hold.qty for hold in active_holds)
    
    bookings = get_bookings_for_event(db, event_id)
    total_booked = sum(booking.qty for booking in bookings)
    
    available = event.total_seats - total_held - total_booked
    
    return schemas.EventStatus(
        total=event.total_seats,
        available=available,
        held=total_held,
        booked=total_booked
    )
