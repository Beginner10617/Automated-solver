from copy import deepcopy
from collections import deque

# Define all Tetris pieces and their rotations
TETRIS_PIECES = {
    'I': [
        [[1, 1, 1, 1]],
        [[1], [1], [1], [1]]
    ],
    'O': [
        [[1, 1],
         [1, 1]]
    ],
    'T': [
        [[0, 1, 0],
         [1, 1, 1]],
        [[1, 0],
         [1, 1],
         [1, 0]],
        [[1, 1, 1],
         [0, 1, 0]],
        [[0, 1],
         [1, 1],
         [0, 1]]
    ],
    'S': [
        [[0, 1, 1],
         [1, 1, 0]],
        [[1, 0],
         [1, 1],
         [0, 1]]
    ],
    'Z': [
        [[1, 1, 0],
         [0, 1, 1]],
        [[0, 1],
         [1, 1],
         [1, 0]]
    ],
    'J': [
        [[1, 0, 0],
         [1, 1, 1]],
        [[1, 1],
         [1, 0],
         [1, 0]],
        [[1, 1, 1],
         [0, 0, 1]],
        [[0, 1],
         [0, 1],
         [1, 1]]
    ],
    'L': [
        [[0, 0, 1],
         [1, 1, 1]],
        [[1, 0],
         [1, 0],
         [1, 1]],
        [[1, 1, 1],
         [1, 0, 0]],
        [[1, 1],
         [0, 1],
         [0, 1]]
    ]
}

WEIGHTS = {
    'aggregate_height': -0.510066,
    'complete_lines': 0.760666,
    'holes': -0.35663,
    'bumpiness': -0.184483
}

# ------------------- Utility Functions -------------------

def normalize(blocks):
    min_r = min(x for x, y in blocks)
    min_c = min(y for x, y in blocks)
    return [(x - min_r, y - min_c) for x, y in blocks]

def shape_from_coords(coords):
    coords = normalize(coords)
    max_r = max(x for x, y in coords)
    max_c = max(y for x, y in coords)
    shape = [[0] * (max_c + 1) for _ in range(max_r + 1)]
    for x, y in coords:
        shape[x][y] = 1
    return shape

def find_connected_components(grid):
    rows, cols = len(grid), len(grid[0])
    visited = [[False]*cols for _ in range(rows)]
    components = []

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and not visited[r][c]:
                queue = deque([(r, c)])
                visited[r][c] = True
                component = []
                while queue:
                    x, y = queue.popleft()
                    component.append((x, y))
                    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                        nx, ny = x+dx, y+dy
                        if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 1 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            queue.append((nx, ny))
                components.append(component)
    return components

def match_piece(shape):
    for piece_type, variants in TETRIS_PIECES.items():
        for idx, variant in enumerate(variants):
            if shape == variant:
                return piece_type, idx
    return None, None

# ------------------- Grid Processing -------------------

def isolate_falling_piece(grid):
    components = find_connected_components(grid)
    four_blocks = [comp for comp in components if len(comp) == 4]
    if not four_blocks:
        return None, None

    # Assume falling piece is the highest 4-block shape
    falling_piece = sorted(four_blocks, key=lambda comp: min(x for x, y in comp))[0]

    new_grid = [[0]*len(grid[0]) for _ in range(len(grid))]
    for x, y in falling_piece:
        new_grid[x][y] = 1
    return new_grid, falling_piece

# ------------------- Evaluation -------------------

def count_complete_lines(grid):
    return sum(all(cell == 1 for cell in row) for row in grid)

def get_column_heights(grid):
    heights = [0] * 10
    for col in range(10):
        for row in range(20):
            if grid[row][col] == 1:
                heights[col] = 20 - row
                break
    return heights

def count_holes(grid):
    holes = 0
    for col in range(10):
        block_found = False
        for row in range(20):
            if grid[row][col] == 1:
                block_found = True
            elif block_found:
                holes += 1
    return holes

def calculate_bumpiness(heights):
    return sum(abs(heights[i] - heights[i+1]) for i in range(9))

def evaluate(grid):
    heights = get_column_heights(grid)
    return (
        WEIGHTS['aggregate_height'] * sum(heights) +
        WEIGHTS['complete_lines'] * count_complete_lines(grid) +
        WEIGHTS['holes'] * count_holes(grid) +
        WEIGHTS['bumpiness'] * calculate_bumpiness(heights)
    )

# ------------------- Simulation -------------------

def drop_piece(grid, shape, x_pos):
    g = deepcopy(grid)
    height = len(shape)
    width = len(shape[0])

    for y in range(0, 21 - height):
        collision = False
        for dy in range(height):
            for dx in range(width):
                if shape[dy][dx] == 1 and g[y + dy][x_pos + dx] == 1:
                    collision = True
                    break
            if collision:
                break
        if collision:
            y -= 1
            break
    else:
        y = 20 - height

    if y < 0:
        return None

    for dy in range(height):
        for dx in range(width):
            if shape[dy][dx] == 1:
                g[y + dy][x_pos + dx] = 1
    return g

def find_best_move(grid, piece_shapes):
    best_score = float('-inf')
    best_rotation_index = 0
    best_x = 0

    for rot_index, shape in enumerate(piece_shapes):
        width = len(shape[0])
        for x in range(10 - width + 1):
            new_grid = drop_piece(grid, shape, x)
            if new_grid:
                score = evaluate(new_grid)
                if score > best_score:
                    best_score = score
                    best_rotation_index = rot_index
                    best_x = x
    return best_rotation_index, best_x

# ------------------- Main -------------------

def decide_best_move(original_grid):
    falling_only_grid, falling_coords = isolate_falling_piece(original_grid)
    if falling_only_grid is None:
        print("No falling piece detected.")
        return ""

    piece_shape = shape_from_coords(falling_coords)
    piece_type, current_rotation = match_piece(piece_shape)
    if piece_type is None:
        print("Unknown piece shape.")
        return ""

    piece_shapes = TETRIS_PIECES[piece_type]

    # Calculate current x-position from falling piece's min column
    current_x = min(y for x, y in falling_coords) - min(y for x, y in normalize(falling_coords))

    best_rotation, best_x = find_best_move(original_grid, piece_shapes)

    moves = ""
    rotation_diff = (best_rotation - current_rotation) % len(piece_shapes)
    moves += "K <UP>\n" * rotation_diff
    dx = best_x - current_x
    moves += ("K <LEFT>\n" * -dx) if dx < 0 else ("K <RIGHT>\n" * dx)
    moves += "K <SPACE>\n"  # Drop the piece
    return moves.strip()

# ------------------- Test Cases -------------------

if __name__ == "__main__":
    test_grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, ],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, ],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, ],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, ],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, ],
    [0, 1, 1, 0, 0, 0, 0, 0, 0, 1, ],
    [1, 1, 0, 0, 0, 0, 0, 1, 1, 1, ],
    ]

    move = decide_best_move(test_grid)
    print(move)
    # Expected output: K <UP> K <LEFT> K <LEFT>