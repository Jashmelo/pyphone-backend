import sys
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, StopApplication

# Import pyphone application logic
from pyphone import demo

def run_pyphone(start_scene=None):
    last_scene = start_scene
    while True:
        try:
            Screen.wrapper(demo, catch_interrupt=True, arguments=[last_scene])
            return
        except ResizeScreenError as e:
            last_scene = e.scene
        except StopApplication:
            return

def main():
    while True:
        print("\n=== PyPhone Launcher ===")
        print("1. Boot PyPhone OS")
        print("2. Binary Converter Tool")
        print("3. Stream Generator Tool")
        print("4. Quit")
        
        choice = input("Select Option: ").strip()
        
        if choice == '1':
            run_pyphone(start_scene="Login") # Or main menu if auto-login logic exists
        elif choice == '2':
            # Boot directly into Converters scene
            run_pyphone(start_scene="Converters")
        elif choice == '3':
            run_pyphone(start_scene="StreamGen")
        elif choice == '4':
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
