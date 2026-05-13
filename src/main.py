"""
Główny program - uruchomienie systemu robota
"""

from controller import RobotController
import time


def main():
    print("""
    ╔════════════════════════════════════════╗
    ║     SYSTEM ROBOTA MOBILNEGO v1.0      ║
    ║   Nauka komunikacji HW ↔ SW           ║
    ╚════════════════════════════════════════╝
    """)
    
    # Inicjalizacja kontrolera
    controller = RobotController()
    
    # Uruchomienie robota
    controller.start()
    
    # Symulacja 20 iteracji (każda iteracja = ~1 sekunda)
    try:
        for iteration in range(1, 21):
            print(f"\n{'='*50}")
            print(f"ITERACJA {iteration}")
            print(f"{'='*50}")
            
            # Aktualizacja robota
            controller.update(iteration)
            
            # Wyswietlenie statusu
            time.sleep(0.3)  # Chwila na "rzeczywistą" pracę
            controller.print_status()
            
            # Czekanie przed następną iteracją
            time.sleep(1.5)
    
    except KeyboardInterrupt:
        print("\n\n⛔ Przerwanie przez użytkownika!")
    
    finally:
        # Zatrzymanie robota
        controller.stop()
        print("\n✓ Program zakończony pomyślnie!")


if __name__ == "__main__":
    main()
