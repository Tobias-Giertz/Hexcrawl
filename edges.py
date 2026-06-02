from enum import Enum


class SegmentType(Enum):
    ROAD = "road"
    RIVER = "river"
    STREAM = "stream"
    TRAIL = "trail"

class Segment:
    def __init__(self, hex_a, hex_b, segment_type: SegmentType):
        self.hexes = frozenset([hex_a, hex_b])
        self.segment_type = segment_type

    def to_dict(self):
        h1, h2 = tuple(self.hexes)
        return {
            "a": [h1.q, h1.r],
            "b": [h2.q, h2.r],
            "type": self.segment_type.value,
        }

    @classmethod
    def from_dict(cls, data, map_obj):
        hex_a = map_obj.get_hex(*data["a"])
        hex_b = map_obj.get_hex(*data["b"])
        segment_type = SegmentType(data["type"])
        return cls(hex_a, hex_b, segment_type)

    def connects(self, h1, h2):
        return frozenset([h1, h2]) == self.hexes
    
class SegmentNetwork:
    def __init__(self):
        self.segments = {}

    def _key(self, hex_a, hex_b, segment_type):
        return (frozenset([hex_a, hex_b]), segment_type)

    def add_segment(self, hex_a, hex_b, segment_type):
        key = self._key(hex_a, hex_b, segment_type)
        self.segments[key] = Segment(hex_a, hex_b, segment_type)

    def get_segment(self, hex_a, hex_b, segment_type):
        key = self._key(hex_a, hex_b, segment_type)
        return self.segments.get(key)

    def get_segments_between(self, hex_a, hex_b):
        hex_key = frozenset([hex_a, hex_b])
        return [
            segment
            for (segment_hexes, _), segment in self.segments.items()
            if segment_hexes == hex_key
        ]

    def to_dict(self):
        return {
            "segments": [
                segment.to_dict()
                for segment in self.segments.values()
            ]
        }

    @classmethod
    def from_dict(cls, data, map_obj):
        network = cls()

        for segment_data in data["segments"]:
            segment = Segment.from_dict(segment_data, map_obj)
            h1, h2 = tuple(segment.hexes)
            key = network._key(h1, h2, segment.segment_type)
            network.segments[key] = segment

        return network