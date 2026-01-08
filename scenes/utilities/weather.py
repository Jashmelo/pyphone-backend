from asciimatics.widgets import Frame, Layout, Label, Button, Divider
from asciimatics.scene import Scene
from asciimatics.exceptions import NextScene
import random

SUN_ART = """
      \\   |   /
       .-'-.
    --|  O  |--
       '-.-'
      /   |   \\
"""

CLOUD_ART = """
      .--.
   .-(    ).
  (___.__)__)
"""

RAIN_ART = """
      .--.
   .-(    ).
  (___.__)__)
   ' ' ' '
    ' ' ' '
"""

class WeatherFrame(Frame):
    def __init__(self, screen):
        super(WeatherFrame, self).__init__(screen, height=20, width=40, title="Weather", on_load=self._on_load)
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        
        self._city = Label("Location: ...")
        self._temp = Label("Temp: ...")
        self._art = Label("", height=6)
        
        layout.add_widget(self._city)
        layout.add_widget(self._temp)
        layout.add_widget(Divider())
        layout.add_widget(self._art)
        
        layout2 = Layout([100])
        self.add_layout(layout2)
        layout2.add_widget(Button("Refresh", self._on_load))
        layout2.add_widget(Button("Back", self._back))
        self.fix()

    def _on_load(self):
        cities = ["New York", "London", "Tokyo", "Paris", "Sydney", "Moscow"]
        city = random.choice(cities)
        temp = random.randint(-5, 35)
        
        condition = "Sunny"
        art = SUN_ART
        if temp < 10:
            condition = "Rainy"
            art = RAIN_ART
        elif temp < 20:
            condition = "Cloudy"
            art = CLOUD_ART
            
        self._city.text = f"Loc: {city}"
        self._temp.text = f"{temp}°C ({condition})"
        self._art.text = art

    def _back(self):
        raise NextScene("Utilities")

def get_scene(screen):
    return Scene([WeatherFrame(screen)], -1, name="Weather")
