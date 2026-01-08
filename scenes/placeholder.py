from asciimatics.widgets import Frame, Layout, Label, Button
from asciimatics.scene import Scene
from asciimatics.exceptions import NextScene

class PlaceholderFrame(Frame):
    def __init__(self, screen, title, name):
        super(PlaceholderFrame, self).__init__(screen,
                                             height=10,
                                             width=40,
                                             name=name,
                                             title=title)
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Label(f"{title} - Under Construction"))
        layout.add_widget(Button("Back", self._back))
        self.fix()

    def _back(self):
        raise NextScene("MainMenu")

def get_scene(screen, name, title):
    return Scene([PlaceholderFrame(screen, title, name)], -1, name=name)
