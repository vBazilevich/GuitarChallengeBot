CREATE TABLE song
(
    song_id serial PRIMARY KEY NOT NULL,
    name character varying COLLATE pg_catalog."default" NOT NULL,
    author character varying COLLATE pg_catalog."default" NOT NULL,
    descr character varying COLLATE pg_catalog."default",
    image_link character varying COLLATE pg_catalog."default"
)

CREATE TABLE bot_user
(
    user_id integer PRIMARY KEY NOT NULL,
    level integer REFERENCES song(song_id),
    status character varying COLLATE pg_catalog."default" NOT NULL,
    gmt integer,
    time_interval_start integer,
    time_interval_end integer
)

CREATE TABLE feedback
(
    feedback_id serial PRIMARY KEY NOT NULL,
    author_id integer REFERENCES bot_user(user_id),
    assessor_id integer REFERENCES bot_user(user_id)
)
