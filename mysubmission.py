import sys
import math
import io
import itertools
import random
#########################################
# Vorto Algorithmic Challenge - Zachary Ward
#########################################
## (from evaluateShared.py) ##
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def distanceBetweenPoints(p1, p2):
    xDiff = p1.x - p2.x
    yDiff = p1.y - p2.y
    return math.sqrt(xDiff*xDiff + yDiff*yDiff)

class Load:
    def __init__(self, id, pickup, dropoff):
        self.id = id
        self.pickup = pickup
        self.dropoff = dropoff
#########################################

# parses and returns load information from a given file path
def parse_load_info(file_path):
    loads = []
    with open(file_path, 'r') as file:
        next(file)  # Skip header
        for line in file:
            # split into [loadNumber, pickup, dropoff]
            parts = line.split()

            # Example: "(-81.31, 146.186)" -> ["-81.31", " 146.186"] -> (-81.31, 146.186)
            load_id = int(parts[0])
            pickup = Point(*tuple(map(float, parts[1].strip('()').split(','))))
            dropoff = Point(*tuple(map(float, parts[2].strip('()').split(','))))
            loads.append(Load(load_id, pickup, dropoff))
    return loads

# calculates the total distance traveled for a given route that starts and ends at a depot
def calculate_route_cost(route):
    depot = Point(0, 0)
    total_distance = distanceBetweenPoints(depot, route[0].pickup)
    current_point = route[0].pickup
    for load in route:
        total_distance += distanceBetweenPoints(current_point, load.pickup)
        current_point = load.pickup
        total_distance += distanceBetweenPoints(current_point, load.dropoff)
        current_point = load.dropoff
    total_distance += distanceBetweenPoints(current_point, depot)
    return total_distance

# calculates the load closest to our current dropoff out of the remaining loads
def nearest_load(current_dropoff, remaining_loads):
    nearest = None
    min_distance = float('inf')
    for load in remaining_loads:
        dist = distanceBetweenPoints(current_dropoff, load.pickup)
        if dist < min_distance:
            min_distance = dist
            nearest = load
    return nearest

# Algorithm: 
# 1. Sort the loads from closest to furthest from depot
# 2. Each iteration of the loop starts by taking the first load from 
# our sorted remaining_loads
# 3. We find the nearest load from our current dropoff and build out the route based on this
# until we start to get close to the max_time (720 min), in which case we append our route and
# start a new one. As we construct our current route, we remove the loads added from remaining_loads.
def get_routes(loads, max_time_per_route):
    loads.sort(key=lambda load: distanceBetweenPoints(load.pickup, Point(0,0)))
    remaining_loads = loads.copy()
    routes = []

    while remaining_loads:
        current_route = [remaining_loads.pop(0)]
        current_time = calculate_route_cost(current_route)

        while True:
            if not remaining_loads:
                break
            current_dropoff = current_route[-1].dropoff
            next_load = nearest_load(current_dropoff, remaining_loads)
            if next_load:
                test_route = current_route + [next_load]
                test_time = calculate_route_cost(test_route)
                if test_time <= max_time_per_route:
                    current_route.append(next_load)
                    remaining_loads.remove(next_load)
                else:
                    break

        routes.append(current_route)

    return routes

def main(file_path):
    loads = parse_load_info(file_path)
    max_time_per_driver = 720  # 12 hours in minutes
    truck_routes = get_routes(loads, max_time_per_driver)

    # was seeing some weird carriage return behavior on my machine --
    # added code here to ensure my output is encoded to utf-8 and this
    # seemed to fix the issue
    for route in truck_routes:
        route_str = ','.join(str(load.id) for load in route)
        output_line = f"[{route_str}]\n".encode('utf-8')
        sys.stdout.buffer.write(output_line)

if __name__ == "__main__":
    main(sys.argv[1])
