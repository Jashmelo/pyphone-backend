from asciimatics.widgets import Frame, Layout, Button, Divider, Label
from asciimatics.scene import Scene
from asciimatics.exceptions import NextScene

class UtilitiesMenuFrame(Frame):
    def __init__(self, screen):
        super(UtilitiesMenuFrame, self).__init__(screen,
                                           height=14,
                                           width=40,
                                           title="Utilities",
                                           hover_focus=True)
        
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        
        layout.add_widget(Label("Tools:"))
        layout.add_widget(Divider())
        
        layout.add_widget(Button("Calculator", self._calc))
        layout.add_widget(Button("Weather", self._weather))
        layout.add_widget(Button("Stream Generator", self._stream))
        layout.add_widget(Button("Converters", self._converters))
        
        layout.add_widget(Divider())
        layout.add_widget(Button("Back", self._back))
        
        self.fix()

    def _calc(self): raise NextScene("Calculator")
    def _weather(self): raise NextScene("Weather")
    def _stream(self): raise NextScene("StreamGen")
    def _converters(self): raise NextScene("Converters")
    def _back(self): raise NextScene("MainMenu")

def get_scene(screen):
    return Scene([UtilitiesMenuFrame(screen)], -1, name="Utilities")
