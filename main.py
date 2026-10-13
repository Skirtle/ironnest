import math

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
    A = ref_1_coords[0]
    B = ref_1_coords[1]
    C = ref_2_coords[0]
    D = ref_2_coords[1]
    
    
    theta_0 = ((-ref_1_bearing - 270) * math.pi) / 180
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
    else: raise ValueError(f"idk")
    
    x = A + res * math.cos(theta_0)
    y = B + res * math.sin(theta_0)

    return (int(x), int(y))

nest = grid_to_coord("G4 1:1")
spotter_1 = grid_to_coord("C5 2:3")
spotter_2 = grid_to_coord("B6 0:6")
spotter_3 = grid_to_coord("A4 5:5")

ref_alpha = coord_from_bearing_distance(spotter_1, 69, spotter_2, 14.73)
print(coord_to_grid(ref_alpha))
print(coord_to_grid(coord_from_bearing_distance(ref_alpha, 207, spotter_1, 10.02)))