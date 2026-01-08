from asciimatics.widgets import Frame, Layout, Button, Divider, Label
from asciimatics.scene import Scene
from asciimatics.effects import Stars, Print
from asciimatics.renderers import FigletText, Box
from asciimatics.exceptions import NextScene
import session
import database

class MainMenuFrame(Frame):
    def __init__(self, screen):
        super(MainMenuFrame, self).__init__(screen,
                                          height=screen.height * 2 // 3,
                                          width=screen.width * 2 // 3,
                                          on_load=self._on_load,
                                          hover_focus=True,
                                          has_border=True,
                                          title="PyPhone OS Home")
        
        # self.set_theme("green") 

        # Header
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Label("PyPhone v1.0", align="^"))
        layout.add_widget(Divider())
        
        # Grid of Apps (Buttons)
        # 3 Columns
        grid_layout = Layout([1, 1, 1])
        self.add_layout(grid_layout)
        
        grid_layout.add_widget(Button("Notes", self._notes), 0)
        grid_layout.add_widget(Button("Messaging", self._messaging), 1)
        grid_layout.add_widget(Button("Friends", self._friends), 2)
        
        grid_layout.add_widget(Button("Games", self._games), 0)
        grid_layout.add_widget(Button("Utilities", self._utilities), 1)
        grid_layout.add_widget(Button("Custom Apps", self._custom), 2)
        
        grid_layout.add_widget(Button("Feedback", self._feedback), 0)
        
        # Bottom controls
        footer_layout = Layout([1, 1])
        self.add_layout(footer_layout)
        footer_layout.add_widget(Divider(), 0)
        footer_layout.add_widget(Divider(), 1)
        
        footer_layout.add_widget(Button("Settings", self._settings), 0)
        footer_layout.add_widget(Button("Logout", self._logout), 1)
        
        self.fix()
        
    def _on_load(self):
        # Update dynamic elements if needed
        pass

    def _notes(self):
        raise NextScene("Notes")

    def _messaging(self):
        raise NextScene("Messaging")
        
    def _friends(self):
        raise NextScene("Friends")

    def _feedback(self):
        # Check Admin
        user = session.get_user()
        user_data = database.get_user(user)
        if user_data and user_data.get('is_admin'):
            raise NextScene("AdminFeedback")
        else:
            raise NextScene("Feedback")

    def _games(self):
        raise NextScene("Games")

    def _utilities(self):
        raise NextScene("Utilities")

    def _custom(self):
        raise NextScene("CustomApps")

    def _settings(self):
        raise NextScene("Settings")

    def _logout(self):
        session.logout()
        raise NextScene("Login")

def get_scene(screen):
    # Background effects
    effects = [
        Stars(screen, 200),
        # Print(screen, FigletText("PyPhone", font='slant'), 
        #       y=screen.height//2 - 8, speed=1, stop_frame=100),
        MainMenuFrame(screen)
    ]
    return Scene(effects, -1, name="MainMenu")
