create table public."CommunityArea"
(
    id       bigserial
        primary key,
    name     text                         not null,
    area     double precision             not null,
    len      double precision             not null,
    geometry geometry(MultiPolygon, 4326) not null
);

create index "idx_CommunityArea_geometry"
    on public."CommunityArea" using gist (geometry);


create table public."Point"
(
    id_trip           text                  not null
        constraint points_id_trip_foreign
            references public."Trip",
    id_community_area bigint                not null
        constraint points_community_area_foreign
            references public."CommunityArea",
    location          text                  not null,
    geometry          geometry(Point, 4326) not null,
    "isPick"          boolean               not null
);

alter table public."Point"
    owner to admin;

create index "idx_Point_geometry"
    on public."Point" using gist (geometry);

create table public."Taxi"
(
    id      text not null
        primary key,
    company text
);

alter table public."Taxi"
    owner to admin;

create table public."Trip"
(
    -- text can not be auto increment
    id           serial
        primary key,
    id_taxi      text             not null
        constraint trip_taxi_id_foreign
            references public."Taxi",
    "createAt"   timestamp        not null,
    "finishedAt" timestamp        not null,
    seconds      integer          not null,
    miles        double precision not null,
    fare         double precision not null,
    tips         double precision not null,
    tolls        double precision not null,
    extras       double precision not null,
    total_fare   double precision not null
);

alter table public."Trip"
    owner to admin;

