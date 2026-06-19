select
    iata_code as airport_code,
    airport_name,
    city,
    state
from {{ source('raw_travelpulse', 'dim_airports') }}