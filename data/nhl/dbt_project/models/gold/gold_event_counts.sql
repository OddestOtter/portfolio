select season, event_type, count(*) as n_events
from {{ ref('silver_events') }}
group by all