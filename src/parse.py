from collections import defaultdict
import pandas as pd
import shapely.wkt


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
    # communes = communes.sample(20)

    # Convert the Geo Point column to a geometry column
    communes['geometry'] = communes['Geo Point'].apply(
        lambda x: shapely.wkt.loads(
            f'POINT({x.split(",")[1]} {x.split(",")[0]})'))

    nodes = []  # all the communes names
    values = defaultdict(lambda: 1)
    for _, row in communes.iterrows():
        node = row['Nom Officiel Commune Majuscule']
        nodes.append(node)
        values[node] = (row['Act_cli'] + row['Act_res']) / 2

    edges = defaultdict(dict[str, int])  # all the edges with their distance
    for _, row in temps.iterrows():
        edges[row['depart']][row['destination']] = row['durée']

    return communes, temps, nodes, edges, values


if __name__ == '__main__':
    print("Parsing data...")
    communes, temps, nodes, edges, values = parse()

    print(nodes[5])

    for i, k in enumerate(edges):
        print(k, edges[k])
        if i >= 1:
            break
