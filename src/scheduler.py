"""
Cleaning scheduler - determines when and where to clean
"""
from datetime import datetime


class CleaningScheduler:
    """Manages cleaning schedule and room assignment"""
    
    def __init__(self, cleaning_hours=None, cleaning_rooms=None):
        """
        Initialize scheduler
        cleaning_hours: list of hours when robot should clean (0-23)
        cleaning_rooms: list of rooms to clean in order
        """
        self.cleaning_hours = cleaning_hours or [14]  # Default: 2 PM
        self.cleaning_rooms = cleaning_rooms or ["living_room", "kitchen", "bedroom"]
        self.current_room_index = 0
    
    def should_start_cleaning(self):
        """Check if current hour matches cleaning time"""
        current_hour = datetime.now().hour
        return current_hour in self.cleaning_hours
    
    def get_next_room(self):
        """Get next room to clean"""
        if self.current_room_index < len(self.cleaning_rooms):
            room = self.cleaning_rooms[self.current_room_index]
            return room
        return None
    
    def advance_to_next_room(self):
        """Move to next room in schedule"""
        self.current_room_index += 1
    
    def reset_rooms(self):
        """Reset room index for next cleaning cycle"""
        self.current_room_index = 0
    
    def get_all_rooms(self):
        """Get list of all rooms to clean"""
        return self.cleaning_rooms
    
    def print_schedule(self):
        """Print cleaning schedule"""
        print(f"\n📋 CLEANING SCHEDULE:")
        print(f"  Hours: {self.cleaning_hours}")
        print(f"  Rooms: {', '.join(self.cleaning_rooms)}")
        print(f"  Current room index: {self.current_room_index}\n")
