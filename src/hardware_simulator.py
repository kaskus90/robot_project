"""
Robot hardware simulation
Represents sensors (sonar, camera) and motors
"""

class Motor:
    """Motor simulation"""
    def __init__(self, name):
        self.name = name
        self.speed = 0  # -100 to 100 (% power)
        self.is_running = False
    
    def set_speed(self, speed):
        """Set motor speed"""
        self.speed = max(-100, min(100, speed))  # Limit -100 to 100
        self.is_running = speed != 0
        print(f"[MOTOR {self.name}] Speed: {self.speed}%")
    
    def stop(self):
        """Stop motor"""
        self.speed = 0
        self.is_running = False
        print(f"[MOTOR {self.name}] Stopped")


class SonarSensor:
    """Simulation of ultrasonic sensor (distance)"""
    def __init__(self, name):
        self.name = name
        self.distance = 0.0  # Distance in cm
    
    def measure(self, obstacle_distance):
        """Measure distance to obstacle"""
        self.distance = obstacle_distance
        return self.distance
    
    def get_distance(self):
        """Get last measurement"""
        return self.distance


class DustSensor:
    """Simulation of dust bin level sensor"""
    def __init__(self):
        self.dust_level = 0  # 0-100 %
    
    def add_dust(self, amount):
        """Add dust during cleaning"""
        self.dust_level = min(100, self.dust_level + amount)
    
    def get_level(self):
        """Get dust bin level"""
        return self.dust_level
    
    def empty(self):
        """Empty the dust bin"""
        self.dust_level = 0
        print("[DUST SENSOR] Bin emptied")


class Robot:
    """Main robot class - connection between HW and SW"""
    def __init__(self):
        # Movement motors
        self.left_motor = Motor("LEFT")
        self.right_motor = Motor("RIGHT")
        
        # Cleaning motors
        self.brush_motor = Motor("BRUSH")
        self.vacuum_motor = Motor("VACUUM")
        
        # Sensors
        self.sonar = SonarSensor("SONAR_FRONT")
        self.dust_sensor = DustSensor()
        
        # Robot state
        self.position = (0, 0)  # x, y
        self.direction = 0  # 0-360 degrees
        self.obstacle_detected = False
        self.battery_level = 100  # Battery %
        self.docked = False
    
    def move_forward(self, speed=50):
        """Move forward"""
        self.left_motor.set_speed(speed)
        self.right_motor.set_speed(speed)
        print(f"[ROBOT] Moving forward - speed: {speed}%")
    
    def move_backward(self, speed=50):
        """Move backward"""
        self.left_motor.set_speed(-speed)
        self.right_motor.set_speed(-speed)
        print(f"[ROBOT] Moving backward - speed: {speed}%")
    
    def turn_left(self, speed=50):
        """Turn left"""
        self.left_motor.set_speed(-speed)
        self.right_motor.set_speed(speed)
        print(f"[ROBOT] Turning left")
    
    def turn_right(self, speed=50):
        """Turn right"""
        self.left_motor.set_speed(speed)
        self.right_motor.set_speed(-speed)
        print(f"[ROBOT] Turning right")
    
    def stop(self):
        """Stop all motors"""
        self.left_motor.stop()
        self.right_motor.stop()
        print(f"[ROBOT] Stopped")
    
    def start_cleaning(self):
        """Start brush and vacuum"""
        self.brush_motor.set_speed(100)
        self.vacuum_motor.set_speed(100)
        print("[ROBOT] 🧹 Cleaning started - brush and vacuum ON")
    
    def stop_cleaning(self):
        """Stop brush and vacuum"""
        self.brush_motor.stop()
        self.vacuum_motor.stop()
        print("[ROBOT] Cleaning stopped")
    
    def dock(self):
        """Return to dock station"""
        self.docked = True
        self.stop()
        self.stop_cleaning()
        print("[ROBOT] 🏠 Docked at charging station")
    
    def undock(self):
        """Leave dock station"""
        self.docked = False
        self.battery_level = 100
        print("[ROBOT] ⚡ Battery fully charged, leaving dock")
    
    def drain_battery(self, amount=1):
        """Simulate battery drain"""
        self.battery_level = max(0, self.battery_level - amount)
        return self.battery_level

    def charge(self, amount=10):
        """Charge battery by amount percent"""
        self.battery_level = min(100, self.battery_level + amount)
        return self.battery_level
    
    def read_sonar(self):
        """Read distance sensor"""
        distance = self.sonar.get_distance()
        if distance < 30:  # Less than 30cm
            self.obstacle_detected = True
        else:
            self.obstacle_detected = False
        return distance
    
    def is_dust_bin_full(self):
        """Check if dust bin is full"""
        return self.dust_sensor.get_level() > 90  # Increased from 80%
    
    def get_status(self):
        """Get robot status"""
        return {
            "left_motor_speed": self.left_motor.speed,
            "right_motor_speed": self.right_motor.speed,
            "brush_motor_speed": self.brush_motor.speed,
            "vacuum_motor_speed": self.vacuum_motor.speed,
            "sonar_distance": self.sonar.distance,
            "obstacle": self.obstacle_detected,
            "position": self.position,
            "direction": self.direction,
            "dust_level": self.dust_sensor.get_level(),
            "battery": self.battery_level,
            "docked": self.docked
        }
