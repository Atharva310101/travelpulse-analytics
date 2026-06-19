with bookings as (
    select * from {{ ref('stg_bookings') }}
),
clients as (
    select * from {{ ref('stg_corporate_clients') }}
),
airlines as (
    select * from {{ ref('stg_airlines') }}
),
airports as (
    select * from {{ ref('stg_airports') }}
)

select
    b.booking_id,
    b.passenger_name,
    b.flight_date,
    b.advance_booking_days,
    b.booking_window_category,
    b.is_policy_compliant,
    b.booked_fare,
    
    -- Client details
    c.client_id,
    c.company_name,
    c.industry as client_industry,
    c.policy_tier as client_policy_tier,
    
    -- Airline details
    a.carrier_code,
    a.airline_name,
    
    -- Origin airport details
    orig.airport_code as origin_airport_code,
    orig.airport_name as origin_airport_name,
    orig.city as origin_city,
    orig.state as origin_state,
    
    -- Destination airport details
    dest.airport_code as destination_airport_code,
    dest.airport_name as destination_airport_name,
    dest.city as destination_city,
    dest.state as destination_state

from bookings b
left join clients c on b.client_id = c.client_id
left join airlines a on b.carrier_code = a.carrier_code
left join airports orig on b.origin_airport_code = orig.airport_code
left join airports dest on b.destination_airport_code = dest.airport_code