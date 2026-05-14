"""
Main program - Roomba robot simulation
Automatic cleaning scheduler and controller
"""

from controller import RobotController
import time


def main():
    print("""
    ╔════════════════════════════════════════╗
    ║         ROOMBA ROBOT SYSTEM v2.0       ║
    ║    Automated Home Cleaning System      ║
    ║   Learning HW ↔ SW Communication      ║
    ╚════════════════════════════════════════╝
    """)
    
    # Initialize controller with cleaning schedule
    # Cleans at 14:00 (2 PM) in all 3 rooms
    controller = RobotController(
        cleaning_hours=[14],
        cleaning_rooms=["living_room", "kitchen", "bedroom"]
    )
    
    # Start robot
    controller.start()
    
    # Run simulation - simulate 50 iterations
    # In real application, this would run continuously
    try:
        for iteration in range(1, 51):
            print(f"\n{'='*60}")
            print(f"ITERATION {iteration}")
            print(f"{'='*60}")
            
            # Update robot state
            controller.update(iteration)
            
            # Display status
            time.sleep(0.2)  # Time for "real work"
            controller.print_status()
            
            # Wait before next iteration
            time.sleep(1.0)
    
    except KeyboardInterrupt:
        print("\n\n⛔ User interrupt!")
    
    finally:
        # Stop robot
        controller.stop()
        print("\n✓ Program completed successfully!")


if __name__ == "__main__":
    main()
