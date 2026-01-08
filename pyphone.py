from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.exceptions import ResizeScreenError
import sys

# Core
import auth

# Menus
from scenes import main_menu
from scenes import settings
from scenes.apps import games_menu, utilities_menu

# Apps
from scenes.apps import notes, messaging, friends, feedback
from scenes import custom_apps

# Games
from scenes.games import rps, chess_game, simple_games

# Utilities
from scenes.utilities import calculator, weather, converters, stream_gen

def demo(screen, scene):
    scenes = []
    
    # Auth
    scenes.extend(auth.get_scenes(screen))
    
    # Main Menu & Settings
    scenes.append(main_menu.get_scene(screen))
    scenes.append(settings.get_scene(screen))
    
    # Sub-Menus
    scenes.append(games_menu.get_scene(screen))
    scenes.append(utilities_menu.get_scene(screen))
    
    # Productivity Apps
    scenes.extend(notes.get_scenes(screen))
    scenes.extend(messaging.get_scenes(screen))
    scenes.extend(friends.get_scenes(screen))
    scenes.extend(feedback.get_scenes(screen))
    scenes.extend(custom_apps.get_scenes(screen))
    
    # Games
    scenes.append(rps.get_scene(screen))
    scenes.append(chess_game.get_scene(screen))
    scenes.extend(simple_games.get_scenes(screen))
    
    # Utilities
    scenes.append(calculator.get_scene(screen))
    scenes.append(weather.get_scene(screen))
    scenes.append(converters.get_scene(screen))
    scenes.append(stream_gen.get_scene(screen))
    
    screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)

if __name__ == "__main__":
    last_scene = None
    while True:
        try:
            Screen.wrapper(demo, catch_interrupt=True, arguments=[last_scene])
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene
