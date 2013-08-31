DROP TABLE IF EXISTS public.epicpython_incoming;
DROP TABLE IF EXISTS public.info;

CREATE TABLE public.epicpython_incoming (
name varchar(255) not null,
position varchar(255) not null,
time_generated timestamp with time zone not null
);

CREATE TABLE public.info (
name varchar(255) not null,
position varchar(255) not null,
time_generated timestamp with time zone not null
);
