import csv
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

num_christians = 500000
num_events = 50000

christians_file = "christians_dataset.csv"
events_file = "events_dataset.csv"

# Generate events data
events_data = [
    {
        "event_id": i + 1,
        "name": fake.company(),
        "location": fake.city(),
        "date": fake.date_between(start_date="-5y", end_date="today"),
        "description": fake.text(max_nb_chars=200),
        "status": random.choice(["upcoming", "ongoing", "completed"]),
        "created_at": fake.date_time_this_year(),
    }
    for i in range(num_events)
]

# Save events to CSV
with open(events_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["event_id", "name", "location", "date", "description", "status", "created_at"])
    writer.writeheader()
    writer.writerows(events_data)

print(f"Dataset with {num_events} events saved to {events_file}.")

# Generate Christians data
christians_data = [
    {
        "christian_id": i + 1,
        "event_id": random.randint(1, num_events),  # Link to an event
        "name": fake.name(),
        "email": fake.unique.email(),
        "phone": fake.phone_number(),
        "age": random.randint(18, 70),
        "gender": random.choice(["Male", "Female"]),
        "status": random.choice(["Active", "Inactive"]),
        "role": random.choice(["Diacon", "Pastor", "Usher"]),
        "joined_date": fake.date_between(start_date="-3y", end_date="today"),
        "created_at": fake.date_time_this_year(),
    }
    for i in range(num_christians)
]

# Save Christians to CSV
with open(christians_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file, 
        fieldnames=["christian_id", "event_id", "name", "email", "phone", "age", "gender", "status", "role", "joined_date", "created_at"]
    )
    writer.writeheader()
    writer.writerows(christians_data)

print(f"Dataset with {num_christians} Christians saved to {christians_file}.")
