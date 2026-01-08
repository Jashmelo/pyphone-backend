from asciimatics.widgets import Frame, Layout, ListBox, Button, Divider, Label, Text
from asciimatics.scene import Scene
from asciimatics.exceptions import NextScene
import database
import session

class FriendsListFrame(Frame):
    def __init__(self, screen):
        super(FriendsListFrame, self).__init__(screen,
                                             height=screen.height * 3 // 4,
                                             width=screen.width * 3 // 4,
                                             on_load=self._on_load,
                                             title="Friends")
        
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        
        layout.add_widget(Label("My Friends:"))
        self._friends_list = ListBox(6, [], name="friends", on_select=None)
        layout.add_widget(self._friends_list)
        
        layout.add_widget(Divider())
        layout.add_widget(Label("Friend Requests:"))
        self._requests_list = ListBox(4, [], name="requests", on_select=self._accept_request)
        layout.add_widget(self._requests_list)
        
        layout.add_widget(Divider())
        
        layout2 = Layout([1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Add Friend", self._add_friend_view), 0)
        layout2.add_widget(Button("Remove", self._remove_friend), 1)
        layout2.add_widget(Button("Back", self._back), 2)
        
        self.fix()

    def _on_load(self):
        user = session.get_user()
        if not user: return
        
        friends = database.get_friends(user)
        self._friends_list.options = [(f, f) for f in friends]
        
        user_data = database.get_user(user)
        reqs = user_data.get('requests_received', [])
        self._requests_list.options = [(f"Req: {r}", r) for r in reqs]

    def _add_friend_view(self):
        raise NextScene("AddFriend")

    def _accept_request(self):
        if self._requests_list.value:
            database.accept_friend_request(session.get_user(), self._requests_list.value)
            self._on_load()

    def _remove_friend(self):
        if self._friends_list.value:
            database.remove_friend(session.get_user(), self._friends_list.value)
            self._on_load()

    def _back(self):
        raise NextScene("MainMenu")

class AddFriendFrame(Frame):
    def __init__(self, screen):
        super(AddFriendFrame, self).__init__(screen, height=10, width=40, title="Add Friend")
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        
        self._username = Text("Username:", "username")
        self._message = Label("")
        
        layout.add_widget(self._username)
        layout.add_widget(self._message)
        layout.add_widget(Divider())
        
        layout2 = Layout([1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Send Req", self._send), 0)
        layout2.add_widget(Button("Cancel", self._cancel), 1)
        self.fix()

    def _send(self):
        self.save()
        target = self.data['username']
        curr = session.get_user()
        
        if database.send_friend_request(curr, target):
            self._message.text = "Request sent!"
        else:
            self._message.text = "Failed (User not found/Already friends)"

    def _cancel(self):
        raise NextScene("Friends")

def get_scenes(screen):
    return [
        Scene([FriendsListFrame(screen)], -1, name="Friends"),
        Scene([AddFriendFrame(screen)], -1, name="AddFriend")
    ]
