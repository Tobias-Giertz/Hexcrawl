class Actor:
    def __init__(self, actor_id, actor_name, current_hex=None):
        self.actor_id = actor_id
        self.name = actor_name
        self.current_hex = current_hex

        self.current_action = None
        self.queued_actions = []

    def to_dict(self):
        return {
            "actor_id": self.actor_id,
            "actor_name": self.name,
            "current_hex": (
                [self.current_hex.q, self.current_hex.r]
                if self.current_hex is not None
                else None
            ),
        }

    @classmethod
    def from_dict(cls, data, map_obj):
        if data["current_hex"] is None:
            current_hex = None
        else:
            q, r = data["current_hex"]
            current_hex = map_obj.get_hex(q, r)

        return cls(data["actor_id"], data["actor_name"], current_hex)