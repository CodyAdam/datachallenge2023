import parse
import geopandas as gpd
import matplotlib.pyplot as plt
from genetic import Population
import utils

print("Parsing data...")
communes, temps, nodes, edges, values = parse.parse()

print("Optimizing...")
edges = utils.optimize_edges(nodes, edges)

print("Creating GeoDataFrame...")
gdf = gpd.GeoDataFrame(communes, geometry='geometry')

print("Loading Brittany map...")
brittany = gpd.read_file(
    'data/bzh_shapefile/georef-france-commune-millesime.shp')

print("Generating population...")
base = 8
base = 30
base = 50
base = 40
base = 35
population = Population(20,
                        nodes,
                        edges,
                        values,
                        base_count=base,
                        mutation_rate=5/base)

fig = plt.figure()
figax = fig.add_subplot(111)
plt.ion()
plt.show()
print("Starting evolution...")
population.call_update_fitness()
plt.pause(2)
for i in range(1000):
    population.next_generation()
    best = population.best_individual
    print("Generation {:>2} : {:>10}".format(i, str(best)))
    if i % 10 == 0:
        utils.plot_individual(best,
                          communes,
                          nodes,
                          brittany,
                          i,
                          fig,
                          figax,
                          gdf,
                          pause=0.01,
                          base=base)

