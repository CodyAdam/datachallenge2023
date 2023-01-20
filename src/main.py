import parse
import geopandas as gpd
import matplotlib.pyplot as plt
from genetic import Population
import utils

print("Parsing data...")
communes, temps, nodes, edges, values = parse.parse()

print("Optimizing...")
edges = utils.optimize_edges(nodes, edges)

print("Generating population...")
population = Population(100,
                        nodes,
                        edges,
                        values,
                        base_count=5,
                        mutation_rate=0.1)

print("Starting evolution...")
for i in range(5):
    population.next_generation()
    print("Generation {:>2} - {:>2}: {:>10}".format(
        i, str(population.best_individual)))

print("Getting best solution...")
best = population.best_individual
base_names = []
for index, gene in enumerate(best.genes):
    if gene:
        base_names.append(nodes[index])
bases_positions = []

print("Creating GeoDataFrame...")
gdf = gpd.GeoDataFrame(communes, geometry='geometry')

# Association des bases à leurs coordonnées
solutions = []
for name in base_names:
    ## get the geometry of the commune
    communes_filtered = communes[communes['Nom Officiel Commune Majuscule'] ==
                                 name]
    solutions.append(gpd.GeoDataFrame(communes_filtered, geometry='geometry'))

print("Loading Brittany map...")
brittany = gpd.read_file(
    'data/bzh_shapefile/georef-france-commune-millesime.shp')
ax = brittany.plot(color='white', edgecolor='grey', figsize=(12, 6), alpha=0.2)

print("Plotting solution...")
gdf.plot(ax=ax, figsize=(12, 6), markersize=5)
for solution in solutions:
    solution.plot(ax=ax,
                  figsize=(12, 6),
                  markersize=1000,
                  color='red',
                  alpha=0.3)
plt.title('Communes de Bretagnes')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.xlim(-5.215, -0.798)  # zoom on brittany
plt.ylim(47.165, 48.984)

print("Showing plot...")
plt.show()