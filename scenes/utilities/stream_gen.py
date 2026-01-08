from asciimatics.widgets import Frame, Layout, Label, Button, Text, TextBox
from asciimatics.scene import Scene
from asciimatics.exceptions import NextScene
import random
import string

class StreamGenFrame(Frame):
    def __init__(self, screen):
        super(StreamGenFrame, self).__init__(screen, height=20, width=60, title="Stream Gen")
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        
        self._search = Text("Search Seq:", "search")
        layout.add_widget(self._search)
        
        self._stream_box = TextBox(12, as_string=True, name="stream")
        layout.add_widget(self._stream_box)
        
        layout2 = Layout([1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Generate", self._gen), 0)
        layout2.add_widget(Button("Search", self._do_search), 1)
        layout2.add_widget(Button("Back", self._back), 2)
        self.fix()

    def _gen(self):
        # Generate 1000 chars
        chars = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*", k=1000))
        self.data['stream'] = chars
        self._stream_box.value = chars

    def _do_search(self):
        self.save()
        query = self.data['search']
        content = self.data['stream']
        if not query: return
        
        count = content.count(query)
        # Highlight? TextBox doesn't support rich highlighting easily in this mode without parser.
        # Just show count.
        self._stream_box.value = f"Found {count} occurrences of '{query}'\n\n" + content

    def _back(self): raise NextScene("Utilities")

def get_scene(screen):
    return Scene([StreamGenFrame(screen)], -1, name="StreamGen")
