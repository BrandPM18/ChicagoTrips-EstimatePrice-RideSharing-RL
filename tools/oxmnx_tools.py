import osmnx as ox
import geopandas as gpd
from shapely import wkt

place_name = "Chicago, Illinois, United States"
def search(gp_nodes,point_obj):
    gp_nodes_ = gp_nodes.copy()
    gp_nodes_['distance'] = [geom.distance(point_obj.geometry[0]) for geom in gp_nodes_.geometry]
    return gp_nodes_.sort_values(by=['distance']).index[0]

def create_route_path(nodes, graph):
    path_final = []
    for i in range(len(nodes)-1):
        path = ox.distance.shortest_path(
            G=graph,
            orig=nodes[i],
            dest=nodes[i+1],
            weight='length')
        if i == len(nodes)-1:
            path_final.extend(path)
        else:
            path_final.extend(path[:len(path)-1])
    return path_final

def plot_map(route, graph):
    graph = ox.graph_from_place(place_name,network_type='drive')
    nodes, edges = ox.graph_to_gdfs(graph)
    pointsNodes = gpd.GeoDataFrame(nodes,geometry=nodes['geometry'].astype(str).apply(wkt.loads),crs="EPSG:4326")
    route_nodes = [search(pointsNodes,point) for point in route]
    fig, ax = ox.plot_graph_route(graph,create_route_path(route_nodes,graph))
