# 🤖 Architektura Systemu Robota Mobilnego

## Struktura projektu

```
robot_project/
├── src/
│   ├── hardware_simulator.py   # Symulacja sprzętu (silniki, czujniki)
│   ├── controller.py           # Logika sterowania robotem
│   └── main.py                 # Główny program
├── ARCHITEKTURA.md             # Ten plik - dokumentacja
└── README.md                   # Instrukcja użytkownika
```

## Komponenty systemu

### 1️⃣ **Hardware Simulator** (`hardware_simulator.py`)
Symuluje rzeczywisty sprzęt robota:
- **Motor (2 szt.)** - lewy i prawy silnik
  - `speed`: -100 do +100 (%)
  - Metody: `set_speed()`, `stop()`
- **SonarSensor** - czujnik ultradźwiękowy
  - Mierzy odleglosc do przeszkód (cm)
  - Metody: `measure()`, `get_distance()`
- **Robot** - klasa integrująca HW
  - Metody sterowania: `move_forward()`, `turn_left()`, `stop()`
  - Metoda `read_sonar()` - odczyt czujnika

### 2️⃣ **Controller** (`controller.py`)
Zawiera logikę AI robota:
- **RobotController** - mózg systemu
  - Stan robota: IDLE, MOVING, AVOIDING
  - `obstacle_avoidance_logic()` - algorytm unikania przeszkód
  - `update()` - aktualizacja w każdej iteracji

### 3️⃣ **Main** (`main.py`)
Program główny:
- Inicjalizacja systemu
- Pętla symulacji (20 iteracji)
- Wyswietlenie statusu robota

---

## 📡 Komunikacja między modułami

```
┌─────────────────────────────────────────────┐
│         HARDWARE SIMULATOR                  │
├─────────────────────────────────────────────┤
│  Motor(LEFT)  │  Motor(RIGHT)  │  Sonar    │
└────────┬──────────────────────┬─────────────┘
         │                      │
    [Rozkazy]              [Dane czujników]
         │                      │
         ↓                      ↓
┌─────────────────────────────────────────────┐
│         ROBOT (Hub danych)                  │
├─────────────────────────────────────────────┤
│  • move_forward()                           │
│  • read_sonar()                             │
│  • get_status()                             │
└────────┬──────────────────────────────────┬─┘
         │                                  │
    [Rozkazy do silników]    [Dane statusu]
         │                                  │
         ↓                                  ↓
┌─────────────────────────────────────────────┐
│         CONTROLLER (Logika decyzyjna)      │
├─────────────────────────────────────────────┤
│  • obstacle_avoidance_logic()               │
│  • update()                                 │
│  • print_status()                           │
└─────────────────────────────────────────────┘
```

---

## 🔄 Przepływ pracy

### Iteracja systemu:
1. **main.py** → Pętla główna
2. **RobotController.update()** → Aktualizacja logiki
3. **simulate_environment()** → Symulacja danych z czujników
4. **obstacle_avoidance_logic()** → Decyzja (jechać / unikać)
5. **Robot.move_forward()** / **turn_right()** → Rozkazy do silników
6. **Motor.set_speed()** → Ustawienie prędkości
7. **print_status()** → Wyswietlenie statusu

---

## 🎯 Algorytm unikania przeszkód

```
START
  ↓
Czytaj czujnik odleglosci
  ↓
Czy odleglosc < 30cm?
  ├─ TAK: Przeszkoda blisko!
  │   ├─ Stop()
  │   ├─ move_backward(40%)
  │   ├─ turn_right(50%)
  │   └─ move_forward(50%)
  │
  └─ NIE: Droga wolna
      └─ move_forward(50%)
```

---

## 💡 Koncepty edukacyjne

### Komunikacja Hardware ↔ Software
- **HW wysyła dane**: Czujnik mierzy odleglosc
- **SW odbiera dane**: Controller czyta `read_sonar()`
- **SW wysyła rozkazy**: `move_forward()` ustawia silnik
- **HW wykonuje**: Motor się obraca

### Event-driven system
- Każda zmiana w czujniku trigger'uje akcję
- Kontroler reaguje na zdarzenia (przeszkoda = event)

### State Machine (Maszyna stanów)
- Robot ma stany: IDLE → MOVING → AVOIDING → MOVING...

---

## 🚀 Uruchomienie

```bash
cd src
python main.py
```

**Oczekiwany wynik:**
- 20 iteracji symulacji
- Robot wykrywa przeszkody (iteracje 5-10, 15+)
- Unika ich i kontynuuje
- Każde działanie logowane w konsoli
