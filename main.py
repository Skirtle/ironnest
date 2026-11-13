from math import sqrt, pi, sin, cos, tan, dist
from random import randint, seed

def bearing_to_radians(theta: float) -> float: return ((-theta - 270) * pi) / 180

def quadratic(a: float | int, b: float | int, c: float | int) -> tuple[float, float]:
    if (a == 0): raise ValueError(f"a cannot be zero")
    
    discrim = b*b - 4*a*c
    if (discrim < 0): raise ValueError(f"No real roots exist")
    
    discrim_sqrt = sqrt(discrim)
    
    x1 = (-b + discrim_sqrt) / (2 * a)
    x2 = (-b - discrim_sqrt) / (2 * a)
    return (x1, x2)

def grid_to_coord(inp: str) -> tuple[int, int]:
    """The grid used in Iron Nest

    Args:
        inp (str): Iron Nest's coordinates

    Returns:
        tuple[int, int]: The coordinates (in meters)
    """
    # inp expected to be in format of "N# #:#"
    split_input = inp.split(" ")
    grid = split_input[0]
    subgrid = split_input[1].split(":")
    
    # Get main grid coords
    grid_x = (ord(grid[0]) - 65) * 1000
    grid_y = (int(grid[1]) - 1) * 1000
    
    # Get subgrid coords
    subgrid_x = int(subgrid[0]) * 100
    subgrid_y = int(subgrid[1]) * 100
    
    return (grid_x + subgrid_x, grid_y + subgrid_y)

def coord_to_grid(inp: tuple[int | float, int | float]) -> str:
    """Convert real coordinates into coordinates for use in Iron Nest

    Args:
        inp (tuple[int  |  float, int  |  float]): The coordinates (in meters)

    Returns:
        str: The grid used in Iron Nest
    """
    # (0, 0) is equal to A1 0:0
    x = int(inp[0])
    y = int(inp[1])
    
    major_grid_x = x // 1000
    major_grid_y = y // 1000
    
    minor_grid_x = int(round((x - (major_grid_x * 1000)) / 100))
    minor_grid_y = int(round((y - (major_grid_y * 1000)) / 100))
    
    return f"{chr(major_grid_x + 65)}{major_grid_y + 1} {minor_grid_x}:{minor_grid_y}"

def coord_from_bearing_distance(ref_1_coords: tuple[int, int], ref_1_bearing: int, ref_2_coords: tuple[int, int], ref_2_distance: float) -> tuple[int, int]:
    """Calculate the coordinates of a target using a bearing from one point and distance from another point

    Args:
        ref_1_coords (tuple[int, int]): coordinates (in meters) of reference point 1
        ref_1_bearing (int): bearing (in degrees, North = 0, clockwise) from reference point 1
        ref_2_coords (tuple[int, int]): coordinates (in meters) of reference point 2
        ref_2_distance (float): distance (in kilometers) from reference point 2

    Raises:
        ValueError: There are no points that intersect

    Returns:
        tuple[int, int]: coordinates (in meters) of target
    """
    A = ref_1_coords[0]
    B = ref_1_coords[1]
    C = ref_2_coords[0]
    D = ref_2_coords[1]
    
    
    theta_0 = bearing_to_radians(ref_1_bearing)
    r = 1000 * ref_2_distance 
    
    E = A - C
    G = B - D
    
    b = 2 * (E * cos(theta_0) + G * sin(theta_0))
    c = (E * E) + (G * G) - (r * r)
    
    root = sqrt((b * b) - (4 * c))
    
    t_1 = (-b - root) / 2
    t_2 = (-b + root) / 2
    
    if (t_1 > 0): res = t_1
    elif (t_2 > 0): res = t_2
    else: raise ValueError(f"No intersection found")
    
    x = A + res * cos(theta_0)
    y = B + res * sin(theta_0)

    return (int(x), int(y))

def coords_from_two_bearings(ref_1_coords: tuple[int, int], ref_1_bearing: int, ref_2_coords: tuple[int, int], ref_2_bearing: int) -> tuple[int, int]:
    """Calculate the coordinates of a target using the bearing from one point and the bearing from another point

    Args:
        ref_1_coords (tuple[int, int]): coordinates (in meters) of reference point 1
        ref_1_bearing (int): bearing (in degrees, North = 0, clockwise) from reference point 1
        ref_2_coords (tuple[int, int]): coordinates (in meters) of reference point 2
        ref_2_bearing (int): bearing (in degrees, North = 0, clockwise) from reference point 2

    Raises:
        ValueError:There is no intersection point

    Returns:
        tuple[int, int]: coordinates (in meters) of target
    """
    a = bearing_to_radians(ref_1_bearing)
    b = bearing_to_radians(ref_2_bearing)
    
    A = ref_1_coords[0]
    B = ref_1_coords[1]
    C = ref_2_coords[0]
    D = ref_2_coords[1]
    
    x0_numer = -(A * tan(a)) + (C * tan(b)) + B - D
    x0_denom = tan(b) - tan(a)
    x0 = x0_numer / x0_denom
    
    t1 = (x0 - A) / cos(a)
    t2 = (x0 - C) / cos(b)
    
    if (t1 < 0 or t2 < 0): raise ValueError(f"No intersection points")
    
    y0 = B + (x0 - A) * tan(a)
    return (round(x0), round(y0))

def coords_from_two_distances(ref_1_coords: tuple[int, int], ref_1_distance: float, ref_2_coords: tuple[int, int], ref_2_distance: float) -> tuple[tuple[int, int], tuple[int, int]]:
    """Calculate the coordinates of a target using the distance from one point and the distance from another point

    Args:
        ref_1_coords (tuple[int, int]): coordinates (in meters) of reference point 1
        ref_1_distance (float): distance (in kilometers) from reference point 1
        ref_2_coords (tuple[int, int]): coordinates (in meters) of reference point 2
        ref_2_distance (float): distance (in kilometers) from reference point 2

    Returns:
        tuple[tuple[int, int], tuple[int, int]]: both possible coordinates (in meters) of the target
    """
    A = ref_1_coords[0]
    B = ref_1_coords[1]
    C = ref_2_coords[0]
    D = ref_2_coords[1]
    r1 = ref_1_distance * 1000
    r2 = ref_2_distance * 1000
    E = ((r1*r1) + (C*C) + (D*D)) - ((r2*r2) + (A*A) + (B*B))
    
    a = ((A - C) / (D - B)) ** 2 + 1
    b = ((E * (A - C)) / ((D - B) ** 2)) + ((2 * ((B * C) - (A * B))) / (D - B)) - (2 * A)
    c = ((E ** 2) / (4 * ((D - B) ** 2))) - ((B * E) / (D - B)) + (A ** 2) + (B ** 2) - (r1 ** 2)
    
    x1, x2 = quadratic(a, b, c)
    
    f = lambda x: int((2*x*(A-C) + r1**2 + C**2 + D**2 - A**2 - B**2 - r2**2) / (2 * (D-B)))
    return ((int(x1), f(x1)), (int(x2), f(x2)))

def create_game(game_seed: int | None = None, spotter_count: int = 3, target_count: int = 3, min_spotter_target_distance: int = 200, min_spotter_distance: int = 200, min_target_distance: int = 50):
    seed(game_seed)
    spotters: list[tuple[int, int]] = []
    targets: list[tuple[int, int]] = []
    for _ in range(spotter_count):
        pos = (randint(0, 20000), randint(0, 10000))
        for spotter in spotters:
            while (dist(pos, spotter) < min_spotter_distance):
                pos = (randint(0, 20000), randint(0, 10000))
        spotters.append(pos)
    
    for _ in range(target_count):
        pos = (randint(0, 20000), randint(0, 10000))
        for target in targets:
            while (dist(pos, target) < min_target_distance):
                pos = (randint(0, 20000), randint(0, 10000))
        targets.append(pos)
            
    
    print(spotters)
    print(targets)

create_game()