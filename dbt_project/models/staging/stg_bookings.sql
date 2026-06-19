select
    booking_id,
    client_id,
    passenger_name,
    cast(flight_date as date) as flight_date,
    origin_airport as origin_airport_code,
    destination_airport as destination_airport_code,
    carrier_code,
    cast(booked_fare as numeric) as booked_fare,
    cast(advance_booking_days as int64) as advance_booking_days,
    cast(policy_compliant as bool) as is_policy_compliant,
    
    -- Derived business metric: Grouping advance bookings into clear categories
    case 
        when advance_booking_days >= 14 then 'Standard (14+ Days)'
        when advance_booking_days >= 7 then 'Short Notice (7-13 Days)'
        else 'Last Minute (0-6 Days)'
    end as booking_window_category
from {{ source('raw_travelpulse', 'fact_bookings') }}