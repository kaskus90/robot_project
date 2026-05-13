"""
Kontroler robota - logika decyzyjne i sterowanie
"""

from hardware_simulator import Robot
import time


class RobotController:
    """Kontroler logiki robota"""
    
    def __init__(self):
        self.robot = Robot()
        self.running = False
        self.state = "IDLE"  # IDLE, MOVING, AVOIDING
        self.obstacle_threshold = 30  # cm
    
    def start(self):
        """Uruchomienie pracy robota"""
        self.running = True
        self.state = "MOVING"
        print("\n=== ROBOT URUCHOMIONY ===\n")
    
    def stop(self):
        """Zatrzymanie robota"""
        self.running = False
        self.robot.stop()
        print("\n=== ROBOT ZATRZYMANY ===\n")
    
    def obstacle_avoidance_logic(self):
        """
        Logika unikania przeszkód:
        - Jechać do przodu
        - Gdy czujnik wykryje przeszkodę -> zatrzymać i skręcić
        - Kontynuować
        """
        distance = self.robot.read_sonar()
        
        if distance < self.obstacle_threshold:
            # Przeszkoda blisko!
            self.state = "AVOIDING"
            print(f"\n⚠️  PRZESZKODA WYKRYTA! Odleglosc: {distance}cm")
            
            # Zatrzymanie
            self.robot.stop()
            time.sleep(0.5)
            
            # Cofnięcie
            print("↶ Cofam...")
            self.robot.move_backward(speed=40)
            time.sleep(1.0)
            
            # Skręt
            print("↻ Skreçam...")
            self.robot.turn_right(speed=50)
            time.sleep(1.5)
            
            # Powrót do przodu
            self.state = "MOVING"
            self.robot.move_forward(speed=50)
        else:
            # Droga wolna - jazda do przodu
            if self.state != "MOVING":
                self.state = "MOVING"
            self.robot.move_forward(speed=50)
    
    def simulate_environment(self, iteration):
        """Symulacja zmiennego otoczenia"""
        # Przeszkody pojawiają się w określonych iteracjach
        if iteration < 5:
            distance = 100  # Droga wolna
        elif iteration < 10:
            distance = 25   # Przeszkoda!
        elif iteration < 15:
            distance = 100  # Znów wolna
        else:
            distance = 40   # Przeszkoda bliżej
        
        # Symulacja pomiaru
        self.robot.sonar.measure(distance)
        return distance
    
    def update(self, iteration):
        """Aktualizacja stanu robota (wywołanie w każdej iteracji)"""
        if not self.running:
            return
        
        # Symulacja czujników
        self.simulate_environment(iteration)
        
        # Logika sterowania
        self.obstacle_avoidance_logic()
    
    def print_status(self):
        """Wyswietlenie statusu robota"""
        status = self.robot.get_status()
        print(f"\n📊 STATUS ROBOTA:")
        print(f"  Stan: {self.state}")
        print(f"  Lewy silnik: {status['left_motor_speed']}%")
        print(f"  Prawy silnik: {status['right_motor_speed']}%")
        print(f"  Odleglosc: {status['sonar_distance']}cm")
        print(f"  Przeszkoda: {'TAK' if status['obstacle'] else 'NIE'}")
        print(f"  Pozycja: {status['position']}")
