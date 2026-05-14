"""
Demo script - Shows Roomba cleaning in action
Forces cleaning mode to demonstrate the full cycle
"""

from controller import RobotController
import time


def demo_cleaning():
    print("""
    ╔════════════════════════════════════════╗
    ║    ROOMBA CLEANING DEMO - v2.0        ║
    ║   Demonstration of cleaning cycle     ║
    ╚════════════════════════════════════════╝
    """)
    
    # Initialize controller
    controller = RobotController(
        cleaning_hours=[14],
        cleaning_rooms=["living_room", "kitchen", "bedroom"]
    )
    
    # Start robot
    controller.start()
    
    print("\n🚀 STARTING DEMO - FORCING CLEANING MODE\n")
    
    # Force cleaning mode
    controller.cleaning_mode = True
    controller.state = "CLEANING"
    controller.robot.undock()
    
    try:
        # Clean all rooms
        rooms_to_clean = controller.scheduler.get_all_rooms()
        
        for room_name in rooms_to_clean:
            print(f"\n{'='*70}")
            print(f"CLEANING ROOM: {controller.home_map.get_room_name(room_name).upper()}")
            print(f"{'='*70}\n")
            
            controller.navigate_to_room(room_name)
            time.sleep(1)
            
            success = controller.clean_room(room_name)
            
            if not success:
                print("\n❌ Cleaning interrupted - need to dock!")
                break
            
            controller.scheduler.advance_to_next_room()
            time.sleep(1)
            
            # Print status
            controller.print_status()
            time.sleep(1)
        
        # Return to dock
        if controller.cleaning_mode:
            print(f"\n{'='*70}")
            print("CLEANING CYCLE COMPLETE - RETURNING TO DOCK")
            print(f"{'='*70}\n")
            
            controller.go_to_dock()
            controller.cleaning_mode = False
            controller.state = "IDLE"
            
            print("\n✅ ALL ROOMS CLEANED SUCCESSFULLY!\n")
            controller.print_status()
    
    except KeyboardInterrupt:
        print("\n\n⛔ Demo interrupted!")
    
    finally:
        controller.stop()
        print("\n✓ Demo completed!")


if __name__ == "__main__":
    demo_cleaning()
