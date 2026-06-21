from world import World
from terrain import Terrain
from edges import SegmentType

### ========================================== ###
###   World generation: Vardvägar, Heymdalen   ###
### ========================================== ###

## Heydalen
world = World()

world.map.add_hex(0, 0)
center_hex = world.map.get_hex(0, 0)

## Rödsjön
sea_hexes = [
    (-3, -2), (-2, -2),
    (-4, -1), (-3, -1), (-2, -1),
    (-5, 0), (-4, 0), (-3, 0), (-2, 0),
    (-5, 1), (-4, 1), (-3, 1), (-2, 1), (-1, 1) , (0, 1), (1, 1), (2, 1), (3, 1),
    (-5, 2), (-4, 2), (-3, 2), (-2, 2), (-1, 2) , (0, 2), (1, 2), (2, 2), (3, 2), (4, 2),
    (-4, 3), (-3, 3), (0, 3), (1, 3), (2, 3), (3, 3), (4, 3),
    (0, 4), (1, 4), (2, 4), (3, 4),
]

for r, q in sea_hexes:
    world.map.add_hex(r, q, Terrain.SEA)


## Stenröses omnejd
land_hexes = [
    (0, -4), (1, -4), (2, -4), (3, -4), (4, -4),
    (-1, -3), (0, -3), (1, -3), (2, -3), (3, -3), (4, -3),
    (-1, -2), (0, -2), (1, -2), (2, -2), (3, -2), (4, -2),
    (-1, -1), (0, -1), (1, -1), (2, -1), (3, -1), (4, -1),
    (-1, 0), (1, 0), (2, 0), (3, 0), (4, 0)
]

for r, q in land_hexes:
    world.map.add_hex(r, q)

## Vägen till Tredagaviken
land_hexes = [
    (5, 3), (6, 3), (9, 3), (10, 3), (11, 3),
    (6, 4), (7, 4), (8, 4)
]

for r, q in land_hexes:
    world.map.add_hex(r, q)


## Landmärken (ej implemenerat)
# Städer: Stenröse (0,0)
# Byar: (-1, -1), (2, -1), (2, 0)
# Torp: (-1, -2), (0, -2), (3, 0), (3, -2)
# Ruiner: (2, -4)


## Vägar
segment = [
    ((-1, 0), (0, 0)),
    ((0, 0), (1, 0)),
    ((1, 0), (2, 0)),
    ((2, 0), (3, 0)),
    ((-1, -1), (-1, 0)),
    ((-1, -2), (-1, -1)),
    ((0, -2), (-1, -1)),
    ((-1, -2), (0, -2)),
    ((0, -2), (1, -2)),
    ((1, -2), (2, -2)),
    ((2, -2), (3, -2)),
    ((3, -2), (2, -1)),
    ((2, -1), (2, 0)),
    ((2, -1), (1, -1)),
    ((0, 0), (1, -1)),
    ((1, -1), (1, -2)),
    ((1, -2), (2, -3)),
    ((2, -3), (2, -4))
]

for start, end in segment:
    world.map.segment_network.add_segment(world.map.get_hex(*start), world.map.get_hex(*end), SegmentType.ROAD)

## Sjöleder
segment = [
    ((0, 0), (0, 1)),
    ((0, 1), (1, 1)),
    ((1, 1), (2, 1)),
    ((2, 1), (3, 1)),
    ((3, 1), (3, 2)),
    ((3, 2), (4, 2)),
    ((4, 2), (4, 3)),
    ((4, 3), (5, 3)),
    ((5, 3), (6, 3)),
    ((6, 3), (6, 4)),
    ((6, 4), (7, 4)),
    ((7, 4), (8, 4)),
    ((8, 4), (9, 3)),
    ((9, 3), (10, 3)),
    ((10, 3), (11, 3))
]

for start, end in segment:
    world.map.segment_network.add_segment(world.map.get_hex(*start), world.map.get_hex(*end), SegmentType.RIVER)

for n in range(1):
    world.expand_map_from_edges()

world.draw_map("Heymdalen.png")

world.save("Heymdalen.json")