CREATE TABLE "Trip"(
    "ID" BIGINT NOT NULL,
    "taxi_ID" BIGINT NOT NULL,
    "start_Timestamp" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "end_Timestamp" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "seconds" INTEGER NOT NULL,
    "miles" DOUBLE PRECISION NOT NULL,
    "fare" DOUBLE PRECISION NOT NULL,
    "tips" DOUBLE PRECISION NULL,
    "tolls" DOUBLE PRECISION NULL,
    "extras" DOUBLE PRECISION NULL,
    "total_fare" DOUBLE PRECISION NOT NULL
);
ALTER TABLE
    "Trip" ADD PRIMARY KEY("ID");
ALTER TABLE
    "Trip" ADD CONSTRAINT "trip_taxi_id_unique" UNIQUE("taxi_ID");
CREATE TABLE "Points"(
    "id_trip" INTEGER NOT NULL,
    "community_area" BIGINT NOT NULL,
    "location" TEXT NOT NULL,
    "geometry" geography(POINT, 4326) NOT NULL,
    "isPick" BOOLEAN NOT NULL
);
ALTER TABLE
    "Points" ADD CONSTRAINT "points_id_trip_unique" UNIQUE("id_trip");
ALTER TABLE
    "Points" ADD CONSTRAINT "points_community_area_unique" UNIQUE("community_area");
CREATE TABLE "Community Area"(
    "id" INTEGER NOT NULL,
    "name" TEXT NOT NULL,
    "area" DOUBLE PRECISION NOT NULL,
    "len" DOUBLE PRECISION NOT NULL,
    "geometry" geography(MULTIPOLYGON, 4326) NOT NULL
);
ALTER TABLE
    "Community Area" ADD PRIMARY KEY("id");
CREATE TABLE "Taxi"(
    "id" INTEGER NOT NULL,
    "company" TEXT NOT NULL
);
ALTER TABLE
    "Taxi" ADD PRIMARY KEY("id");
ALTER TABLE
    "Trip" ADD CONSTRAINT "trip_taxi_id_foreign" FOREIGN KEY("taxi_ID") REFERENCES "Taxi"("id");
ALTER TABLE
    "Points" ADD CONSTRAINT "points_id_trip_foreign" FOREIGN KEY("id_trip") REFERENCES "Trip"("ID");
ALTER TABLE
    "Points" ADD CONSTRAINT "points_community_area_foreign" FOREIGN KEY("community_area") REFERENCES "Community Area"("id");