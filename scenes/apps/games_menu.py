from asciimatics.widgets import Frame, Layout, Button, Divider, Label
from asciimatics.scene import Scene
from asciimatics.exceptions import NextScene

class GamesMenuFrame(Frame):
    def __init__(self, screen):
        super(GamesMenuFrame, self).__init__(screen,
                                           height=14,
                                           width=40,
                                           title="Games Arcade",
                                           hover_focus=True)
        
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        
        layout.add_widget(Label("Select a Game:"))
        layout.add_widget(Divider())
        
        layout.add_widget(Button("Rock Paper Scissors", self._rps))
        layout.add_widget(Button("Quick Math", self._math))
        layout.add_widget(Button("Hangman", self._hangman))
        layout.add_widget(Button("Chess vs AI", self._chess))
        layout.add_widget(Button("Lucky Number", self._lucky))
        
        layout.add_widget(Divider())
        layout.add_widget(Button("Back", self._back))
        
        self.fix()

    def _rps(self): raise NextScene("RPS")
    def _math(self): raise NextScene("MathGame")
    def _hangman(self): raise NextScene("Hangman")
    def _chess(self): raise NextScene("Chess")
    def _lucky(self): raise NextScene("LuckyNumber")
    def _back(self): raise NextScene("MainMenu")

def get_scene(screen):
    return Scene([GamesMenuFrame(screen)], -1, name="Games")
