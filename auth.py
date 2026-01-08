from asciimatics.widgets import Frame, Layout, Label, Button, Text, Divider
from asciimatics.scene import Scene
from asciimatics.exceptions import NextScene, StopApplication
import database
import session
import ui_common

class LoginFrame(Frame):
    def __init__(self, screen):
        super(LoginFrame, self).__init__(screen,
                                       height=15,
                                       width=40,
                                       name="Login",
                                       hover_focus=True,
                                       can_scroll=False,
                                       title="PyPhone OS Login")
        self.set_theme("monochrome")
        
        # Layouts
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        
        self._username = Text("Username:", "username")
        self._password = Text("Password:", "password", hide_char="*")
        self._message = Label("")
        
        layout.add_widget(Label("Welcome to PyPhone"))
        layout.add_widget(Divider())
        layout.add_widget(self._username)
        layout.add_widget(self._password)
        layout.add_widget(Divider())
        layout.add_widget(self._message)
        
        layout2 = Layout([1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Login", self._login), 0)
        layout2.add_widget(Button("Register", self._register), 1)
        layout2.add_widget(Button("Quit", self._quit), 0)
        
        self.fix()

    def _login(self):
        self.save()
        username = self.data['username']
        password = self.data['password']
        
        if database.verify_login(username, password):
            session.set_user(username)
            raise NextScene("MainMenu")
        else:
            self._message.text = "Invalid credentials!"

    def _register(self):
        raise NextScene("Register")

    def _quit(self):
        raise StopApplication("UserQuit")

class RegisterFrame(Frame):
    def __init__(self, screen):
        super(RegisterFrame, self).__init__(screen,
                                          height=18,
                                          width=40,
                                          name="Register",
                                          hover_focus=True,
                                          title="New Account")
        self.set_theme("monochrome")
        
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        
        self._username = Text("Username:", "username")
        self._password = Text("Password:", "password", hide_char="*")
        self._confirm = Text("Confirm:", "confirm", hide_char="*")
        self._message = Label("")
        
        layout.add_widget(Label("Create PyPhone Account"))
        layout.add_widget(Divider())
        layout.add_widget(self._username)
        layout.add_widget(self._password)
        layout.add_widget(self._confirm)
        layout.add_widget(Divider())
        layout.add_widget(self._message)
        
        layout2 = Layout([1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Create", self._create), 0)
        layout2.add_widget(Button("Back", self._back), 1)
        
        self.fix()

    def _create(self):
        self.save()
        username = self.data['username']
        password = self.data['password']
        confirm = self.data['confirm']
        
        if password != confirm:
            self._message.text = "Passwords do not match!"
            return

        if len(password) < 1:
            self._message.text = "Password too short!"
            return
            
        if database.create_user(username, password):
            self._message.text = "Account created!"
            # Optionally auto-login or ask to login
            # For now, stay here or go back? Let's go back to login
            # raise NextScene("Login") # User might want to see the success message
        else:
            self._message.text = "User already exists!"

    def _back(self):
        raise NextScene("Login")

def get_scenes(screen):
    return [
        Scene([LoginFrame(screen)], -1, name="Login"),
        Scene([RegisterFrame(screen)], -1, name="Register")
    ]
