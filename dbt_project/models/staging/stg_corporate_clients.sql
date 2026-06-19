select
    client_id,
    company_name,
    industry,
    policy_tier
from {{ source('raw_travelpulse', 'dim_corporate_clients') }}