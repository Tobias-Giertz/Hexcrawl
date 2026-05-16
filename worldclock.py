from dataclasses import dataclass
from enum import Enum


class Season(Enum):
    SPRING = "spring"
    SUMMER = "summer"
    AUTUMN = "autumn"
    WINTER = "winter"

SEASON_DATA = {
    Season.SPRING: {
        "days": 30,
        "dawn_hour": 5,
        "dusk_hour": 21,
    }
}

@dataclass
class WorldClock:
    tick: int = 0

    HOURS_PER_DAY = 24
    DAYS_PER_SEASON = 30
    SEASONS_PER_YEAR = 4
    DAYS_PER_YEAR = DAYS_PER_SEASON * SEASONS_PER_YEAR

    DAWN_HOUR = 6
    NOON_HOUR = 12
    DUSK_HOUR = 18
    MIDNIGHT_HOUR = 0

    @property
    def hour(self) -> int:
        return self.tick % self.HOURS_PER_DAY

    @property
    def day_index(self) -> int:
        return self.tick // self.HOURS_PER_DAY

    @property
    def year(self) -> int:
        return self.day_index // self.DAYS_PER_YEAR + 1

    @property
    def day_of_year(self) -> int:
        return self.day_index % self.DAYS_PER_YEAR + 1

    @property
    def season(self) -> Season:
        season_index = (self.day_index % self.DAYS_PER_YEAR) // self.DAYS_PER_SEASON
        return list(Season)[season_index]

    @property
    def day_of_season(self) -> int:
        return (self.day_index % self.DAYS_PER_SEASON) + 1

    def advance(self, hours: int = 1):
        if hours < 0:
            raise ValueError("Cannot advance time backwards.")
        self.tick += hours

    def hours_until_hour(self, target_hour: int) -> int:
        target_hour %= self.HOURS_PER_DAY
        delta = (target_hour - self.hour) % self.HOURS_PER_DAY
        return delta if delta != 0 else self.HOURS_PER_DAY

    def hours_until_next_dawn(self) -> int:
        return self.hours_until_hour(self.DAWN_HOUR)

    def hours_until_next_dusk(self) -> int:
        return self.hours_until_hour(self.DUSK_HOUR)

    def is_daylight(self) -> bool:
        return self.DAWN_HOUR <= self.hour < self.DUSK_HOUR

    def to_dict(self):
        return {
            "tick": self.tick,
        }

    @classmethod
    def from_dict(cls, data):
        if isinstance(data, int):
            return cls(tick=data)
        return cls(tick=data.get("tick", 0))