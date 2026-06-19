select
    carrier_code,
    airline_name
from {{ source('raw_travelpulse', 'dim_airlines') }}