import pandas as pd
import math

# Calculate the Euclidean distance between two cities
def euclidean_distance(city1, city2):
    lat1, lon1 = city1[:2]
    lat2, lon2 = city2[:2]
    return math.sqrt((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2)

# Create the distance matrix based on the city data
def create_distance_matrix(city_data):
    n = len(city_data)
    distance_matrix = [[0] * n for _ in range(n)]  # Initialize distance matrix with all elements set to 0
    for i in range(n):
        for j in range(n):
            if i != j:
                distance_matrix[i][j] = euclidean_distance(city_data[i], city_data[j])
    return distance_matrix

# Solve the TSP using BFS search
def bfs_search(distance_matrix, start_city, city_names):
    n = len(distance_matrix)
    visited = [False] * n  # Keep track of visited cities
    visited[start_city] = True  # Mark the start city as visited
    route = [(start_city, city_names[start_city])]  # Store the current route
    shortest_distance = float('inf')  # Initialize the shortest distance to infinity
    shortest_route = None  # Initialize the shortest route as None

    # Recursive function to explore all possible paths
    def backtrack(current_city, current_route, current_distance, shortest_dist, shortest_rt):
        # Base case: If all cities have been visited, check if this route is the shortest
        if len(current_route) == n:
            total_distance = current_distance + distance_matrix[current_route[-1][0]][start_city]
            if total_distance < shortest_dist:
                shortest_dist = total_distance
                shortest_rt = current_route
            return shortest_dist, shortest_rt

        # Iterate over next possible cities to visit
        for next_city in range(n):
            if not visited[next_city]:
                visited[next_city] = True  # Mark the city as visited
                shortest_dist, shortest_rt = backtrack(
                    next_city,
                    current_route + [(next_city, city_names[next_city])],
                    current_distance + distance_matrix[current_city][next_city],
                    shortest_dist,
                    shortest_rt
                )
                visited[next_city] = False  # Mark the city as unvisited for other possible paths

        return shortest_dist, shortest_rt

    # Call the backtrack function to find the shortest distance and route
    shortest_distance, shortest_route = backtrack(start_city, route, 0, shortest_distance, shortest_route)

    return shortest_distance, [city_name for city_index, city_name in shortest_route]


# Read the city data from CSV file
city_data = pd.read_csv('city_data_50.csv', usecols=['latitude', 'longitude']).values.tolist()
city_names = pd.read_csv('city_data_50.csv', usecols=['name']).values.flatten().tolist()

# Create the distance matrix
distance_matrix = create_distance_matrix(city_data)

# Solve TSP using BFS search
start_city = 0  # Start from the first city
shortest_distance, shortest_route = bfs_search(distance_matrix, start_city, city_names)

# Print the shortest distance and route
print('Shortest Distance:', shortest_distance)
print('Shortest Route:', shortest_route)
