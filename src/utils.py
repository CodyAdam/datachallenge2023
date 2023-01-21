from collections import defaultdict
import heapq
import geopandas as gpd
import matplotlib.pyplot as plt


def plot_individual(best,
                    communes,
                    nodes,
                    brittany,
                    i,
                    fig,
                    figax,
                    gdf,
                    pause=0.5,
                    base=None):
    # print("Plotting Map...")
    ax = brittany.plot(ax=figax,
                       color='white',
                       edgecolor='grey',
                       figsize=(22, 12),
                       alpha=0.3)
    gdf.plot(ax=ax, figsize=(12, 6), markersize=10, color='green', alpha=0.3)
    plt.title(f'Communes de Bretagnes - Generation {i}')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.xlim(-5.215, -0.798)  # zoom on brittany
    plt.ylim(47.165, 48.984)
    plt.text(.01, .99, f'Fitness: {best.fitness}',ha='left', va='top', transform=ax.transAxes)
    plt.text(.01, .95, f'Nombre de bases: {best.base_count}',ha='left', va='top', transform=ax.transAxes)
    plt.text(.01, .90, f'Communes sans base: {len(best.without_bases)}' ,ha='left', va='top', transform=ax.transAxes)
    plt.text(.01, .85, f'Temps moyen déplacement: {best.avg_dist_to_base}s',ha='left', va='top', transform=ax.transAxes)
    base_names = []
    for gene in best.genes:
        base_names.append(nodes[gene])

    # Association des bases à leurs coordonnées
    bases = []
    for name in base_names:
        ## get the geometry of the commune
        communes_filtered = communes[communes['Nom Officiel Commune Majuscule']
                                     == name]
        bases.append(gpd.GeoDataFrame(communes_filtered, geometry='geometry'))
    not_covered = []
    for without_base in best.without_bases:
        communes_filtered = communes[communes['Nom Officiel Commune Majuscule']
                                     == without_base]
        not_covered.append(
            gpd.GeoDataFrame(communes_filtered, geometry='geometry'))

    for commune in not_covered:
        commune.plot(ax=ax,
                     figsize=(12, 6),
                     markersize=20,
                     color='red',
                     alpha=1)
    for b in bases:
        b.plot(ax=ax, figsize=(12, 6), markersize=60, color='blue', alpha=0.6)

    # clear the figure
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.savefig(
        f'./data/img/{("b" + str(base)) + "_" if base else ""}gen_{i}.png',
        bbox_inches='tight')
    plt.pause(pause)
    plt.cla()


def optimize_edges(nodes, edges):
    optimized = defaultdict(lambda: defaultdict(lambda: float('infinity')))
    for start in nodes:
        dist_from_node = dijkstra30min(start, nodes, edges)
        for end in nodes:
            optimized[start][end] = dist_from_node[end]
    return optimized


def dijkstra30min(start, nodes, edges):
    distances = defaultdict(lambda: float('infinity'))
    distances[start] = 0
    queue = [(0, start)]
    while queue:
        current_distance, current_node = heapq.heappop(queue)
        if current_distance > distances[current_node]:
            continue
        if current_node not in edges:
            continue
        for neighbor, weight in edges[current_node].items():
            distance = current_distance + weight
            if distance < 30 * 60 and distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))
    return distances


if __name__ == "__main__":
    # nodes, edges
    nodes = ["1", "2", "3", "4", "5", "6"]
    edges = {}
    edges["1"] = {"2": 7 * 60, "3": 9 * 60, "6": 14 * 60}
    edges["2"] = {"1": 7 * 60, "3": 10 * 60, "4": 15 * 60}
    edges["3"] = {"1": 9 * 60, "2": 10 * 60, "4": 25 * 60, "6": 2 * 60}
    edges["4"] = {"2": 15 * 60, "3": 25 * 60, "5": 12 * 60}
    edges["5"] = {"4": 12 * 60, "6": 24 * 60}
    edges["6"] = {"1": 14 * 60, "3": 2 * 60, "5": 24 * 60}

    print(dijkstra30min("1", nodes, edges))
    res = optimize_edges(nodes, edges)
    for k in res:
        print(k, res[k])
