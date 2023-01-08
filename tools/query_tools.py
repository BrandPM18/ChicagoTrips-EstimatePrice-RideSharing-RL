from sqlalchemy import create_engine
import geopandas as gpd
import pandas as pd


class SQLTool:
    def __init__(self, engine_url):
        # Engine SQLAlchemy
        self.engine_url = engine_url

    def isDiffPoints(self, id_trip):
        consult_sql_pick = f'SELECT * FROM public.\"Point\"  WHERE id_trip = \'{id_trip}\' AND \"isPick\" = true'
        consult_sql_drop = f'SELECT * FROM public.\"Point\"  WHERE id_trip = \'{id_trip}\' AND \"isPick\" = false'
        gp_drop = gpd.read_postgis(
            sql=consult_sql_drop,
            con=self.engine_url,
            geom_col='geometry',
            crs='EPSG:4326')
        gp_pick = gpd.read_postgis(
            sql=consult_sql_pick,
            con=self.engine_url,
            geom_col='geometry',
            crs='EPSG:4326')
        if gp_pick['id_community_area'][0] != gp_drop['id_community_area'][0]:
            return True
        print("Validate Points")
        print(gp_pick['id_trip'][0],": ",gp_pick['geometry'][0].distance(gp_drop['geometry'][0]))
        return gp_pick['geometry'][0].distance(gp_drop['geometry'][0]) != 0.0

    def search_trips(self, offset, count):
        consult_sql = f'SELECT * FROM public.\"Trip\" OFFSET {offset} LIMIT {count}'
        return pd.read_sql(
            sql=consult_sql,
            con=self.engine_url
        )

    def get_point_trip(self, list):
        consult_sql = f'SELECT * FROM public.\"Point\" WHERE id_trip in {tuple(list)}'
        value_points = gpd.read_postgis(
            sql=consult_sql,
            con='postgresql://admin:admin@localhost:5433/taxis_db',
            geom_col='geometry',
            crs='EPSG:4326'
        )
        return value_points[value_points['isPick'] == True], value_points[value_points['isPick'] == False]

    def rand_trips(self, count):
        consult_sql = f'SELECT * FROM public.\"Trip\" ORDER BY  random() LIMIT {count}'
        pd_trips = pd.read_sql(
            sql=consult_sql,
            con=self.engine_url
        )
        for i in range(count):
            if not self.isDiffPoints(pd_trips['id'][i]):
                print("Trip invalido por puntos iguales")
                pd_trips = pd.read_sql(
                    sql=consult_sql,
                    con=self.engine_url
                )
        return pd_trips

class SQLTripTool:
    def __init__(self, id_trip, id_taxi, id_community_area, engine_url):
        self.id_trip = id_trip
        self.id_taxi = id_taxi
        self.id_community_area = id_community_area

        # Engine SQLAlchemy
        self.engine_url = engine_url
        self.engine = create_engine(engine_url)

    def sql_pickup(self):
        consult_sql = f'SELECT * FROM public.\"Point\" WHERE id_trip = \'{self.id_trip}\' AND \"isPick\" = true'
        return gpd.read_postgis(
            sql=consult_sql,
            con=self.engine_url,
            geom_col='geometry',
            crs='EPSG:4326')

    def sql_drop(self):
        consult_sql = f'SELECT * FROM public.\"Point\" WHERE id_trip = \'{self.id_trip}\' AND \"isPick\" = false'
        return gpd.read_postgis(
            sql=consult_sql,
            con=self.engine_url,
            geom_col='geometry',
            crs='EPSG:4326')

    def sql_taxi(self):
        consult_sql = f'SELECT * FROM public.\"Point\" WHERE id_trip = \'{self.id_trip}\' AND \"isPick\" = false'
        return gpd.read_postgis(
            sql=consult_sql,
            con=self.engine_url,
            geom_col='geometry',
            crs='EPSG:3035')

    def set_id_trip(self, id_trip):
        self.id_trip = id_trip

# %%
