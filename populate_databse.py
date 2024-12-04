import random
from faker import Faker
from sqlalchemy.orm import Session
from datetime import datetime
from database import Base, engine, get_db  # Import database setup and dependencies
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey

# Faker setup
fake = Faker()

# Number of records to generate
num_christians = 5000  # Start small for testing
num_events = 500

# Define Events table
class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Define Christians table
class Christian(Base):
    __tablename__ = "christians"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    status = Column(String, nullable=False)
    role = Column(String, nullable=False)
    joined_date = Column(Date, nullable=False)
    # created_at = Column(DateTime, default=datetime.utcnow)

# Create tables in the database
Base.metadata.create_all(bind=engine)

# Generate events data
def generate_events(num_events):
    return [
        Event(
            id=i + 1,
            name=fake.company(),
            location=fake.city(),
            date=fake.date_between(start_date="-5y", end_date="today"),
            description=fake.text(max_nb_chars=200),
            status=random.choice(["upcoming", "ongoing", "completed"]),
            created_at=fake.date_time_this_year(),
        )
        for i in range(num_events)
    ]

def generate_christians(num_christians, db):
    event_ids = [event.id for event in db.query(Event).all()]
    return [
        Christian(
            id=i + 1,
            event_id=random.choice(event_ids),  
            name=fake.name(),
            email=fake.unique.email(),
            phone=fake.phone_number(),
            age=random.randint(18, 70),
            gender=random.choice(["Male", "Female"]),
            status=random.choice(["Active", "Inactive"]),
            role=random.choice(["Diacon", "Pastor", "Usher"]),
            joined_date=fake.date_between(start_date="-3y", end_date="today"),
        
        )
        for i in range(num_christians)
    ]

# Populate the database
def populate_database():
    with next(get_db()) as db:  # Use the database session dependency
        print("Generating events data...")
        events = generate_events(num_events)
        db.bulk_save_objects(events)
        db.commit()
        print(f"{num_events} events inserted.")

        print("Generating Christians data...")
        christians = generate_christians(num_christians, db)
        db.bulk_save_objects(christians)
        db.commit()
        print(f"{num_christians} Christians inserted.")

if __name__ == "__main__":
    populate_database()
    print("Data saved to the database.")
