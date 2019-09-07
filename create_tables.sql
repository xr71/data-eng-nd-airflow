CREATE TABLE IF NOT EXISTS staging_events (
 artist text
,auth text
,firstName text
,gender text
,itemInSession text
,lastName text
,length text
,level text
,location text
,method text
,page text
,registration text
,sessionid int
,song text
,status text
,ts text
,userAgent text
,userid int
);


CREATE TABLE IF NOT EXISTS staging_songs (
num_songs integer
,artist_id text
,artist_latitude double precision
,artist_longitude double precision
,artist_location text
,artist_name text
,song_id text PRIMARY KEY
,title text
,duration double precision
,year integer
);


CREATE TABLE IF NOT EXISTS songplays (
songplayid integer PRIMARY KEY IDENTITY(0,1)
,startTime timestamp sortkey
,userid text 
,level text
,songid text
,artistid text
,sessionid text
,location text
,userAgent text
);


CREATE TABLE IF NOT EXISTS users (
userid text PRIMARY KEY
,firstName text
,lastName text
,gender text
,level text
) DISTSTYLE ALL;



CREATE TABLE IF NOT EXISTS songs (
songid text PRIMARY KEY
,title text
,artistid text sortkey
,year integer
,duration double precision
) DISTSTYLE ALL;


CREATE TABLE IF NOT EXISTS artists (
artistid text PRIMARY KEY
,artistName text
,artistLocation text
,artistLatitude double precision
,artistLongitude double precision
) DISTSTYLE ALL;


CREATE TABLE IF NOT EXISTS time (
startTime timestamp PRIMARY KEY
,hour integer
,day integer
,week integer
,month integer
,year integer
,weekday text
) DISTSTYLE ALL;
