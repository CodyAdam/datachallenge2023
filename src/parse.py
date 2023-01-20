from collections import defaultdict
import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
from geopandas import GeoDataFrame
import shapely.wkt
import json
import matplotlib.pyplot as plt


def parse():
    # lecture des données
    temps = pd.read_csv('data/temps_trajet30_filtered.csv',
                        delimiter=',',
                        encoding='utf-8')
    lvls = pd.read_csv('data/niveau_interventions_improved.csv',
                       delimiter=',',
                       usecols=[
                        'code_insee_commune',
                        'Niveau d\'activité clientèle',
                        'Niveau d\'activité réseau',
                        'Act_cli',
                        'Act_res',
                       ],
                       encoding='utf-8')
    communes = pd.read_csv('data/communes_bre.csv',
                           delimiter=';',
                           usecols=[
                               'Code Officiel Commune', 'Geo Shape',
                               'Nom Officiel Commune Majuscule', 'Geo Point'
                           ],
                           encoding='utf-8')
    communes = communes.merge(lvls,
                              left_on='Code Officiel Commune',
                              right_on='code_insee_commune')
    # communes = communes.head(100)

    # Convert the Geo Point column to a geometry column
    communes['geometry'] = communes['Geo Point'].apply(
        lambda x: shapely.wkt.loads(
            f'POINT({x.split(",")[1]} {x.split(",")[0]})'))

    nodes = []  # all the communes names
    for _, row in communes.iterrows():
        nodes.append(row['Nom Officiel Commune Majuscule'])

    edges = defaultdict(dict[str, int])  # all the vertexes with their distance
    for _, row in temps.iterrows():
        edges[row['depart']][row['destination']] = row['durée']

    values = defaultdict(lambda: 1)
    return communes, temps, nodes, edges, values

if __name__ == '__main__':
    print("Parsing data...")
    communes, temps, nodes, vertexes, values = parse()
    
    print(nodes[5])

    for i,k in enumerate(vertexes):
        print(k, vertexes[k])
        if i >= 1:
            break

