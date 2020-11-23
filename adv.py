from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


#
# START HERE
#

backwards = {
    'n': 's',
    's': 'n',
    'w': 'e',
    'e': 'w'
}

visited = {}

# store reverse path
reverse = []

# add first room, get exits
visited[player.current_room.id] = player.current_room.get_exits()
# check
# print(visited[player.current_room.id][-1])

# add until we reach 499 rooms
while len(visited) < 500:
    # check if room exists
    if player.current_room.id not in visited:
        # if not add to dict
        visited[player.current_room.id] = player.current_room.get_exits()
        # last move is previous move we made
        prev_move = reverse[-1]
        #if prev_move in list remove it
        if prev_move in visited[player.current_room.id]:
            visited[player.current_room.id].remove(prev_move)

    # if we still have some possible exits to visit     
    if len(visited[player.current_room.id]) > 0:
        # Grab the last exit possible, set to move
        move = visited[player.current_room.id][-1]
        # Pop the possible direction from values of current room
        visited[player.current_room.id].pop()
        # add to our path
        traversal_path.append(move)
        # add backwarads to reverse
        reverse.append(backwards[move])
        # move the previous move
        player.travel(move)

    # if we've tried everything else
    else:
        prev_move = reverse[-1]
        #Remove from reverse list
        reverse.pop()
        #Add prev_move to our traversal path because we have to travel back
        traversal_path.append(prev_move)
        #move with previous move
        player.travel(prev_move)

## TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######

#player.current_room.print_room_description(player)
#while True:
#    cmds = input("-> ").lower().split(" ")
#    if cmds[0] in ["n", "s", "e", "w"]:
#        player.travel(cmds[0], True)
#    elif cmds[0] == "q":
#        break
#    else:
#        print("I did not understand that command.")