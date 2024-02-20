import math
import pandas as pd

def euclidean_distance(location1, location2):
    lat1, long1 = location1
    lat2, long2 = location2
    return math.sqrt((lat2 - lat1)**2 + (long2 - long1)**2)

def create_distance_matrix(location_list):
    list_size = len(location_list)
    distance_matrix = [[0] * list_size for _ in range(list_size)]
    
    for i in range(list_size):
        for j in range(list_size):
            if i != j:
                distance_matrix[i][j] = euclidean_distance(location_list[i], location_list[j])
    
    return distance_matrix

def bfs_algorithm(distance_matrix, name_list):
    matrix_size = len(distance_matrix)
    start = 0
    visited = [False] * matrix_size
    visited[start] = True
    visited_path = [(start, name_list[start][0])]
    
    def solve(current_distance, current_path, shortest_distance, shortest_path):
        if len(current_path) == matrix_size:
            total_distance = current_distance + distance_matrix[current_path[-1][0]][start]
            if total_distance < shortest_distance[0]:
                shortest_distance[0] = total_distance
                shortest_path[0] = current_path
            return

        for next_location in range(matrix_size):
            if not visited[next_location]:
                visited[next_location] = True
                next_city = name_list[next_location][0]
                next_distance = distance_matrix[current_path[-1][0]][next_location]
                solve(current_distance + next_distance, current_path + [(next_location, next_city)], shortest_distance, shortest_path)
                visited[next_location] = False

    shortest_distance = [float('inf')]
    shortest_path = [None]
    solve(0, visited_path, shortest_distance, shortest_path)
    return shortest_distance[0], shortest_path[0]


# Read the city data from CSV file
df = pd.read_csv("city_data_50.csv")

# Extract the location values into a list
location_list = df[['latitude', 'longitude']].values.tolist()

# Extract the name values into a list
name_list = df[['name']].values.tolist()

# Create the distance matrix
distance_matrix = create_distance_matrix(location_list)

# Solve TSP using BFS algorithm
shortest_distance, shortest_path = bfs_algorithm(distance_matrix, name_list)

# Extract the city names from the shortest path
city_names = [name_list[i][0] for i, _ in shortest_path]

# Print the shortest distance and path
print('Shortest Distance:', shortest_distance)
print('Shortest Path:', city_names)
