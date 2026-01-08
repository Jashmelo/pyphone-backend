from asciimatics.widgets import Frame, Layout, ListBox, Button, Divider, TextBox, Text, Label
from asciimatics.scene import Scene
from asciimatics.exceptions import NextScene
import database
import session
import datetime

class FeedbackFrame(Frame):
    def __init__(self, screen):
        super(FeedbackFrame, self).__init__(screen, height=15, width=50, title="Feedback", on_load=self._on_load)
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        
        # Mode 1: Send Feedack
        self._msg_lbl = Label("Send Feedback to Admin:")
        self._content = TextBox(5, name="content", as_string=True)
        self._status = Label("")
        
        # Mode 2: View Inbox (Admin only)
        self._list = ListBox(10, [], name="list")
        
        # Widgets added to layout, but logic determines what is active/visible?
        # Asciimatics doesn't have "visible=False" easily.
        # Use two Frames? Or re-add widgets.
        # Simpler: Two Layouts?
        pass # Will implement dynamic layout in on_load or separate frames
    
    def _on_load(self):
        pass

class SendFeedbackFrame(Frame):
    def __init__(self, screen):
        super(SendFeedbackFrame, self).__init__(screen, height=15, width=50, title="Send Feedback")
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        
        layout.add_widget(Label("Describe your issue/idea:"))
        self._content = TextBox(5, name="content", as_string=True)
        layout.add_widget(self._content)
        
        layout2 = Layout([1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Send", self._send), 0)
        layout2.add_widget(Button("Back", self._back), 1)
        self.fix()

    def _send(self):
        self.save()
        database.send_feedback(session.get_user(), self.data['content'])
        raise NextScene("MainMenu") # Or confirm

    def _back(self): raise NextScene("MainMenu")

class AdminFeedbackFrame(Frame):
    def __init__(self, screen):
        super(AdminFeedbackFrame, self).__init__(screen, height=20, width=60, title="Admin Inbox", on_load=self._on_load)
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        
        self._list = ListBox(15, [], name="list")
        layout.add_widget(self._list)
        layout.add_widget(Button("Back", self._back))
        self.fix()

    def _on_load(self):
        feedbacks = database.get_feedback()
        # "User (Time): Content"
        options = []
        for i, f in enumerate(feedbacks):
            t = f"{f['user']} ({f['timestamp']}): {f['content'][:30]}"
            options.append((t, i))
        self._list.options = options

    def _back(self): raise NextScene("MainMenu")

def get_scenes(screen):
    # Logic: How to direct to Admin vs User?
    # Both Frames are registered. MainMenu calls "Feedback".
    # BUT MainMenu needs to know which one to call.
    # OR we use an Intermediate Scene "Feedback" that immediately raising NextScene based on user.
    # No, Scene effects run. Frame runs.
    # I'll create a "FeedbackRoutingFrame" that auto-redirects?
    # Or just register both and have MainMenu decide?
    # MainMenu Frame doesn't easily check user specifics in the button callback unless I update logic there.
    # I'll update MainMenu logic to check admin status.
    # NO: Easier -> "Feedback" Scene contains a Frame that checks user on `_on_load` and swaps layout?
    # Or simplified: User always sees Send, Admin sees Inbox?
    # Let's make "Feedback" Scene use `SendFeedbackFrame`.
    # And "AdminFeedback" Scene use `AdminFeedbackFrame`.
    # And have MainMenu check.
    return [
        Scene([SendFeedbackFrame(screen)], -1, name="Feedback"),
        Scene([AdminFeedbackFrame(screen)], -1, name="AdminFeedback")
    ]
