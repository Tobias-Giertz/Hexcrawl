from dataclasses import dataclass
from enum import Enum

class Months(Enum):
    JANUARY = "january"
    FEBRUARY = "february"
    MARCH = "march"
    APRIL = "april"
    MAY = "may"
    JUNE = "june"
    JULY = "july"
    AUGUST = "august"
    SEPTEMBER = "september"
    OCTOBER = "october"
    NOVEMBER = "november"
    DECEMBER = "december"

SPRING = [Months.MARCH, Months.APRIL, Months.MAY]
SUMMER = [Months.JUNE, Months.JULY, Months.AUGUST]
AUTUMN = [Months.SEPTEMBER, Months.OCTOBER, Months.NOVEMBER]
WINTER = [Months.DECEMBER, Months.JANUARY, Months.FEBRUARY]

YEAR = SPRING + SUMMER + AUTUMN + WINTER

MONTH_DATA = {
    Months.JANUARY: {
        "days": 30,
        "dawn_hour": 9,
        "dusk_hour": 15,
    },
    Months.FEBRUARY: {
        "days": 28,
        "dawn_hour": 8,
        "dusk_hour": 16,
    },
    Months.MARCH: {
        "days": 31,
        "dawn_hour": 6,
        "dusk_hour": 18,
    },
    Months.APRIL: {
        "days": 30,
        "dawn_hour": 5,
        "dusk_hour": 19,
    },
    Months.MAY: {
        "days": 31,
        "dawn_hour": 4,
        "dusk_hour": 20,
    },
    Months.JUNE: {
        "days": 30,
        "dawn_hour": 3,
        "dusk_hour": 21,
    },
    Months.JULY: {
        "days": 31,
        "dawn_hour": 3,
        "dusk_hour": 21,
    },
    Months.AUGUST: {
        "days": 31,
        "dawn_hour": 4,
        "dusk_hour": 20,
    },
    Months.SEPTEMBER: {
        "days": 30,
        "dawn_hour": 6,
        "dusk_hour": 18,
    },
    Months.OCTOBER: {
        "days": 31,
        "dawn_hour": 7,
        "dusk_hour": 17,
    },
    Months.NOVEMBER: {
        "days": 30,
        "dawn_hour": 8,
        "dusk_hour": 16,
    },
    Months.DECEMBER: {
        "days": 31,
        "dawn_hour": 9,
        "dusk_hour": 15,
    },
}

@dataclass
class WorldClock:
    tick: int = 0
    HOURS_PER_DAY = 24
    DAYS_PER_YEAR = sum(MONTH_DATA[month]["days"] for month in YEAR)

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
    def month(self) -> Months:
        day_of_year = self.day_of_year
        for month in YEAR:
            if day_of_year <= MONTH_DATA[month]["days"]:
                return month
            day_of_year -= MONTH_DATA[month]["days"]
        raise ValueError("Invalid day of year")

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