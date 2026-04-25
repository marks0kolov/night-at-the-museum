import random

from app.config import GRID_SIZES

DIFFICULTY_RULES = {
    "easy": {
        "gems": 1,
        "artifacts": 1,
        "guards": 1,
        "cycle_size": 1,
    },
    "medium": {
        "gems": 4,
        "artifacts": 2,
        "guards": 4,
        "cycle_size": 4,
    },
    "hard": {
        "gems": 10,
        "artifacts": 4,
        "guards": 5,
        "cycle_size": 8,
    },
}

GEM_SCORE = 1
ARTIFACT_SCORE = 3

# ============ CREATE MUSEUM ============

def _rooms_are_neighbors(room1, room2):
    """check if two rooms touch by side or diagonal"""
    s_x = abs(room1[0] - room2[0])
    s_y = abs(room1[1] - room2[1])
    return max(s_x, s_y) == 1

def _generate_random_path(difficulty):
    """create a random path from start to finish to be safe"""
    grid_w, grid_h = GRID_SIZES[difficulty]
    moves = ["right"] * (grid_w - 1) + ["down"] * (grid_h - 1)
    random.shuffle(moves)

    x, y = 0, 0
    path = [(x, y)]
    for move in moves:
        if move == "right":
            x += 1
        else:
            y += 1
        path.append((x, y))

    return path

def _get_guard_possible_next_rooms(available_rooms, safe_path, cycle, cycle_size):
    """find valid next rooms for the guard cycle"""
    cycle_index = len(cycle)
    # get forbidden rooms tht cannot be entered because of the safe path
    forbidden_rooms = set()
    for time, room in enumerate(safe_path):
        if time % cycle_size == cycle_index:
            forbidden_rooms.add(room)

    previous_room = cycle[-1] if cycle else None

    choices = []
    for room in available_rooms:
        if not (
            room in cycle # room already taken in cycle
            or room in forbidden_rooms # room forbidden
            or (
                previous_room 
                and not _rooms_are_neighbors(room, previous_room)
            ) # rooms aren't neighbors
        ):
            choices.append(room)

    random.shuffle(choices) # add randomness to make guards vary from run to run
    return choices

def _find_guard_cycle(available_rooms, safe_path, cycle_size, cycle=None):
    """build a continuous guard cycle using backtracking"""
    if cycle is None: # init cycle
        cycle = []

    if len(cycle) == cycle_size: # return cycle if it loops or return nothing if it doesn't
        if cycle_size == 1 or _rooms_are_neighbors(cycle[-1], cycle[0]):
            return cycle
        return []

    choices = _get_guard_possible_next_rooms(available_rooms, safe_path, cycle, cycle_size) # get possible choices
    for room in choices:
        result = _find_guard_cycle(available_rooms, safe_path, cycle_size, cycle + [room]) # check all possible path continuations recursively
        if result:
            return result

    return [] # pls don't happen

def generate_museum(difficulty):
    """generate gems, artifacts and guard cycles with one guaranteed safe path"""
    # get rules for current difficulty
    rules = DIFFICULTY_RULES[difficulty]
    grid_w, grid_h = GRID_SIZES[difficulty]

    # generate a guaranteed safe path so the game always has a solution
    safe_path = _generate_random_path(difficulty)

    # create a random list of rooms on which something can be placed
    rooms = [(x, y) for x in range(grid_w) for y in range(grid_h)]
    available_rooms = [room for room in rooms if room not in ((0, 0), (grid_w - 1, grid_h - 1))]
    random.shuffle(available_rooms)

    # place guards with wallking cycles
    guards = []
    for _ in range(rules["guards"]):
        cycle = _find_guard_cycle(available_rooms, safe_path, rules["cycle_size"])
        guards.append(cycle)

    # place gems
    gems = set(random.sample(available_rooms, rules["gems"]))
    available_rooms = [room for room in available_rooms if room not in gems]

    # place artifacts
    artifacts = set(random.sample(available_rooms, rules["artifacts"]))
    available_rooms = [room for room in available_rooms if room not in artifacts]

    # return generated museum structure
    return {
        "gems": gems,
        "artifacts": artifacts,
        "guards": guards,
        "safe_path": safe_path,
    }

# ============ SOLVE MUSEUM ============

def solve_museum(difficulty, museum):
    """use dp[x][y][t] to find the max score for a path from top-left to bottom-right"""
    grid_w, grid_h = GRID_SIZES[difficulty]
    finish = (grid_w - 1, grid_h - 1)
    steps = grid_w + grid_h - 2

    # dp[x][y][t] is the best score possible when standing in room (x, y) at time t. -1 means a guard.
    dp = [[[-1 for _ in range(steps + 1)] for _ in range(grid_h)] for _ in range(grid_w)]

    # start at (0, 0) at time 0
    dp[0][0][0] = 0

    for t in range(steps):
        # check guard positions at next move
        guard_positions = {cycle[(t + 1) % len(cycle)] for cycle in museum["guards"] if cycle}

        for x in range(grid_w):
            for y in range(grid_h):
                #  skip rooms that cannot be safely went through because of guards
                if dp[x][y][t] == -1:
                    continue

                for dx, dy in ((1, 0), (0, 1)):
                    new_x = x + dx
                    new_y = y + dy
                    new_pos = (new_x, new_y)

                    # ignore moves outside the grid
                    if new_x >= grid_w or new_y >= grid_h:
                        continue

                    # ignore moves into rooms with guards
                    if new_pos in guard_positions:
                        continue

                    # best score from previous room at previous time
                    score = dp[x][y][t]

                    # add score for each room
                    if new_pos in museum["gems"]:
                        score += GEM_SCORE
                    if new_pos in museum["artifacts"]:
                        score += ARTIFACT_SCORE

                    # Keep the best score for reaching this room at the next time.
                    dp[new_x][new_y][t + 1] = max(dp[new_x][new_y][t + 1], score)

    # If the finish is still -1, no safe route exists.
    return dp[finish[0]][finish[1]][steps]
