with plays as (
    select
        game_id,
        season,
        cast(fetched_at as timestamp) as fetched_at,
        unnest(payload.plays) as play
    from {{ source('landing', 'games') }}
),

flat as (
    select
        game_id,
        season,
        fetched_at,
        cast(play.eventId as integer)      as event_id,
        play.typeDescKey                   as event_type,
        play.periodDescriptor.number       as period,
        play.timeInPeriod                  as time_in_period,
        cast(split_part(play.timeInPeriod, ':', 1) as integer) * 60
          + cast(split_part(play.timeInPeriod, ':', 2) as integer) as seconds_in_period
    from plays
)

select * from flat
qualify row_number() over (
    partition by game_id, event_id order by fetched_at desc
) = 1