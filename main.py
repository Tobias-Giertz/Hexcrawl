import time

from world import World
from actor import Actor
from roads import *
from actions import ACTIONS


### New or load game ###

new_or_load = input("Load or start new? (load/new/quit) ").strip().lower()

if new_or_load == "new":
    world_name = input("Enter world name: ")
    world = World()

    # Center hex
    world.map.add_hex(0, 0)

    center_hex = world.map.get_hex(0, 0)

    # Generate surrounding hexes
    for i in range(3):
        world.draw_map("world.png")
        world.expand_map_from_edges()
        time.sleep(1)

    # Player
    player_id = "player"
    player = Actor(player_id, "Player", center_hex)
    world.add_actor(player_id, player)
    world.player = player

    # Debug road, remove later
    world.map.road_network.add_road(world.map.get_hex(0, 0), world.map.get_hex(1, 0))

elif new_or_load == "load":
    world_name = input("Load world name: ")
    world = World.load(f"{world_name}.json")

elif new_or_load == "quit":
    exit()

else:
    print("Unknown option.")
    exit()



### GAME LOOP ###

while True:
    world.expand_map_from_actors()

    print(f"Time: {world.clock}")

    for action in world.active_actions:
        print(f" - {action.print_description()}")

    world.draw_map("world.png")

    command = input("> ").strip().lower()

    if command == "quit":
        break

    elif command == "expand map":
        # expand from all edge hexes
        world.expand_map_from_edges()
        continue

    elif command == "advance":
        world.advance_time(1)
        continue

    action = ACTIONS.get(command)

    if action:
        action(world)
    else:
        print("Unknown command.")



### Save game option ###

save_or_not = input("Save game? (y/n) ").strip().lower()

if save_or_not == "y":
    world.save(f"{world_name}.json")
    print(f"Game saved: {world_name}.json")
