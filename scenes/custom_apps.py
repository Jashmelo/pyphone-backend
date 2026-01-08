from asciimatics.widgets import Frame, Layout, ListBox, Button, Divider, TextBox, Text, Label
from asciimatics.scene import Scene
from asciimatics.exceptions import NextScene
import database
import session
import sys
import io

class AppListFrame(Frame):
    def __init__(self, screen):
        super(AppListFrame, self).__init__(screen, height=15, width=50, title="My Apps", on_load=self._on_load)
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        
        self._list_box = ListBox(6, [], name="apps", on_select=self._edit)
        layout.add_widget(self._list_box)
        layout.add_widget(Divider())
        
        layout.add_widget(Button("Run", self._run))
        layout.add_widget(Button("New App", self._new))
        layout.add_widget(Button("Back", self._back))
        self.fix()

    def _on_load(self):
        self.user_apps = database.get_custom_apps(session.get_user())
        options = [(a['name'], i) for i, a in enumerate(self.user_apps)]
        self._list_box.options = options

    def _edit(self):
        if self._list_box.value is None: return
        # Store index to edit
        session.temp_app_idx = self._list_box.value
        raise NextScene("EditApp")

    def _run(self):
        if self._list_box.value is None: return
        app = self.user_apps[self._list_box.value]
        # Execute Code
        # We need to capture output to show it.
        # But Screen is active...
        # We can StopApplication, run, wait input, restart?
        # Or just show Popup with output.
        
        output = io.StringIO()
        sys.stdout = output
        try:
            exec(app['code'], {"__builtins__": __builtins__})
        except Exception as e:
            print(f"Error: {e}")
        finally:
            sys.stdout = sys.__stdout__ # Restore
            
        # Store last output to show in Result view?
        session.last_app_output = output.getvalue()
        raise NextScene("AppResult")

    def _new(self):
        session.temp_app_idx = None
        raise NextScene("EditApp")

    def _back(self): raise NextScene("MainMenu")

class EditAppFrame(Frame):
    def __init__(self, screen):
        super(EditAppFrame, self).__init__(screen, height=20, width=60, title="Editor", on_load=self._on_load)
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        
        self._name = Text("Name:", "name")
        self._code = TextBox(10, label="Code:", name="code", as_string=True)
        
        layout.add_widget(self._name)
        layout.add_widget(self._code)
        
        layout2 = Layout([1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Save", self._save), 0)
        layout2.add_widget(Button("Cancel", self._cancel), 1)
        self.fix()

    def _on_load(self):
        idx = getattr(session, 'temp_app_idx', None)
        self.data = {"name": "", "code": "print('Hello')"}
        if idx is not None:
             user_apps = database.get_custom_apps(session.get_user())
             if idx < len(user_apps):
                 self.data = user_apps[idx]
        self.save() # Reset UI
        self._name.value = self.data['name']
        self._code.value = self.data['code']

    def _save(self):
        self.save()
        database.save_custom_app(session.get_user(), self.data['name'], self.data['code'])
        raise NextScene("CustomApps")

    def _cancel(self): raise NextScene("CustomApps")

class ResultFrame(Frame):
    def __init__(self, screen):
        super(ResultFrame, self).__init__(screen, height=15, width=60, title="Output", on_load=self._on_load)
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        
        self._out = TextBox(10, as_string=True)
        self._out.disabled = True
        layout.add_widget(self._out)
        
        layout.add_widget(Button("Back", self._back))
        self.fix()

    def _on_load(self):
        self._out.value = getattr(session, 'last_app_output', "")

    def _back(self): raise NextScene("CustomApps")

def get_scenes(screen):
    return [
        Scene([AppListFrame(screen)], -1, name="CustomApps"),
        Scene([EditAppFrame(screen)], -1, name="EditApp"),
        Scene([ResultFrame(screen)], -1, name="AppResult")
    ]
