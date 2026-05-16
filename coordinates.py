import math
from typing import Tuple, Dict

# Riktningar i axial-koordinater.
# Dessa används för att hitta grannar i hex-griden.
DIRECTIONS: Dict[str, Tuple[int, int]] = {
    "east":         (1, 0),
    "north_east":   (1, -1),
    "north_west":   (0, -1),
    "west":         (-1, 0),
    "south_west":   (-1, 1),
    "south_east":   (0, 1),
}

def offset_to_axial(col: int, row: int) -> Tuple[int, int]:
    """
    Konverterar från offset-koordinater (odd-r layout) till axial-koordinater.

    Offset-systemet används ofta för grid-lagring (rad/kolumn),
    medan axial är mer matematiskt praktiskt för hex-beräkningar.

    Parametrar:
        col (int): kolumnindex i offset-systemet
        row (int): radindex i offset-systemet

    Returnerar:
        (q, r) (Tuple[int, int]): motsvarande axial-koordinater
    """
    # Justerar kolumnen beroende på om raden är udda eller jämn
    q = col - (row - (row & 1)) // 2
    r = row
    return q, r


def axial_to_offset(q: int, r: int) -> Tuple[int, int]:
    """
    Konverterar från axial-koordinater till offset-koordinater (odd-r layout).

    Parametrar:
        q (int): axial x-koordinat
        r (int): axial y-koordinat

    Returnerar:
        (col, row) (Tuple[int, int]): motsvarande offset-koordinater
    """
    # Inverterar transformationen från offset_to_axial
    col = q + (r - (r & 1)) // 2
    row = r
    return col, row


def axial_to_cube(q: int, r: int) -> Tuple[int, int, int]:
    """
    Konverterar axial-koordinater till cube-koordinater.

    Cube-systemet använder tre axlar (x, y, z) där:
        x + y + z = 0

    Detta system är mycket användbart för avståndsberäkningar
    och vissa algoritmer (t.ex. pathfinding).

    Parametrar:
        q (int): axial x-koordinat
        r (int): axial y-koordinat

    Returnerar:
        (x, y, z) (Tuple[int, int, int]): cube-koordinater
    """
    x = q
    z = r
    y = -x - z  # säkerställer att x + y + z = 0
    return x, y, z


def axial_to_pixel(q: int, r: int) -> Tuple[float, float]:
    """
    Konverterar axial-koordinater till kartesiska (pixel-)koordinater.

    Används vid rendering, t.ex. med matplotlib eller i webbläsare.

    Antaganden:
        - Hexagonerna är "pointy-top"
        - Storleken är normaliserad (radie = 1)

    Parametrar:
        q (int): axial x-koordinat
        r (int): axial y-koordinat

    Returnerar:
        (x, y) (Tuple[float, float]): position i 2D-plan
    """
    # Horisontell position (√3 ≈ bredden av hex)
    x = math.sqrt(3) * (q + r / 2)

    # Vertikal position (1.5 = avstånd mellan rader)
    y = -3 / 2 * r

    return x, y


def cube_distance(
    a_x: int, a_y: int, a_z: int,
    b_x: int, b_y: int, b_z: int
) -> int:
    """
    Beräknar hex-avståndet mellan två punkter i cube-koordinater.

    Avståndet definieras som minsta antal steg mellan två hexar
    i ett hexagonalt rutnät.

    Formeln bygger på att cube-koordinater uppfyller:
        x + y + z = 0

    Avståndet kan beräknas som:
        max(|dx|, |dy|, |dz|)

    vilket är ekvivalent med:
        (|dx| + |dy| + |dz|) / 2

    Parametrar:
        a_x, a_y, a_z: första punkten
        b_x, b_y, b_z: andra punkten

    Returnerar:
        int: antal steg mellan punkterna
    """
    dx = abs(a_x - b_x)
    dy = abs(a_y - b_y)
    dz = abs(a_z - b_z)

    return max(dx, dy, dz)


def axial_distance(a_q: int, a_r: int, b_q: int, b_r: int) -> int:
    """
    Beräknar hex-avståndet mellan två punkter i axial-koordinater.

    Detta görs genom att:
        1. Konvertera axial -> cube
        2. Använda cube_distance

    Parametrar:
        a_q, a_r: första punkten (axial)
        b_q, b_r: andra punkten (axial)

    Returnerar:
        int: antal steg mellan hexarna
    """
    a_x, a_y, a_z = axial_to_cube(a_q, a_r)
    b_x, b_y, b_z = axial_to_cube(b_q, b_r)

    return cube_distance(a_x, a_y, a_z, b_x, b_y, b_z)

def is_adjacent(aq: int, ar: int, bq: int, br: int) -> bool:
    """
    Kontrollerar om två hexar är grannar (adjacent).

    Två hexar är grannar om axiala distansen mellan dem är 1.

    Parametrar:
        aq, ar: första hexen (axial)
        bq, br: andra hexen (axial)
    
    Returnerar:
        bool: True om hexarna är grannar, annars False
    """
    return axial_distance(aq, ar, bq, br) == 1

