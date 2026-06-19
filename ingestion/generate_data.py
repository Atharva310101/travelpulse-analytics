import os
import random
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta

# Initialize Faker and seed for reproducibility
fake = Faker()
Faker.seed(42)
random.seed(42)

# Ensure the data directory exists
os.makedirs("data", exist_ok=True)

# 1. Define Static Reference Data: Major US Airports
airports_data = [
    {"iata_code": "ATL", "airport_name": "Hartsfield-Jackson Atlanta International", "city": "Atlanta", "state": "GA"},
    {"iata_code": "LAX", "airport_name": "Los Angeles International", "city": "Los Angeles", "state": "CA"},
    {"iata_code": "ORD", "airport_name": "O'Hare International", "city": "Chicago", "state": "IL"},
    {"iata_code": "DFW", "airport_name": "Dallas/Fort Worth International", "city": "Dallas", "state": "TX"},
    {"iata_code": "DEN", "airport_name": "Denver International", "city": "Denver", "state": "CO"},
    {"iata_code": "JFK", "airport_name": "John F. Kennedy International", "city": "New York", "state": "NY"},
    {"iata_code": "SFO", "airport_name": "San Francisco International", "city": "San Francisco", "state": "CA"},
    {"iata_code": "SEA", "airport_name": "Seattle-Tacoma International", "city": "Seattle", "state": "WA"},
    {"iata_code": "LAS", "airport_name": "Harry Reid International", "city": "Las Vegas", "state": "NV"},
    {"iata_code": "MCO", "airport_name": "Orlando International", "city": "Orlando", "state": "FL"},
    {"iata_code": "EWR", "airport_name": "Newark Liberty International", "city": "Newark", "state": "NJ"},
    {"iata_code": "CLT", "airport_name": "Charlotte Douglas International", "city": "Charlotte", "state": "NC"},
    {"iata_code": "MIA", "airport_name": "Miami International", "city": "Miami", "state": "FL"},
    {"iata_code": "PHX", "airport_name": "Phoenix Sky Harbor International", "city": "Phoenix", "state": "AZ"},
    {"iata_code": "BOS", "airport_name": "Boston Logan International", "city": "Boston", "state": "MA"}
]
df_airports = pd.DataFrame(airports_data)

# 2. Define Static Reference Data: Major US Airlines
airlines_data = [
    {"carrier_code": "DL", "airline_name": "Delta Air Lines"},
    {"carrier_code": "UA", "airline_name": "United Airlines"},
    {"carrier_code": "AA", "airline_name": "American Airlines"},
    {"carrier_code": "WN", "airline_name": "Southwest Airlines"},
    {"carrier_code": "B6", "airline_name": "JetBlue Airways"},
    {"carrier_code": "AS", "airline_name": "Alaska Airlines"}
]
df_airlines = pd.DataFrame(airlines_data)

# 3. Generate Synthetic Corporate Clients
industries = ["Technology", "Finance", "Healthcare", "Energy", "Manufacturing", "Consulting"]
policy_tiers = ["Bronze", "Silver", "Gold"]

clients = []
for i in range(1, 101):  # 100 Corporate Clients
    clients.append({
        "client_id": f"CLNT{i:03d}",
        "company_name": fake.company(),
        "industry": random.choice(industries),
        "policy_tier": random.choice(policy_tiers)
    })
df_clients = pd.DataFrame(clients)

# 4. Generate Synthetic Flight Bookings (Fact Table)
bookings = []
start_date = datetime(2023, 1, 1)

for i in range(1, 15001):  # 15,000 individual bookings
    client = random.choice(clients)
    carrier = random.choice(airlines_data)
    
    # Pick distinct origin and destination airports
    origin = random.choice(airports_data)
    dest = random.choice(airports_data)
    while dest["iata_code"] == origin["iata_code"]:
        dest = random.choice(airports_data)
        
    # Generate dates
    random_days = random.randint(0, 450)  # Covers ~15 months
    flight_date = start_date + timedelta(days=random_days)
    
    # Policy adherence logical connection:
    # Bookings made further in advance are cheaper and highly policy-compliant.
    # Last-minute bookings (< 7 days) are expensive and often violate corporate policy.
    advance_booking_days = random.randint(1, 30)
    
    if advance_booking_days >= 14:
        booked_fare = round(random.uniform(150.0, 450.0), 2)
        policy_compliant = True if random.random() < 0.95 else False
    elif advance_booking_days >= 7:
        booked_fare = round(random.uniform(300.0, 750.0), 2)
        policy_compliant = True if random.random() < 0.75 else False
    else:
        booked_fare = round(random.uniform(600.0, 1400.0), 2)
        policy_compliant = True if random.random() < 0.30 else False

    bookings.append({
        "booking_id": f"BKG{i:06d}",
        "client_id": client["client_id"],
        "passenger_name": fake.name(),
        "flight_date": flight_date.strftime("%Y-%m-%d"),
        "origin_airport": origin["iata_code"],
        "destination_airport": dest["iata_code"],
        "carrier_code": carrier["carrier_code"],
        "booked_fare": booked_fare,
        "advance_booking_days": advance_booking_days,
        "policy_compliant": policy_compliant
    })

df_bookings = pd.DataFrame(bookings)

# 5. Save datasets to CSV
df_airports.to_csv("data/dim_airports.csv", index=False)
df_airlines.to_csv("data/dim_airlines.csv", index=False)
df_clients.to_csv("data/dim_corporate_clients.csv", index=False)
df_bookings.to_csv("data/fact_bookings.csv", index=False)

print("Data generation complete. Files created in 'data/' directory:")
print(" - data/dim_airports.csv (15 rows)")
print(" - data/dim_airlines.csv (6 rows)")
print(" - data/dim_corporate_clients.csv (100 rows)")
print(" - data/fact_bookings.csv (15,000 rows)")