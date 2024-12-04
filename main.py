from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, cast, String
from database import engine, SessionLocal
from models import Base, Christian, Event
from schemas import ChristianCreate, Christian as ChristianResponse, EventCreate, Event as EventResponse




# Initialize FastAPI application
app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create database tables
Base.metadata.create_all(bind=engine)

# Helper function to create ILIKE filter
def ilike_filter(column, search_query):
    """
    Helper function to create an ILIKE filter for SQLAlchemy queries.

    Args:
        column (Column): The column to apply the ILIKE filter on.
        search_query (str): The search term to use in the filter.

    Returns:
        sqlalchemy.sql.elements.BinaryExpression: The ILIKE filter expression.
    """
    search_pattern = f"%{search_query}%"
    return column.ilike(search_pattern)

# Christians Endpoints

@app.get("/christians", response_model=list[ChristianResponse])
def get_all_christians(db: Session = Depends(get_db)):
    christians = db.query(Christian).all()
    return christians

@app.get("/searchChristians", response_model=list[ChristianResponse])
def search_christians(
    search_query: str,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    results = db.query(Christian).filter(
        or_(
            ilike_filter(Christian.name, search_query),
            ilike_filter(cast(Christian.age, String), search_query),
            ilike_filter(Christian.role, search_query),
            ilike_filter(Christian.status, search_query),
            ilike_filter(Christian.gender, search_query),
        )
    ).offset(skip).limit(limit).all()
    return results

@app.post("/christians/addChristian", response_model=ChristianResponse)
def add_christian(christian: ChristianCreate, db: Session = Depends(get_db)):
    db_christian = Christian(**christian.dict())
    db.add(db_christian)
    db.commit()
    db.refresh(db_christian)
    return db_christian

@app.put("/christians/{christian_id}", response_model=ChristianResponse)
def edit_christian(christian_id: int, christian: ChristianCreate, db: Session = Depends(get_db)):
    db_christian = db.query(Christian).filter(Christian.id == christian_id).first()
    if db_christian is None:
        raise HTTPException(status_code=404, detail="Christian not found")
    
    for key, value in christian.dict().items():
        setattr(db_christian, key, value)
    db.commit()
    db.refresh(db_christian)
    return db_christian

@app.delete("/christians/{christian_id}", response_model=ChristianResponse)
def delete_christian(christian_id: int, db: Session = Depends(get_db)):
    db_christian = db.query(Christian).filter(Christian.id == christian_id).first()
    if db_christian is None:
        raise HTTPException(status_code=404, detail="Christian not found")
    
    db.delete(db_christian)
    db.commit()
    return db_christian

# Events Endpoints

@app.get("/events", response_model=list[EventResponse])
def get_all_events(db: Session = Depends(get_db)):
    events = db.query(Event).all()
    return events

@app.get("/searchEvents", response_model=list[EventResponse])
def search_events(
    search_text: str, 
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db)
):
    events = db.query(Event).filter(
        or_(
            Event.name.ilike(f"%{search_text}%"),
            Event.location.ilike(f"%{search_text}%"),
            Event.description.ilike(f"%{search_text}%")
        )
    ).offset(skip).limit(limit).all()
    return events

@app.post("/events/addEvent", response_model=EventResponse)
def add_event(event: EventCreate, db: Session = Depends(get_db)):
    db_event = Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@app.put("/events/{event_id}", response_model=EventResponse)
def edit_event(event_id: int, event: EventCreate, db: Session = Depends(get_db)):
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    for key, value in event.dict().items():
        setattr(db_event, key, value)
    db.commit()
    db.refresh(db_event)
    return db_event

@app.delete("/events/{event_id}", response_model=EventResponse)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    db.delete(db_event)
    db.commit()
    return db_event

# Combined Count Endpoint

@app.get("/counts")
def get_counts(search_text: str = Query("", min_length=0), db: Session = Depends(get_db)):
    search_text = f"%{search_text.lower()}%"
    events_count = db.query(func.count(Event.id)).filter(Event.name.ilike(search_text)).scalar()
    christians_count = db.query(func.count(Christian.id)).scalar()
    return {
        "events_count": events_count,
        "christians_count": christians_count
    }
