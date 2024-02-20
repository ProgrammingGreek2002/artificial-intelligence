import pandas as pd
from math import radians, sin, cos, sqrt, atan2

# Read the data from the CSV file
df = pd.read_csv('city_data_50.csv')

# Calculate the distance matrix using the Haversine formula
def distance(city1, city2):
    lat1, lon1 = radians(city1['latitude']), radians(city1['longitude'])
    lat2, lon2 = radians(city2['latitude']), radians(city2['longitude'])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return 6373.0 * c
print("jello1")
n = len(df)
dist_matrix = [[distance(df.iloc[i], df.iloc[j]) for j in range(n)] for i in range(n)]

def dfs_tsp(dist_matrix):
    n = len(dist_matrix)
    stack = [(i, [i], 0) for i in range(n)]
    min_path = None
    min_dist = float('inf')
    while stack:
        (v, path, dist) = stack.pop()
        if len(path) == n:
            if dist + dist_matrix[v][0] < min_dist:
                min_path = path + [0]
                min_dist = dist + dist_matrix[v][0]
        else:
            for u in range(n):
                if u not in path:
                    stack.append((u, path + [u], dist + dist_matrix[v][u]))
    return min_dist, [df.iloc[i]['name'] for i in min_path]
print("jello2")

def bfs_tsp(dist_matrix):
    n = len(dist_matrix)
    queue = [(i, [i], 0) for i in range(n)]
    min_path = None
    min_dist = float('inf')
    while queue:
        (v, path, dist) = queue.pop(0)
        if len(path) == n:
            if dist + dist_matrix[v][0] < min_dist:
                min_path = path + [0]
                min_dist = dist + dist_matrix[v][0]
        else:
            for u in range(n):
                if u not in path:
                    queue.append((u, path + [u], dist + dist_matrix[v][u]))
    return min_dist, [df.iloc[i]['name'] for i in min_path]
print("jello3")
def astar_tsp(dist_matrix):
    n = len(dist_matrix)
    open_set = [(0, [0], 0, [0])]
    closed_set = set()
    min_path = None
    min_dist = float('inf')
    while open_set:
        _, path, dist, h_values = min(open_set)
        v = path[-1]
        open_set.remove((dist + h_values[-1], path, dist, h_values))
        if len(path) == n:
            if dist + dist_matrix[v][0] < min_dist:
                min_path = path + [0]
                min_dist = dist + dist_matrix[v][0]
        else:
            for u in range(n):
                if u != v and u not in closed_set:
                    open_set.append((dist + dist_matrix[v][u] + h_values[-1] - h_values[v], path+[u], dist+dist_matrix[v][u], h_values + [h_values[-1] - h_values[v] + dist_matrix[v][u]]))
        closed_set.add(v)
    return min_dist, [df[i]['name'] for i in min_path]
print("jello4")