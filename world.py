import json
import csv
import matplotlib.pyplot as plt

from actions import Action
from map import Map
from actor import Actor
from coordinates import axial_to_pixel
from terrain import Terrain, TERRAIN_DATA
from edges import SegmentType

class World:
    def __init__(self):
        self.map = Map()
        self.actors = {}
        self.clock = 0
        self.active_actions = []

    def to_dict(self):
        return {
            "save_version": 1,
            "map": self.map.to_dict(),
            "actors": [actor.to_dict() for actor in self.actors.values()],
            "clock": self.clock,
            "active_actions": [action.to_dict() for action in self.active_actions],
        }

    @classmethod
    def from_dict(cls, data):
        world = cls()
        world.map = Map.from_dict(data["map"])
        world.actors = {
            actor_data["actor_id"]: Actor.from_dict(actor_data, world.map)
            for actor_data in data["actors"]
        }
        world.clock = data["clock"] if data["clock"] else 0
        world.active_actions = [
            Action.from_dict(action_data)
            for action_data in data["active_actions"]
        ]
        return world

    def save(self, filepath):
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(self.to_dict(), file, indent=4, ensure_ascii=False)

    @classmethod
    def load(cls, filepath):
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

        return cls.from_dict(data)

    def advance_time(self, amount=1):
        self.check_random_events()

        for actor in self.actors.values():
            action = actor.current_action

            if action is None:
                self.start_next_action(actor)
                action = actor.current_action

            if action is None:
                continue

            action.remaining_time -= 1

            if action.remaining_time <= 0:
                action.on_complete(self)
                actor.current_action = None
                self.start_next_action(actor)

        self.clock += amount

        for action in self.active_actions[:]:
            if action.remaining_time <= 0:
                self.active_actions.remove(action)

    def add_actor(self, actor_id, actor):
        self.actors[actor_id] = actor

    def add_action(self, action):
        actor = self.actors.get(action.actor_id)

        if actor is None:
            raise ValueError(f"No actor with id {action.actor_id} found!")

        if actor.current_action is None:
            try:
                action.on_start(self)
            except ValueError as error:
                print(f"Action failed to start: {error}")
                return

            actor.current_action = action
            self.active_actions.append(action)
        else:
            actor.queued_actions.append(action)

    def start_next_action(self, actor):
        while actor.current_action is None and actor.queued_actions:
            action = actor.queued_actions.pop(0)

            try:
                action.on_start(self)
            except ValueError as error:
                print(f"Queued action failed to start: {error}")
                continue

            actor.current_action = action

    def expand_map_from_edges(self):
        edge_hexes = [h for h in self.map.hexes.values() if self.map.is_edge_hex(h)]

        for hex in edge_hexes:
            for q, r in self.map.get_neighbor_coords(hex):
                if self.map.get_hex(q, r) is None:
                    self.map.add_hex(q, r)

    def expand_map_from_actors(self):
        for actor in self.actors.values():
            if actor.current_hex is None:
                continue

            for q, r in self.map.get_neighbor_coords(actor.current_hex):
                if self.map.get_hex(q, r) is None:
                    self.map.add_hex(q, r)

    def check_random_events(self): # placeholder
        print("Checking for random encounters...")
        for actors in self.actors.values():
            if actors.current_hex is None:
                continue
            # actor.roll_random_event(self)
        pass
    

####==============================####

    def list_world_objects(self):
        if not self.map.hexes:
            print("(empty map)")
            return

        for hex in self.map.hexes:
            q, r = hex
            data = self.map.get_hex(q, r)
            print(f'Hex at: {data.q}, {data.r} - {data.terrain}')

        if not self.actors:
            print("(no actors)")
            return

        for actor in self.actors.values():
            name = actor.name
            q, r = actor.current_hex.q, actor.current_hex.r
            print(f'Actor: {name}, at ({q}, {r})')
        return
        
    def draw_map(self, filename="plot.png"):
        terrain_colors = {t: data["map_color"] for t, data in TERRAIN_DATA.items()}

        xs = []
        ys = []
        colors = []

        plt.figure(figsize=(8, 8))

        for q, r in self.map.hexes:
            tile = self.map.get_hex(q, r)
            x, y = axial_to_pixel(q, r)

            xs.append(x)
            ys.append(y)
            colors.append(terrain_colors.get(tile.terrain, "black"))

        plt.scatter(
            xs,
            ys,
            s=1000,
            c=colors,
            marker="h"
        )

        for q, r in self.map.hexes:
            x, y = axial_to_pixel(q, r)

            plt.text(
                x,
                y,
                f"{q},{r}",
                ha="center",
                va="center",
                fontsize=7,
                color="black"
            )

        segment_colors = {
            SegmentType.ROAD: "black",
            SegmentType.RIVER: "lightblue",
        }

        for segment in self.map.segment_network.segments:
            hexes, s_type = tuple(segment)
            a, b = tuple(hexes)

            a_x, a_y = axial_to_pixel(a.q, a.r)
            b_x, b_y = axial_to_pixel(b.q, b.r)

            plt.plot([a_x, b_x], [a_y, b_y], color=segment_colors.get(s_type))

        actor_xs = []
        actor_ys = []

        for actor in self.actors.values():
            if actor.current_hex is None:
                continue

            x, y = axial_to_pixel(actor.current_hex.q, actor.current_hex.r)
            actor_xs.append(x)
            actor_ys.append(y)

        plt.scatter(
            actor_xs,
            actor_ys,
            s=50,
            c="red",
            marker="o"
        )

        plt.axis("equal")
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(filename, dpi=150)
        plt.close()
