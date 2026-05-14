"""
Pathfinding agent - A* algorithm for navigating around obstacles on a grid
"""

import heapq


class PathfindingAgent:
    """Finds shortest obstacle-free path between two grid positions using A*"""

    def __init__(self, grid_size=10):
        self.grid_size = grid_size

    def find_path(self, start, goal, obstacles, room_bounds):
        """
        Returns list of (x, y) positions from start to goal, or [] if no path exists.
        room_bounds: (x_min, y_min, x_max, y_max)
        """
        x_min, y_min, x_max, y_max = room_bounds

        if goal in obstacles:
            return []

        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        def neighbors(pos):
            x, y = pos
            for nx, ny in [
                (x + self.grid_size, y),
                (x - self.grid_size, y),
                (x, y + self.grid_size),
                (x, y - self.grid_size),
            ]:
                if x_min <= nx < x_max and y_min <= ny < y_max and (nx, ny) not in obstacles:
                    yield (nx, ny)

        open_set = [(0, start)]
        came_from = {}
        g_score = {start: 0}
        visited = set()

        while open_set:
            _, current = heapq.heappop(open_set)

            if current in visited:
                continue
            visited.add(current)

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            for nb in neighbors(current):
                new_g = g_score[current] + self.grid_size
                if nb not in g_score or new_g < g_score[nb]:
                    came_from[nb] = current
                    g_score[nb] = new_g
                    heapq.heappush(open_set, (new_g + heuristic(nb, goal), nb))

        return []
