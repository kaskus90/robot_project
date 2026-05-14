"""
Home mapper - defines room locations and cleaning patterns
"""


class HomeMap:
    """Defines layout of house and room locations"""
    
    def __init__(self):
        """Initialize home map with room coordinates"""
        self.obstacles = set()  # Set of (x, y) grid coords blocked by obstacles

        self.rooms = {
            "living_room": {
                "name": "Living Room",
                "x_range": (0, 100),
                "y_range": (0, 100),
                "grid_size": 10
            },
            "kitchen": {
                "name": "Kitchen",
                "x_range": (100, 200),
                "y_range": (0, 100),
                "grid_size": 10
            },
            "bedroom": {
                "name": "Bedroom",
                "x_range": (0, 100),
                "y_range": (100, 200),
                "grid_size": 10
            }
        }
    
    def get_room_coordinates(self, room_name):
        """Get x, y range for a room"""
        if room_name in self.rooms:
            room = self.rooms[room_name]
            return room["x_range"], room["y_range"]
        return None, None
    
    def get_cleaning_grid(self, room_name):
        """Get grid pattern for cleaning a room"""
        if room_name not in self.rooms:
            return []
        
        room = self.rooms[room_name]
        x_start, x_end = room["x_range"]
        y_start, y_end = room["y_range"]
        grid_size = room["grid_size"]
        
        grid_points = []
        for x in range(x_start, x_end, grid_size):
            for y in range(y_start, y_end, grid_size):
                grid_points.append((x, y))
        
        return grid_points
    
    def get_room_name(self, room_key):
        """Get human-readable room name"""
        if room_key in self.rooms:
            return self.rooms[room_key]["name"]
        return room_key
    
    def get_dock_position(self):
        """Get charging dock position"""
        return (210, 50)  # Near kitchen
    
    def add_obstacle(self, x, y):
        self.obstacles.add((x, y))

    def remove_obstacle(self, x, y):
        self.obstacles.discard((x, y))

    def is_obstacle(self, x, y):
        return (x, y) in self.obstacles

    def get_room_at(self, x, y):
        """Return room key if (x,y) is inside a room, else None"""
        for room_key, room in self.rooms.items():
            x_start, x_end = room["x_range"]
            y_start, y_end = room["y_range"]
            if x_start <= x < x_end and y_start <= y < y_end:
                return room_key
        return None

    def print_map(self):
        """Print home layout"""
        print("\n🏠 HOME MAP:")
        for room_key, room_data in self.rooms.items():
            x_range, y_range = room_data["x_range"], room_data["y_range"]
            print(f"  {room_data['name']}: X{x_range} Y{y_range}")
        dock_x, dock_y = self.get_dock_position()
        print(f"  Dock: ({dock_x}, {dock_y})\n")
