import pandas as pd
import heapq
import random

campus_paths = {
    "Main Ground": {"Student Mosque": 210, "Sports Complex": 120, "Admin Block": 3},
    "Student Mosque": {"FBS Building": 50, "Main Ground": 210},
    "Admin Block": {"FCSE Building": 500, "Main Ground": 3},
    "FCSE Building": {"Admin Block": 550, "FBS Building": 77, "AHA Auditorium": 100},
    "FBS Building": {"FCSE Building": 400, "New Academic Block": 190, "Central Mess": 62, "AHA Auditorium": 500},
    "Central Mess": {"FBS Building": 62, "Senior Hostels": 400},
    "New Academic Block": {"Central Library": 300, "FBS Building": 77},
    "Central Library": {"New Academic Block": 300, "Faculty Club": 600, "Brabers building": 130, "AHA Auditorium": 350},
    "Faculty Club": {"Hostel 11 and 12": 1400, "Central Library": 950},
    "Brabers building": {"Central Library": 130, "New Girls Hostel": 160},
    "New Girls Hostel": {"Brabers building": 160, "Medical Centre": 290},
    "Medical Centre": {"New Girls Hostel": 290, "FMCE": 350, "Tuck": 9},
    "FMCE": {"Medical Centre": 350, "AHA Auditorium": 200},
    "FME": {"AHA Auditorium": 200, "GIKI Guest House": 350},
    "GIKI Guest House": {"FME": 350, "GIKI School And College": 500},
    "Tuck": {"Medical Centre": 9, "Tuck Mosque": 260, "GIKI School And College": 130},
    "AHA Auditorium": {"FCSE Building": 100, "FBS Building": 500, "Central Library": 350, "FMCE": 200, "FME": 200},
    "GIKI School And College": {},
    "Senior Hostels": {},
    "Tuck Mosque": {},
    "Sports Complex": {}
} # dictionary containing distances of nodes to its neighbouring buildings
data = []
for start in campus_paths: # for each starting node in campus
    for end in campus_paths[start]: # for each neighbouring building connected to nodes 
        data.append({"From": start, "To": end, "Distance (m)": campus_paths[start][end]})
campus_df = pd.DataFrame(data) # dataframe
print(campus_df) # prints Campus DataFrame
def shortest_path(graph, start, end): # shortest distance function
    pq = [(0, start)] # defines the priority queue
    distances = {}  # create an empty dictionary( no distances at start)
    for node in graph:  # go through each building in the campus
        distances[node] = float('inf')   # set the initial distance to infinity( we don't know the distances yet)
    distances[start] = 0 #distances of start building is 0 
    previous = {} #visited buildings
    while pq: # until there are buildings in pq
        current_distance, current_node = heapq.heappop(pq) # tuple unpacking,pop the samllest distance from pq 
        if current_node == end: # if the current building is the final destination
            break # stop the loop ,path found
        neighbors = graph.get(current_node, {}) # get all neighboring buildings of current building ( returns value of key)
        for neighbor in neighbors: # for each key in neighbours
            weight = neighbors[neighbor] # distance from current building to this neighbouring building
            distance = current_distance + weight # total distance from starting building to neighboring building via current building 
            if distance < distances.get(neighbor, float('inf')): # if new path is shorter than previous one 
                distances[neighbor] = distance # update shortest distance to tjis neighbour         
                previous[neighbor] = current_node 
                heapq.heappush(pq, (distance, neighbor)) # adds the neoghbour building with updated distance to priority queue

    path = [] # empty list to store shorttest path
    node = end  # start backtarcking from final building 
    while node in previous: # until we reach our starting building
        path.append(node) # add current building to path
        node = previous[node] # move to building from where we came
    path.append(start) # finally add starting building
    return path[::-1], distances[end] # reverse path
def shortest_path_distance(graph, start, end): # path distance function
    return shortest_path(graph, start, end)[1]
start_building = input("Enter a starting building: ")
end_building = input("Enter an ending building: ")
route, total_distance = shortest_path(campus_paths, start_building, end_building) # call the shorter path function
print(f"Shortest route from {start_building} to {end_building}:")
print(" → ".join(route)) #prints steps of route
print(f"Total distance: {total_distance} meters")

def campus_mystery_game(campus_map): # campus mystery game function (displays story of game)

    print("\n CAMPUS MYSTERY GAME")
    print("A USB containing exam papers is missing.")
    print("Try to find it before security arrives.\n")

    areas = {
        "Academic Area": {"FCSE Building", "FBS Building", "Central Library", "New Academic Block", "AHA Auditorium", "FME", "FMCE"},
        "Hostels Area": {"New Girls Hostel", "Senior Hostels", "Hostel 11 and 12"},
        "Sports Area": {"Sports Complex", "Main Ground"},
        "Quiet Area": {"Faculty Club", "GIKI Guest House", "Tuck Mosque"}
    }

    buildings = list(campus_map.keys())
    current_location = random.choice(buildings)#randomly select starting location and usb location
    usb_location = random.choice(buildings)
    moves_left = 12
    score = 0
    visited = set()
    for area, places in areas.items():#give the player an initial clue about usb location
        if usb_location in places: # if usb present those places 
            print("Clue: The USB is somewhere in the", area)
            break # stop the loop
    while moves_left > 0: # until we have tries left 
        print(f"\n Current location: {current_location}")
        print(f" Moves left: {moves_left} |  Score: {score}")
        if current_location == usb_location:
            print("\n🎉 You found the USB!")
            score += 50 #add score
            print("Final score:", score)
            return
        #calculate distance from usb
        current_distance = shortest_path_distance(campus_map, current_location, usb_location) # call function
        if current_distance <= 100:#provide hints based on how far the player is
            print("Hint: You are very close!")
        elif current_distance <= 300:
            print("Hint: You are near.")
        elif current_distance <= 700:
            print("Hint: You are still far.")
        else:
            print("Hint: You are very far away.")
        #get nerighbouring buildings that player can move to
        neighbors = list(campus_map[current_location].keys())
        #add a few random places to make the game less predictble
        extra_places = random.sample([b for b in campus_map if b != current_location and b not in neighbors],
                                     min(2, len(campus_map)))
        options = neighbors + extra_places#combine all movement problems
        random.shuffle(options)
        print("\nYou can go to:")
        for i, place in enumerate(options, 1):
            print(f"{i} - {place}")
        choice = input("Choose a place number: ")
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            next_location = options[int(choice)-1]
            #compare distances to see if the palyer moved closer
            new_distance = shortest_path_distance(campus_map, next_location, usb_location)
            if new_distance < current_distance:
                score += 10 # adds score
                print("Good move! You are getting closer.")
            else:
                score -= 5
                print("Oops! You are moving away from the USB.")

            current_location = next_location#update location
            visited.add(current_location)
        else:
            print("Invalid choice! You wasted a move.")
            score -= 5
        moves_left -= 1#decrease remaining moves after each turn
    print("\n Game Over!") #if the loop ends, the players runs out of moves       
    print("The USB was hidden in:", usb_location)
    print("Final score:", score)
campus_mystery_game(campus_paths) # run the game