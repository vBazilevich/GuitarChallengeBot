CREATE TABLE "USER"
(
    id integer NOT NULL,
    level integer NOT NULL,
    status character varying COLLATE pg_catalog."default" NOT NULL,
    gmt integer,
    time_interval_start integer,
    time_interval_end integer,
    CONSTRAINT "USER_pkey" PRIMARY KEY (id)
)

CREATE TABLE "FEEDBACK"
(
    "author_id" integer NOT NULL,
    assessor_id integer NOT NULL,
    CONSTRAINT "FEEDBACK_pkey" PRIMARY KEY ("author_id", assessor_id)
)

CREATE TABLE "SONG"
(
    name character varying COLLATE pg_catalog."default" NOT NULL,
    author character varying COLLATE pg_catalog."default" NOT NULL,
    descr character varying COLLATE pg_catalog."default",
    image_link character varying COLLATE pg_catalog."default",
    CONSTRAINT "SONG_pkey" PRIMARY KEY (name, author)
)
