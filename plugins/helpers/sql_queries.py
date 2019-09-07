class SqlQueries:
    songplay_table_insert = ("""
        INSERT INTO songplays 
        (startTime, userid, level, songid, artistid, sessionid, location, userAgent)
        select TIMESTAMP 'epoch' + ts/1000*INTERVAL '1 second' as starttime
              ,e.userid
              ,e.level
              ,s.song_id
              ,s.artist_id
              ,e.sessionid
              ,e.location
              ,e.userAgent
        FROM staging_events as e
        JOIN staging_songs as s
            on e.song = s.title
        where e.page = 'NextSong'
    """)

    user_table_insert = ("""
        INSERT INTO users
        (userid, firstName, lastName, gender, level)
        select distinct userid
              ,firstName
              ,lastName
              ,gender
              ,level
        FROM staging_events 
        where page = 'NextSong'
        and userid is not null
    """)

    song_table_insert = ("""
        INSERT INTO songs
        (songid, title, artistid, year, duration)
        select distinct song_id
              ,title
              ,artist_id
              ,year
              ,duration
        from staging_songs 
    """)

    artist_table_insert = ("""
        INSERT INTO artists
        (artistid, artistName, artistLocation, artistLatitude, artistLongitude)
        select distinct artist_id
              ,artist_name
              ,artist_location
              ,artist_latitude
              ,artist_longitude
        FROM staging_songs
    """)

    time_table_insert = ("""
    INSERT INTO time
    (starttime, hour, day, week, month, year, weekday)
    select distinct starttime
          ,extract(hr from starttime) as hour
          ,extract(d from starttime) as day
          ,extract(w from starttime) as week
          ,extract(mon from starttime) as month
          ,extract(yr from starttime) as year
          ,extract(weekday from starttime) as weekday
    FROM (
        select distinct 
               TIMESTAMP 'epoch' + ts/1000*INTERVAL '1 second' as starttime
        from staging_events
        where starttime is not null
    ) as e
    """)