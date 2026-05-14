"""
Visual simulator - Display robot cleaning in real-time with GUI
Uses tkinter for 2D visualization of the house and robot
"""

import tkinter as tk
from tkinter import Canvas, Label, Frame
import time
from controller import RobotController


class RobotVisualizer:
    """Visual representation of robot cleaning"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 Roomba Robot Cleaner - Visual Simulator")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")
        
        # Create controller
        self.controller = RobotController(
            cleaning_hours=[14],
            cleaning_rooms=["living_room", "kitchen", "bedroom"]
        )
        
        # Visual settings
        self.scale = 1.5  # Scale for drawing (1 unit = 1.5 pixels)
        self.grid_size = 10  # Grid cells
        self.robot_size = 8
        
        # Rooms with colors
        self.rooms = {
            "living_room": {"color": "#FFE6CC", "name": "Living Room", "x": 0, "y": 0, "w": 100, "h": 100},
            "kitchen": {"color": "#E6F2FF", "name": "Kitchen", "x": 100, "y": 0, "w": 100, "h": 100},
            "bedroom": {"color": "#F2E6FF", "name": "Bedroom", "x": 0, "y": 100, "w": 100, "h": 100}
        }
        
        # Track cleaned cells
        self.cleaned_cells = {}
        for room in self.rooms:
            self.cleaned_cells[room] = set()
        
        # Create GUI elements
        self.create_widgets()
        
        # Start simulation
        self.controller.start()
        self.running = True
        self.start_cleaning()
    
    def create_widgets(self):
        """Create GUI layout"""
        # Top panel
        top_frame = Frame(self.root, bg="#333333", height=60)
        top_frame.pack(side=tk.TOP, fill=tk.X)
        top_frame.pack_propagate(False)
        
        title_label = Label(top_frame, text="🏠 ROOMBA VISUAL SIMULATOR", 
                           font=("Arial", 16, "bold"), bg="#333333", fg="white")
        title_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Main content frame
        content_frame = Frame(self.root, bg="#f0f0f0")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas for drawing
        self.canvas = Canvas(content_frame, bg="white", width=600, height=600, 
                            highlightthickness=2, highlightbackground="#333333")
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Info panel
        info_frame = Frame(content_frame, bg="#ffffff", width=300, relief=tk.SUNKEN, bd=2)
        info_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH)
        info_frame.pack_propagate(False)
        
        # Status labels
        Label(info_frame, text="📊 STATUS", font=("Arial", 12, "bold"), 
              bg="#ffffff").pack(pady=10)
        
        self.status_labels = {}
        
        status_items = [
            ("State", "state"),
            ("Current Room", "room"),
            ("Position", "position"),
            ("Battery", "battery"),
            ("Dust Bin", "dust"),
            ("Motors", "motors"),
            ("Cleaned %", "cleaned")
        ]
        
        for label_text, key in status_items:
            frame = Frame(info_frame, bg="#ffffff")
            frame.pack(fill=tk.X, padx=10, pady=5)
            
            Label(frame, text=f"{label_text}:", font=("Arial", 10, "bold"), 
                  bg="#ffffff", width=12, anchor="w").pack(side=tk.LEFT)
            
            status_label = Label(frame, text="---", font=("Arial", 10), 
                                bg="#ffffff", fg="#0066cc", anchor="w")
            status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            self.status_labels[key] = status_label
        
        # Draw initial map
        self.draw_map()
    
    def draw_map(self):
        """Draw house layout"""
        self.canvas.delete("all")
        
        # Draw rooms
        for room_key, room in self.rooms.items():
            x1 = room["x"] * self.scale
            y1 = room["y"] * self.scale
            x2 = (room["x"] + room["w"]) * self.scale
            y2 = (room["y"] + room["h"]) * self.scale
            
            # Room background
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=room["color"], 
                                        outline="#333333", width=2)
            
            # Room label
            cx = (x1 + x2) / 2
            cy = (y1 + y2) / 2
            self.canvas.create_text(cx, cy, text=room["name"], font=("Arial", 10, "bold"))
            
            # Draw grid
            self.draw_grid(room_key, room)
        
        # Draw dock station
        dock_x, dock_y = self.controller.home_map.get_dock_position()
        dock_x1 = dock_x * self.scale - 5
        dock_y1 = dock_y * self.scale - 5
        dock_x2 = dock_x * self.scale + 5
        dock_y2 = dock_y * self.scale + 5
        self.canvas.create_rectangle(dock_x1, dock_y1, dock_x2, dock_y2, 
                                     fill="#FFD700", outline="#FF6600", width=2)
        self.canvas.create_text(dock_x, dock_y, text="🏠", font=("Arial", 12))
    
    def draw_grid(self, room_key, room):
        """Draw cleaned grid cells for a room"""
        grid_size = self.grid_size
        
        for x in range(room["x"], room["x"] + room["w"], grid_size):
            for y in range(room["y"], room["y"] + room["h"], grid_size):
                x1 = x * self.scale
                y1 = y * self.scale
                x2 = (x + grid_size) * self.scale
                y2 = (y + grid_size) * self.scale
                
                # Check if cell is cleaned
                cell_key = (x, y)
                if cell_key in self.cleaned_cells[room_key]:
                    cell_color = "#90EE90"  # Light green
                    outline = "#00AA00"
                else:
                    cell_color = "white"
                    outline = "#CCCCCC"
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=cell_color, 
                                            outline=outline, width=1)
    
    def draw_robot(self, x, y):
        """Draw robot on canvas"""
        robot_x = x * self.scale
        robot_y = y * self.scale
        
        size = self.robot_size
        self.canvas.create_oval(robot_x - size, robot_y - size, 
                               robot_x + size, robot_y + size, 
                               fill="#FF6600", outline="#FF3300", width=2)
        self.canvas.create_text(robot_x, robot_y, text="🤖", font=("Arial", 12))
    
    def start_cleaning(self):
        """Start cleaning and animation loop"""
        self.controller.cleaning_mode = True
        self.controller.state = "CLEANING"
        self.controller.robot.undock()
        
        rooms_to_clean = self.controller.scheduler.get_all_rooms()
        
        self.clean_rooms_animation(rooms_to_clean, 0)
    
    def clean_rooms_animation(self, rooms, room_index):
        """Animate cleaning of rooms"""
        if not self.running or room_index >= len(rooms):
            if self.running:
                # All rooms done
                self.controller.go_to_dock()
                self.update_status()
                self.controller.stop()
            return
        
        room_name = rooms[room_index]
        room = self.rooms[room_name]
        
        self.controller.navigate_to_room(room_name)
        grid_points = self.controller.home_map.get_cleaning_grid(room_name)
        
        # Keep cleaning this room until done (handle multiple dock cycles)
        self.clean_room_completely(room_name, room, grid_points, 0, rooms, room_index)
    
    def clean_room_completely(self, room_name, room, grid_points, start_point, rooms, room_index):
        """Clean a room completely, docking as needed"""
        self.clean_grid_animation(room_name, room, grid_points, start_point, rooms, room_index, 
                                 complete_room=True)
    
    def clean_grid_animation(self, room_name, room, grid_points, point_index, rooms, room_index, complete_room=False):
        """Animate cleaning of grid points in a room"""
        if not self.running or point_index >= len(grid_points):
            # Room done - move to next room
            self.controller.scheduler.advance_to_next_room()
            self.root.after(500, lambda: self.clean_rooms_animation(rooms, room_index + 1))
            return
        
        x, y = grid_points[point_index]
        
        # Update cleaned cells
        self.cleaned_cells[room_name].add((x, y))
        
        # Simulate dust collection
        self.controller.robot.dust_sensor.add_dust(0.5)  # Even less dust
        self.controller.robot.drain_battery(0.2)  # Less battery drain
        
        # Check conditions - DOCK IF NEEDED BUT RETURN TO SAME ROOM
        if self.controller.robot.is_dust_bin_full():
            print(f"⚠️  Dust bin full at point {point_index + 1}/{len(grid_points)} in {room_name}")
            self.controller.go_to_dock()
            self.update_status()
            # Continue cleaning the SAME room after docking
            self.root.after(1000, lambda: self.clean_grid_animation(
                room_name, room, grid_points, point_index + 1, rooms, room_index, complete_room=True))
            return
        
        if self.controller.robot.battery_level < 15:
            print(f"🔋 Battery low at point {point_index + 1}/{len(grid_points)}")
            self.controller.go_to_dock()
            self.update_status()
            # Continue cleaning the SAME room after docking
            self.root.after(1000, lambda: self.clean_grid_animation(
                room_name, room, grid_points, point_index + 1, rooms, room_index, complete_room=True))
            return
        
        # Draw map and robot
        self.draw_map()
        self.draw_robot(x, y)
        
        # Update status
        self.update_status()
        
        # Move to next point
        self.root.after(100, lambda: self.clean_grid_animation(
            room_name, room, grid_points, point_index + 1, rooms, room_index, complete_room=complete_room))
    
    def update_status(self):
        """Update status panel"""
        status = self.controller.robot.get_status()
        
        self.status_labels["state"].config(text=self.controller.state)
        self.status_labels["room"].config(
            text=self.controller.home_map.get_room_name(self.controller.current_room) 
            if self.controller.current_room else "None")
        self.status_labels["position"].config(
            text=f"({status['position'][0]}, {status['position'][1]})")
        self.status_labels["battery"].config(
            text=f"{status['battery']:.1f}% {'🔴' if status['battery'] < 20 else '🟢'}")
        self.status_labels["dust"].config(
            text=f"{status['dust_level']}% {'⚠️' if status['dust_level'] > 80 else '✓'}")
        
        motors_on = sum([1 for m in [status['left_motor_speed'], status['right_motor_speed'],
                                     status['brush_motor_speed'], status['vacuum_motor_speed']]
                        if m != 0])
        self.status_labels["motors"].config(text=f"{motors_on} running")
        
        # Calculate cleaned percentage
        total_cells = sum(len(points) for points in self.cleaned_cells.values())
        total_possible = 3 * 10 * 10  # 3 rooms, 10x10 grid each
        cleaned_pct = (total_cells / total_possible) * 100
        self.status_labels["cleaned"].config(text=f"{cleaned_pct:.1f}%")
        
        self.root.update()
    
    def on_closing(self):
        """Handle window close"""
        self.running = False
        self.controller.stop()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = RobotVisualizer(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
