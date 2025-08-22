# Mohit's Box Office - Ticketing Service

## Key Modules
- `main.py`: FastAPI app with 4 endpoints (events, holds, bookings, status)
- `models.py`: SQLAlchemy models (Event, Hold, Booking)
- `schemas.py`: Pydantic schemas for request/response validation
- `crud.py`: Database operations with concurrency handling
- `database.py`: SQLAlchemy engine and session management

## Data Model
- **Event**: event_id, name, total_seats, created_at
- **Hold**: hold_id, event_id, qty, expires_at, payment_token, created_at
- **Booking**: id, hold_id, event_id, qty, payment_token, created_at

## Idempotency Approach
- Booking endpoint uses hold_id as unique identifier. 
- Duplicate requests with same hold_id return existing booking without creating new records.

## APIs
- POST `{base_url}/events` - Create event
- POST `{base_url}/holds` - Hold seats
- POST `{base_url}/bookings` - Book seats  
- GET `{base_url}/events/{event_id}/status` - Check event status
- GET `{base_url}/docs` - Swagger UI

## Steps to Test the online Application
- Please Open the postman collection provided in the email
- The collection will have base_url populated to the Application deployed on Render dot com.

## Local Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```


