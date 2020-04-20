from room import Room
from player import Player
from world import World

import random
import os
import time

from ast import literal_eval


class Queue:
    def __init__(self):
        self.storage = []

    def enqueue(self, item):
        self.storage.append(item)

    def dequeue(self):
        return self.storage.pop(0)

    def size(self):
        return len(self.storage)


class Stack:
    def __init__(self):
        self.storage = []

    def push(self, item):
        self.storage.append(item)

    def pop(self):
        return self.storage.pop()

    def size(self):
        return len(self.storage)


def get_neighbors(room):
    if room is not None:
        neighbors = []
        if(room.n_to):
            neighbors.append(('n', room.n_to))
        if room.e_to:
            neighbors.append(('e', room.e_to))
        if room.s_to:
            neighbors.append(('s', room.s_to))
        if room.w_to:
            neighbors.append(('w', room.w_to))
        return neighbors
    else:
        print(f'Room is NoneType')
        return


def dft(starting_room):
    pass


def bfs(current_room, target_room):
    visited = []
    queue = Queue()
    queue.enqueue(([], current_room))
    visited.append(current_room)

    while queue.size() > 0:
        current_room = queue.dequeue()
        if current_room[1] == target_room:
            return current_room[0]
        if current_room not in visited:
            visited.append(current_room)
            neighbors = get_neighbors(current_room[1])
            for n in neighbors:
                if n[1] not in visited:
                    visited.append(n[1])
                    new_path = current_room[0][:]
                    new_path.append(n[0])
                    queue.enqueue((new_path, n[1]))


def traverse_maze():
    # Rooms that have been visited, by id for space efficiently
    visited = []
    # Rooms that need to be explored.
    target_rooms = Stack()
    # The adventure_bot's path through the dungeon
    adventure_path = []
    # The rooms to be visited
    target_rooms.push((None, player.current_room))
    current_room = player.current_room
    # visited.append(current_room)
    # print(f'Current room from player: {player.current_room}')
    while target_rooms.size() > 0:
        target_room = target_rooms.pop()
        #print(f'target room from stack: {target_room[1].id}')
        # update current room
        if current_room != target_room[1]:
            path_back = bfs(current_room, target_room[1])
            current_room = target_room[1]
            adventure_path += path_back[:]
            # print(f'PATH BACK {path_back}')
        # if target_room[0] != None:
        #     adventure_path.append(target_room[0])
        #     print(f'Adventure path: {adventure_path}')
        if target_room[1] not in visited:
            visited.append(target_room[1])
            # print(f'Target room before get neighbors: {target_room[1]}')
            neighbors = get_neighbors(target_room[1])
            for n in neighbors:
                if n[1] not in visited:
                    target_rooms.push(n)
    # print(f"Adventure path: {adventure_path}")
    return adventure_path


# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
# world.print_rooms(player.current_room)

player = Player(world.starting_room)

# Fill this out with directions to walk
traversal_path = traverse_maze()

# Check starting room choices
# print(f"Starting room choices:")
# neighbors = get_neighbors(player.current_room)
# for i in neighbors:
#     print(i)

# TRAVERSAL TEST - DO NOT MODIFY


visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)
    world.print_rooms(player.current_room)
    time.sleep(0.5)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     (cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break     n
#     else:
#         print("I did not understand that command.")
