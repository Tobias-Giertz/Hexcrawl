from terrain import Terrain
from coordinates import axial_to_offset, axial_to_cube, axial_to_pixel


class Hex:
    """
    Representerar en enskild hex i kartan.

    Koordinatsystem:
    - Lagrar position internt i axial-koordinater (q, r)
    - Kan konverteras till:
        - offset (för grid/indexering)
        - cube (för beräkningar som avstånd)
        - pixel (för rendering)
    """

    def __init__(self, q: int, r: int, terrain: Terrain) -> None:
        """
        Skapar en ny hex.

        Args:
            q (int): Axial q-koordinat
            r (int): Axial r-koordinat
            terrain (Terrain): Terrängtyp (enum)

        Raises:
            ValueError: Om terrain inte är av typen Terrain
        """
        if not isinstance(terrain, Terrain):
            raise ValueError("terrain must be a Terrain")

        self.q: int = q
        self.r: int = r
        self.terrain: Terrain = terrain

    def to_dict(self) -> dict:
        """
        Serialiserar hexen till en dictionary.

        Returns:
            dict: Representation av hexen
        """
        return {
            "q": self.q,
            "r": self.r,
            "terrain": self.terrain.value,  # enum -> serialiserbart värde
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Hex":
        """
        Skapar en Hex från en dictionary.

        Args:
            data (dict): Dictionary med nycklar "q", "r", "terrain"

        Returns:
            Hex: Ny instans av Hex
        """
        return cls(
            data["q"],
            data["r"],
            Terrain(data["terrain"])  # värde -> enum
        )

    @property
    def offset(self) -> tuple[int, int]:
        """
        Returnerar offset-koordinater (odd-r).

        Bra för:
        - Array-indexering
        - Grid-baserad logik

        Returns:
            tuple[int, int]: (col, row)
        """
        return axial_to_offset(self.q, self.r)

    @property
    def cube(self) -> tuple[int, int, int]:
        """
        Returnerar cube-koordinater.

        Bra för:
        - Avståndsberäkningar
        - Vektoroperationer

        Returns:
            tuple[int, int, int]: (x, y, z)
        """
        return axial_to_cube(self.q, self.r)
    
    @property
    def pixel(self) -> tuple[float, float]:
        """
        Returnerar kartesiska (pixel) koordinater.

        Bra för:
        - Rendering (t.ex. matplotlib, canvas, web)

        Notera:
        - Dessa är kontinuerliga värden (float), inte grid-index

        Returns:
            tuple[float, float]: (x, y)
        """
        return axial_to_pixel(self.q, self.r)