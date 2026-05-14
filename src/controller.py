"""
Robot controller - decision logic and control
Now with Roomba cleaning capabilities!
"""

from hardware_simulator import Robot
from scheduler import CleaningScheduler
from home_mapper import HomeMap
import time


class RobotController:
    """Roomba robot controller"""
    
    def __init__(self, cleaning_hours=None, cleaning_rooms=None):
        self.robot = Robot()
        self.scheduler = CleaningScheduler(cleaning_hours, cleaning_rooms)
        self.home_map = HomeMap()
        
        self.running = False
        self.state = "IDLE"  # IDLE, CLEANING, AVOIDING, DOCKING
        self.obstacle_threshold = 30  # cm
        self.current_room = None
        self.cleaning_mode = False
    
    def start(self):
        """Start robot operation"""
        self.running = True
        self.state = "IDLE"
        print("\n=== 🤖 ROOMBA ROBOT STARTED ===\n")
        self.home_map.print_map()
    
    def stop(self):
        """Stop robot"""
        self.running = False
        self.robot.stop()
        self.robot.stop_cleaning()
        print("\n=== 🛑 ROBOT STOPPED ===\n")
    
    def check_cleaning_schedule(self):
        """Check if it's time to start cleaning"""
        if self.scheduler.should_start_cleaning() and not self.cleaning_mode:
            print("\n⏰ TIME TO CLEAN! Starting cleaning cycle...\n")
            self.cleaning_mode = True
            self.state = "CLEANING"
            self.scheduler.reset_rooms()
            self.robot.undock()
            return True
        return False
    
    def navigate_to_room(self, room_name):
        """Navigate to target room"""
        self.current_room = room_name
        room_display = self.home_map.get_room_name(room_name)
        print(f"\n🗺️  Navigating to {room_display}...")
        self.state = "MOVING_TO_ROOM"
    
    def clean_room(self, room_name):
        """Clean a room using grid pattern"""
        if room_name not in self.robot.position:  # Just a check
            grid_points = self.home_map.get_cleaning_grid(room_name)
            room_display = self.home_map.get_room_name(room_name)
            
            print(f"\n🧹 Cleaning {room_display} with {len(grid_points)} grid points...")
            self.robot.start_cleaning()
            
            # Clean along grid pattern
            for i, (x, y) in enumerate(grid_points):
                self.robot.position = (x, y)
                self.robot.dust_sensor.add_dust(5)  # Simulate collecting dust
                
                if (i + 1) % 5 == 0:
                    print(f"  Progress: {i + 1}/{len(grid_points)} points cleaned")
                
                # Check if dust bin is full
                if self.robot.is_dust_bin_full():
                    print("  ⚠️  Dust bin full! Returning to dock...")
                    self.robot.stop_cleaning()
                    return False
                
                # Check battery
                self.robot.drain_battery(0.5)
                if self.robot.battery_level < 20:
                    print("  🔋 Battery low! Returning to dock...")
                    self.robot.stop_cleaning()
                    return False
                
                time.sleep(0.1)  # Simulate cleaning time
            
            print(f"  ✅ {room_display} cleaning complete!")
            self.robot.stop_cleaning()
            return True
    
    def go_to_dock(self):
        """Return to charging dock"""
        print("\n🏠 Returning to dock for charging and bin emptying...")
        dock_x, dock_y = self.home_map.get_dock_position()
        self.robot.position = (dock_x, dock_y)
        
        self.robot.dock()
        self.robot.dust_sensor.empty()
        
        print("✅ Docked and ready for next cleaning!\n")
        self.state = "DOCKED"
    
    def cleaning_cycle(self):
        """Execute complete cleaning cycle"""
        if not self.check_cleaning_schedule():
            return
        
        # Clean all rooms
        rooms_to_clean = self.scheduler.get_all_rooms()
        
        for room_name in rooms_to_clean:
            self.navigate_to_room(room_name)
            success = self.clean_room(room_name)
            
            if not success:
                # Need to go to dock
                self.go_to_dock()
                break
            
            self.scheduler.advance_to_next_room()
            time.sleep(0.5)
        
        # All rooms cleaned - return to dock
        if self.cleaning_mode:
            self.go_to_dock()
            self.cleaning_mode = False
            self.state = "IDLE"
    
    def obstacle_avoidance_logic(self):
        """
        Obstacle avoidance logic (for manual mode):
        - Move forward
        - When sensor detects obstacle -> stop and turn
        - Continue
        """
        if self.cleaning_mode:
            return  # Skip obstacle avoidance during cleaning
        
        distance = self.robot.read_sonar()
        
        if distance < self.obstacle_threshold:
            # Obstacle detected!
            self.state = "AVOIDING"
            print(f"\n⚠️  OBSTACLE DETECTED! Distance: {distance}cm")
            
            # Stop
            self.robot.stop()
            time.sleep(0.5)
            
            # Backup
            print("↶ Backing up...")
            self.robot.move_backward(speed=40)
            time.sleep(1.0)
            
            # Turn
            print("↻ Turning...")
            self.robot.turn_right(speed=50)
            time.sleep(1.5)
            
            # Resume forward
            self.state = "MOVING"
            self.robot.move_forward(speed=50)
        else:
            # Path clear - continue forward
            if self.state != "MOVING":
                self.state = "MOVING"
            self.robot.move_forward(speed=50)
    
    def simulate_environment(self, iteration):
        """Simulate changing environment"""
        # Obstacles appear at specific iterations
        if iteration < 5:
            distance = 100  # Clear
        elif iteration < 10:
            distance = 25   # Obstacle!
        elif iteration < 15:
            distance = 100  # Clear again
        else:
            distance = 40   # Obstacle
        
        # Simulate measurement
        self.robot.sonar.measure(distance)
        return distance
    
    def update(self, iteration):
        """Update robot state (call each iteration)"""
        if not self.running:
            return
        
        # Check if cleaning time
        self.cleaning_cycle()
        
        # Simulate sensors (if in manual mode)
        if not self.cleaning_mode:
            self.simulate_environment(iteration)
            self.obstacle_avoidance_logic()
        
        # Battery drain
        if not self.robot.docked:
            self.robot.drain_battery(0.01)
    
    def print_status(self):
        """Display robot status"""
        status = self.robot.get_status()
        print(f"\n📊 ROBOT STATUS:")
        print(f"  State: {self.state}")
        print(f"  Mode: {'🧹 CLEANING' if self.cleaning_mode else 'IDLE/MANUAL'}")
        print(f"  Left motor: {status['left_motor_speed']}%")
        print(f"  Right motor: {status['right_motor_speed']}%")
        print(f"  Brush motor: {status['brush_motor_speed']}%")
        print(f"  Vacuum motor: {status['vacuum_motor_speed']}%")
        print(f"  Distance: {status['sonar_distance']}cm")
        print(f"  Obstacle: {'YES ⚠️' if status['obstacle'] else 'NO'}")
        print(f"  Position: {status['position']}")
        print(f"  Dust bin: {status['dust_level']}%")
        print(f"  Battery: {status['battery']}%")
        print(f"  Docked: {'YES 🏠' if status['docked'] else 'NO'}")

