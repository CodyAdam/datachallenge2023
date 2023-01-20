from collections import defaultdict
import heapq


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
