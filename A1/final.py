'''
Gurraj Singh
190128350
Ninam Rai
200619540
CP468
Make sure to have csv in same directory

Install pip below
pip install pandas
'''
import pandas as pd
import math

#City object to store values from csv file
class City:
    def __init__(self, name, description, latitude, longitude):
        self.name = name
        self.description = description
        self.latitude = latitude
        self.longitude = longitude




#Function that calculates the euclidian distance between the cities
def calculate_distance(city1,city2):
    lat1, lon1 = city1.latitude, city1.longitude
    lat2, lon2 = city2.latitude, city2.longitude
    distance = math.sqrt((lat2-lat1)**2 + (lon2-lon1)**2)

    return distance

#Function that creates the distance matrix to be used in the depth search
def distance_matrix_dfs(cities):
    numberOfCities = len(cities)
    distance = [[0]*numberOfCities for _ in range(numberOfCities)]
    for i in range(numberOfCities):
        for j in range(i+1, numberOfCities):
            distanceNum = calculate_distance(cities[i],cities[j])
            distance[i][j] = distanceNum
            distance[j][i] = distanceNum
    return distance



#Opening the csv data file and storing the values in the city object using the pandas library
city_data = pd.read_csv('city_data_50.csv')
cities = []

for _, row in city_data.iterrows():
    city = City(row['name'],row['description'],row['latitude'],row['longitude'])
    cities.append(city)

#Depth search for shortest path iterative method
def depth(start_city, distance_matrix):
    stack = [(start_city, [start_city], 0)]
    s_path = None
    min_distance = float('inf')

    while stack:
        current_city, path, distance = stack.pop()

        if len(path) == len(distance_matrix):
            if distance < min_distance:
                min_distance = distance
                s_path = path
            continue

        for next_city in range(len(distance_matrix)):
            if next_city not in path:
                current_distance = distance_matrix[current_city][next_city]

                next_path = path + [next_city]
                next_distance = distance + current_distance

                stack.append((next_city, next_path, next_distance))

    return s_path, next_distance


start = 0
distance = distance_matrix_dfs(cities)
sPath, min = depth(start, distance)
print("Depth-first Search")
print("Shortest Path: ")
for i in range(len(cities)-1):
    print(cities[sPath[i]].name,"->",end=" ")
print(cities[sPath[-1]].name)
print("Shortest Distance:",min)




def distance_matrix(location_one, location_two):
    # getting lat and long
    lat_one, long_one = location_one[:2]
    lat_two, long_two = location_two[:2]
    # distance calculation
    distance = math.sqrt((lat_two - lat_one) ** 2 + (long_two - long_one) ** 2)
    return distance


def create_matrix():
    list_size = len(location_list)
    # matrix creation
    matrix = [[0] * list_size for i in range(list_size)]

    # print test statements
    # print("Check for proper matrix size: ")
    # for i in matrix:
    #     print(i)

    for i in range(list_size):
        for j in range(list_size):
            # needs diagonal 0 for location distance to itself
            if i != j:
                # location_list that we turned into list from the csv file, check csv manipulation
                matrix[i][j] = distance_matrix(location_list[i], location_list[j])

    # print test statements
    # print("Check for correct distance in matrix: ")
    # for i in matrix:
    #     print(i)
    return matrix


def bfs_algorithm(matrix, name_list):
    matrix_size = len(matrix)
    # index where the search starts
    start = 0
    # creates an list for visited nodes(NOT A MATRIX)
    visited = [False] * matrix_size
    # visits the 0 element of the visited list and starts the search
    visited[start] = True
    # returns the index and location name from csv
    visited_path = [(start, name_list[start])]
    # variable to add distance into
    starting_distance = 0

    def solve(curr_location, curr_path, curr_distance, shortest_distance, shortest_path):
        # base case
        if len(curr_path) == matrix_size:
            # total = 0 + the distance that is in the matrix(-1 goes to end of list, first element, its an array)
            # start = traversal(up down left right)
            total_distance = curr_distance + matrix[curr_path[-1][0]][start]
            # compare total to shortest and pick shortest as curr
            if total_distance < shortest_distance:
                shortest_distance = total_distance
                shortest_path = curr_path
            return shortest_distance, shortest_path

        for next_location in range(matrix_size):
            # check if visited or not, true after u do
            if not visited[next_location]:
                visited[next_location] = True
                # call function solve
                shortest_distance, shortest_path = solve(
                    next_location,
                    # add the name of next location into current path
                    curr_path + [(next_location, name_list[next_location])],
                    # add distance in between them together
                    curr_distance + matrix[curr_location][next_location],
                    shortest_distance,
                    shortest_path
                )
                # flase for other paths
                visited[next_location] = False
        return shortest_distance, shortest_path

    # make sure that distance is initilized as high as possible cuz everything else needs smaller
    distance = float('inf')
    path = None
    shortest_distance, shortest_path = solve(start, visited_path, starting_distance, distance, path)
    location_names = [location_name for i, location_name in shortest_path]

    return shortest_distance, location_names


# MAIN FUNCTION
# puts csv data into a dataframe
df = pd.read_csv("city_data_50.csv")

# extract the values into list
location = df[['latitude', 'longitude']]
location_list = location.values.tolist()

name = df[['name']]
name_list = name.values.tolist()

# print csv test statements
# print("Check the list has correct values from csv: ")
# print(location_list)

# print("Check the list has correct names from csv: ")
# print(name_list)


# print answer
matrix = create_matrix()
shortest_distance, shortest_path = bfs_algorithm(matrix, name_list)
print("\nBreadth-first search")
print("Shortest Distance: ")
print(shortest_distance)
print("Shortest Path:")
print(shortest_path)
