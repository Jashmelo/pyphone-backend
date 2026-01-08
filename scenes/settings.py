from asciimatics.widgets import Frame, Layout, Label, Button, Divider, Text, CheckBox
from asciimatics.scene import Scene
from asciimatics.exceptions import NextScene
import session
import database

class SettingsFrame(Frame):
    def __init__(self, screen):
        super(SettingsFrame, self).__init__(screen, height=10, width=40, title="Settings", on_load=self._on_load)
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        
        self._clock_fmt = CheckBox("Use 24-hour Clock", name="clock_24h")
        layout.add_widget(self._clock_fmt)
        layout.add_widget(Divider())
        
        layout2 = Layout([1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Save", self._save), 0)
        layout2.add_widget(Button("Back", self._back), 1)
        self.fix()

    def _on_load(self):
        user = database.get_user(session.get_user())
        settings = user.get('settings', {})
        self.data = {'clock_24h': settings.get('clock_24h', True)}
        self.save()

    def _save(self):
        self.save()
        user_data = database.get_user(session.get_user())
        if 'settings' not in user_data: user_data['settings'] = {}
        user_data['settings']['clock_24h'] = self.data['clock_24h']
        database._save_json(database.USERS_FILE, {**database._load_json(database.USERS_FILE), session.get_user(): user_data})
        # Note: Ideally database has update_user method.
        # Quick hack: existing database.py create_user handles overwrite? No. 
        # I should have added update_settings in database.py.
        # Re-implementing save here properly:
        all_users = database._load_json(database.USERS_FILE)
        all_users[session.get_user()] = user_data
        database._save_json(database.USERS_FILE, all_users)
        
        raise NextScene("MainMenu")

    def _back(self): raise NextScene("MainMenu")

def get_scene(screen):
    return Scene([SettingsFrame(screen)], -1, name="Settings")
