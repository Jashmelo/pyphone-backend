from asciimatics.widgets import Frame, Layout, ListBox, Button, Divider, Label, Text, TextBox, PopUpDialog
from asciimatics.scene import Scene
from asciimatics.exceptions import NextScene
import database
import session

# Shared state
view_message_content = ""
view_message_from = ""

class InboxFrame(Frame):
    def __init__(self, screen):
        super(InboxFrame, self).__init__(screen,
                                       height=screen.height * 3 // 4,
                                       width=screen.width * 3 // 4,
                                       on_load=self._on_load,
                                       title="Inbox")
        
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        
        self._list_box = ListBox(
            height=10,
            options=[],
            name="messages",
            on_select=self._view_message,
        )
        layout.add_widget(self._list_box)
        layout.add_widget(Divider())
        
        layout2 = Layout([1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Compose", self._compose), 0)
        layout2.add_widget(Button("Back", self._back), 1)
        
        self.fix()

    def _on_load(self):
        user = session.get_user()
        msgs = database.get_messages(user)
        # Display: "From: Content..."
        # Value: index
        options = []
        for idx, m in enumerate(reversed(msgs)): # Newest first
            snippet = m['content'][:20].replace("\n", " ")
            label = f"[{m['timestamp']}] {m['from']}: {snippet}..."
            options.append((label, idx))
        
        self._list_box.options = options

    def _view_message(self):
        if self._list_box.value is None: return
        
        user = session.get_user()
        msgs = list(reversed(database.get_messages(user)))
        msg = msgs[self._list_box.value]
        
        global view_message_content, view_message_from
        view_message_content = msg['content']
        view_message_from = msg['from']
        
        raise NextScene("ViewMessage")

    def _compose(self):
        raise NextScene("ComposeMessage")

    def _back(self):
        raise NextScene("MainMenu")

class ViewMessageFrame(Frame):
    def __init__(self, screen):
        super(ViewMessageFrame, self).__init__(screen, height=15, width=50, on_load=self._on_load, title="Message")
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        
        self._from_lbl = Label("")
        self._content_box = TextBox(8, as_string=True)
        self._content_box.disabled = True
        
        layout.add_widget(self._from_lbl)
        layout.add_widget(Divider())
        layout.add_widget(self._content_box)
        
        layout2 = Layout([100])
        self.add_layout(layout2)
        layout2.add_widget(Button("Back", self._back))
        self.fix()

    def _on_load(self):
        global view_message_content, view_message_from
        self._from_lbl.text = f"From: {view_message_from}"
        self._content_box.value = view_message_content

    def _back(self):
        raise NextScene("Messaging")

class ComposeFrame(Frame):
    def __init__(self, screen):
        super(ComposeFrame, self).__init__(screen, height=15, width=50, title="Compose")
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        
        self._to = Text("To:", "to")
        self._content = TextBox(8, label="Message:", name="content", as_string=True)
        self._status = Label("")
        
        layout.add_widget(self._to)
        layout.add_widget(self._content)
        layout.add_widget(self._status)
        
        layout2 = Layout([1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Send", self._send), 0)
        layout2.add_widget(Button("Cancel", self._cancel), 1)
        self.fix()

    def _send(self):
        self.save()
        to_user = self.data['to']
        content = self.data['content']
        
        if not to_user:
            self._status.text = "Recipient required"
            return
            
        database.send_message(session.get_user(), to_user, content)
        # Maybe show popup?
        raise NextScene("Messaging")

    def _cancel(self):
        raise NextScene("Messaging")

def get_scenes(screen):
    return [
        Scene([InboxFrame(screen)], -1, name="Messaging"),
        Scene([ViewMessageFrame(screen)], -1, name="ViewMessage"),
        Scene([ComposeFrame(screen)], -1, name="ComposeMessage")
    ]
