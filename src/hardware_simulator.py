"""
Symulacja Hardware'u robota
Reprezentuje czujniki (sonar, kamera) i silniki
"""

class Motor:
    """Symulacja silnika"""
    def __init__(self, name):
        self.name = name
        self.speed = 0  # -100 do 100 (% moc)
        self.is_running = False
    
    def set_speed(self, speed):
        """Ustawianie predkości silnika"""
        self.speed = max(-100, min(100, speed))  # Ograniczenie -100 do 100
        self.is_running = speed != 0
        print(f"[MOTOR {self.name}] Predkosc: {self.speed}%")
    
    def stop(self):
        """Zatrzymanie silnika"""
        self.speed = 0
        self.is_running = False
        print(f"[MOTOR {self.name}] Stop")


class SonarSensor:
    """Symulacja czujnika ultradźwiękowego (odleglosc)"""
    def __init__(self, name):
        self.name = name
        self.distance = 0.0  # Odleglosc w cm
    
    def measure(self, obstacle_distance):
        """Pomiar odleglosci do przeszkody"""
        self.distance = obstacle_distance
        return self.distance
    
    def get_distance(self):
        """Zwrócenie ostatniego pomiaru"""
        return self.distance


class Robot:
    """Glowna klasa robota - lacznik miedzy HW i SW"""
    def __init__(self):
        # Silniki
        self.left_motor = Motor("LEFT")
        self.right_motor = Motor("RIGHT")
        
        # Czujniki
        self.sonar = SonarSensor("SONAR_FRONT")
        
        # Stan robota
        self.position = (0, 0)  # x, y
        self.direction = 0  # 0-360 stopni
        self.obstacle_detected = False
    
    def move_forward(self, speed=50):
        """Przód"""
        self.left_motor.set_speed(speed)
        self.right_motor.set_speed(speed)
        print(f"[ROBOT] Ruch do przodu - predkosc: {speed}%")
    
    def move_backward(self, speed=50):
        """Tył"""
        self.left_motor.set_speed(-speed)
        self.right_motor.set_speed(-speed)
        print(f"[ROBOT] Ruch do tylu - predkosc: {speed}%")
    
    def turn_left(self, speed=50):
        """Skreç w lewo"""
        self.left_motor.set_speed(-speed)
        self.right_motor.set_speed(speed)
        print(f"[ROBOT] Skreç lewo")
    
    def turn_right(self, speed=50):
        """Skreç w prawo"""
        self.left_motor.set_speed(speed)
        self.right_motor.set_speed(-speed)
        print(f"[ROBOT] Skreç prawo")
    
    def stop(self):
        """Zatrzymanie"""
        self.left_motor.stop()
        self.right_motor.stop()
        print(f"[ROBOT] Stop")
    
    def read_sonar(self):
        """Odczyt sensora odleglosci"""
        distance = self.sonar.get_distance()
        if distance < 30:  # Mniej niz 30cm
            self.obstacle_detected = True
        else:
            self.obstacle_detected = False
        return distance
    
    def get_status(self):
        """Pobranie statusu robota"""
        return {
            "left_motor_speed": self.left_motor.speed,
            "right_motor_speed": self.right_motor.speed,
            "sonar_distance": self.sonar.distance,
            "obstacle": self.obstacle_detected,
            "position": self.position,
            "direction": self.direction
        }
