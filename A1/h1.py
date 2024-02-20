import csv
import math

# Step 1: Read city data from CSV file
def read_city_data(filename):
    city_data = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader):
            if i < 10: # Add this condition to limit to the first 10 cities
                city_data.append(row)
            else:
                break
    return city_data
# Step 2: Calculate distance matrix
def calculate_distance_matrix(city_data):
    distance_matrix = []
    for i in range(len(city_data)):
        distances = []
        lat1 = float(city_data[i]['latitude'])
        lon1 = float(city_data[i]['longitude'])
        for j in range(len(city_data)):
            lat2 = float(city_data[j]['latitude'])
            lon2 = float(city_data[j]['longitude'])
            distance = math.sqrt((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2)
            distances.append(distance)
        distance_matrix.append(distances)
    return distance_matrix

# Step 3: Depth-first search (DFS) algorithm
def dfs(city_data, distance_matrix, current_city, visited, distance, path):
    if len(visited) == len(city_data):
        return distance, path

    min_distance = float('inf')
    min_path = None

    for i in range(len(city_data)):
        if i not in visited:
            next_city = city_data[i]['name']
            new_distance = distance + distance_matrix[current_city][i]
            visited.add(i)
            new_path = path + [next_city]
            result = dfs(city_data, distance_matrix, i, visited, new_distance, new_path)
            if result[0] < min_distance:
                min_distance = result[0]
                min_path = result[1]
            visited.remove(i)

    return min_distance, min_path

""" # Step 4: Breadth-first search (BFS) algorithm
def bfs(city_data, distance_matrix):
    queue = [(i, [city_data[i]['name']]) for i in range(len(city_data))]
    min_distance = float('inf')
    min_path = None

    while queue:
        current_city, path = queue.pop(0)
        if len(path) == len(city_data):
            distance = calculate_path_distance(path, distance_matrix)
            if distance < min_distance:
                min_distance = distance
                min_path = path
        else:
            for i in range(len(city_data)):
                if city_data[i]['name'] not in path:
                    next_city = city_data[i]['name']
                    new_path = path + [next_city]
                    queue.append((i, new_path))

    return min_distance, min_path

# Helper function to calculate the total distance of a path
def calculate_path_distance(path, distance_matrix):
    distance = 0
    for i in range(len(path) - 1):
        city1 = path[i]
        city2 = path[i + 1]
        distance += distance_matrix[city_data.index(city1)][city_data.index(city2)]
    return distance """

# Main program
city_data = read_city_data('city_data_50.csv')
distance_matrix = calculate_distance_matrix(city_data)

# Perform Depth-first search
start_city = city_data[0]['name']
visited = set([0])
distance, path = dfs(city_data, distance_matrix, 0, visited, 0, [start_city])
print("Depth-first search:")
print("Shortest distance:", distance)
print("Shortest path:", ' -> '.join(path))

""" # Perform Breadth-first search
distance, path = bfs(city_data, distance_matrix)
print("\nBreadth-first search:")
print("Shortest distance:", distance)
print("Shortest path:", ' -> '.join(path)) """