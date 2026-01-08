from asciimatics.widgets import Frame, Layout, ListBox, Button, Divider, Label, TextBox, Text
from asciimatics.scene import Scene
from asciimatics.exceptions import NextScene
import database
import session

# Shared state to pass note ID between List and Edit frames
current_note_id = None

class NotesListFrame(Frame):
    def __init__(self, screen):
        super(NotesListFrame, self).__init__(screen,
                                           height=screen.height * 3 // 4,
                                           width=screen.width * 3 // 4,
                                           on_load=self._on_load,
                                           title="My Notes")
        
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        
        self._list_box = ListBox(
            height=10,
            options=[],
            name="notes_list",
            on_select=self._edit_note,
        )
        layout.add_widget(self._list_box)
        layout.add_widget(Divider())
        
        layout2 = Layout([1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("New Note", self._new_note), 0)
        layout2.add_widget(Button("Delete", self._delete_note), 1)
        layout2.add_widget(Button("Back", self._back), 2)
        
        self.fix()

    def _on_load(self):
        user = session.get_user()
        if not user: return
        notes = database.get_notes(user)
        # Options format: [(Label, Value), ...]
        options = [(f"{n['title']} ({n['timestamp']})", n['id']) for n in notes]
        self._list_box.options = options
        self._list_box.value = None # clear selection

    def _new_note(self):
        global current_note_id
        current_note_id = None
        raise NextScene("NoteEdit")

    def _edit_note(self):
        global current_note_id
        if self._list_box.value is None: return
        current_note_id = self._list_box.value
        raise NextScene("NoteEdit")

    def _delete_note(self):
        if self._list_box.value is None: return
        database.delete_note(session.get_user(), self._list_box.value)
        self._on_load() # refresh

    def _back(self):
        raise NextScene("MainMenu")

class NoteEditFrame(Frame):
    def __init__(self, screen):
        super(NoteEditFrame, self).__init__(screen,
                                          height=screen.height * 3 // 4,
                                          width=screen.width * 3 // 4,
                                          on_load=self._on_load,
                                          title="Edit Note")
        
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        
        self._title = Text("Title:", "title")
        self._content = TextBox(10, label="Content:", name="content", as_string=True)
        
        layout.add_widget(self._title)
        layout.add_widget(self._content)
        layout.add_widget(Divider())
        
        layout2 = Layout([1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Save", self._save), 0)
        layout2.add_widget(Button("Cancel", self._cancel), 1)
        
        self.fix()

    def _on_load(self):
        global current_note_id
        user = session.get_user()
        self.data = {"title": "", "content": ""}
        
        if current_note_id is not None:
             notes = database.get_notes(user)
             for n in notes:
                 if n['id'] == current_note_id:
                     self.data['title'] = n['title']
                     self.data['content'] = n['content']
                     break
        # Force redraw data
        self.save() # Reset internal widgets to the self.data
        # Update widgets manually because self.data assignment doesn't always reflect
        self._title.value = self.data['title']
        self._content.value = self.data['content']

    def _save(self):
        self.save() # widget -> data
        global current_note_id
        user = session.get_user()
        database.save_note(user, self.data['title'], self.data['content'], current_note_id)
        raise NextScene("Notes")

    def _cancel(self):
        raise NextScene("Notes")

def get_scenes(screen):
    return [
        Scene([NotesListFrame(screen)], -1, name="Notes"),
        Scene([NoteEditFrame(screen)], -1, name="NoteEdit")
    ]
