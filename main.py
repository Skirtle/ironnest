import math

def bearing_to_radians(theta: float) -> float: return ((-theta - 270) * math.pi) / 180

def grid_to_coord(inp: str) -> tuple[int, int]:
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
    
    b = 2 * (E * math.cos(theta_0) + G * math.sin(theta_0))
    c = (E * E) + (G * G) - (r * r)
    
    root = math.sqrt((b * b) - (4 * c))
    
    t_1 = (-b - root) / 2
    t_2 = (-b + root) / 2
    
    if (t_1 > 0): res = t_1
    elif (t_2 > 0): res = t_2
    else: raise ValueError(f"No intersection found")
    
    x = A + res * math.cos(theta_0)
    y = B + res * math.sin(theta_0)

    return (int(x), int(y))


def coords_from_two_bearings(ref_1_coords: tuple[int, int], ref_1_bearing: int, ref_2_coords: tuple[int, int], ref_2_bearing: int) -> tuple[int, int]:
    a = bearing_to_radians(ref_1_bearing)
    b = bearing_to_radians(ref_2_bearing)
    
    A = ref_1_coords[0]
    B = ref_1_coords[1]
    C = ref_2_coords[0]
    D = ref_2_coords[1]
    
    x0_numer = -(A * math.tan(a)) + (C * math.tan(b)) + B - D
    x0_denom = math.tan(b) - math.tan(a)
    x0 = x0_numer / x0_denom
    
    t1 = (x0 - A) / math.cos(a)
    t2 = (x0 - C) / math.cos(b)
    
    if (t1 < 0 or t2 < 0): raise ValueError(f"No intersection points")
    
    y0 = B + (x0 - A) * math.tan(a)
    return (round(x0), round(y0))

nest = grid_to_coord("C7 5:5")
spotter_1 = grid_to_coord("E1 8:8")
spotter_2 = grid_to_coord("C7 8:7")
spotter_3 = grid_to_coord("E3 1:9")

ref_alpha = coord_from_bearing_distance(spotter_1, 65, spotter_2, 8.21)
target_1 = coords_from_two_bearings(ref_alpha, 118, spotter_3, 99)
target_2 = coord_from_bearing_distance(ref_alpha, 181, spotter_1, 5.55)

print(f"{coord_to_grid(ref_alpha) = }")
print(f"{coord_to_grid(target_1) = }")
print(f"{coord_to_grid(target_2) = }")