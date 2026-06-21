from coordinates import DIRECTIONS, is_adjacent
from terrain import Terrain, TERRAIN_DATA
from edges import SegmentType

ACTIONS = {
    "player moves east": lambda world: move_player(world, "east"),
    "player moves north east": lambda world: move_player(world, "north_east"),
    "player moves north west": lambda world: move_player(world, "north_west"),
    "player moves west": lambda world: move_player(world, "west"),
    "player moves south west": lambda world: move_player(world, "south_west"),
    "player moves south east": lambda world: move_player(world, "south_east")
}

class Action:
    def __init__(self, actor_id, duration):
        self.actor_id = actor_id
        self.remaining_time = duration
    
    def on_complete(self, world):
        raise NotImplementedError

    def to_dict(self):
        return {
            "actor_id": self.actor_id,
            "remaining_time": self.remaining_time,
        }
    
    @classmethod
    def from_dict(cls, data):
        action = cls(data["actor_id"], None)
        action.remaining_time = data["remaining_time"]
        return action


### TEMPLATE ###
# class Actions(Action):
#     def __init__(self, actor_id, parameters):
#         super().__init__(actor_id, duration)
#         self.parameters = parameters
#
#     def to_dict(self):
#         pass
#
#     @classmethod
#     def from_dict(cls, data):
#         pass
#
#     def on_start(self, world):
#         pass  
#
#     def on_complete(self, world):
#         pass  
#
#     def print_description(self):
#         pass  


### WORLD ACTIONS ###
    
### ACTOR ACTIONS ###

class MoveAction(Action):
    def __init__(self, actor_id, target_q, target_r, teleport=False):
        super().__init__(actor_id, duration=2)
        self.target_q = target_q
        self.target_r = target_r
        self.teleport = teleport

    def to_dict(self):
        data = super().to_dict()

        data.update({
            "type": "MoveAction",
            "target_q": self.target_q,
            "target_r": self.target_r,
            "teleport": self.teleport,
        })

        return data

    @classmethod
    def from_dict(cls, data):
        action = cls(
            data["actor_id"],
            data["target_q"],
            data["target_r"],
            teleport=data.get("teleport", False)
        )

        action.remaining_time = data["remaining_time"]

        return action

    def on_start(self, world):
        actor = world.actors[self.actor_id]

        # Road
        if world.map.segment_network.get_segment(actor.current_hex, world.map.get_hex(self.target_q, self.target_r), SegmentType.ROAD):
            self.remaining_time = 1
            print("Road found!")
        else:
            self.remaining_time = TERRAIN_DATA[world.map.get_hex(self.target_q, self.target_r).terrain]["speed"]
        # print(f"Target terrain: {world.map.get_hex(self.target_q, self.target_r).terrain}, speed: {self.remaining_time}")

        if not self.teleport:
            if not is_adjacent(
                actor.current_hex.q,
                actor.current_hex.r,
                self.target_q,
                self.target_r
            ):
                raise ValueError("Target hex is not adjacent!")

    def on_complete(self, world):
        actor = world.actors[self.actor_id]
        actor.current_hex = world.map.get_hex(self.target_q, self.target_r)
        self.print_on_complete(world)


    def print_description(self):
        return f"{self.actor_id} moves to ({self.target_q}, {self.target_r}), time remaining: {self.remaining_time}"   
    
    def print_on_complete(self, world):
        return f"{self.actor_id} has arrived at a {Terrain(world.map.get_hex(self.target_q, self.target_r).terrain).name} hex at ({self.target_q}, {self.target_r})"


def move_player(world, direction):
    player = world.actors["player"]

    dq, dr = DIRECTIONS[direction]

    world.add_action(
        MoveAction(
            player.actor_id,
            player.current_hex.q + dq,
            player.current_hex.r + dr
        )
    )

class RestAction(Action):
    SHORT = "short" # 1 time unit. Low interuption risk
    LONG = "long" # 8 time units. High interuption risk
    LONG_ELVEN = "long_elven" # 4 time units. High interuption risk
    LONG_DAWN = "long_dawn" # At least 8 time units, minimum till dawn. High interuption risk.

    def __init__(self, actor_id, type=None):
        super().__init__(actor_id, duration=8)
        self.type = type

    def to_dict(self):
        data = super().to_dict()

        data.update({
            "type": "RestAction",
            "type": self.type
        })

        return data

    @classmethod
    def from_dict(cls, data):
        action = cls(
            data["actor_id"]
        )

        action.remaining_time = data["remaining_time"]

        return action

    def on_start(self, world):
        pass

    def on_complete(self, world):
        pass

    def print_description(self):
        return f"{self.actor_id} is taking a rest, time remaining: {self.remaining_time}"
