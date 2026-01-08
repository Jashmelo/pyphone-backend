from asciimatics.widgets import Frame, Layout, Label, Button, Text, RadioButtons, Divider
from asciimatics.scene import Scene
from asciimatics.exceptions import NextScene

class ConverterFrame(Frame):
    def __init__(self, screen):
        super(ConverterFrame, self).__init__(screen, height=20, width=50, title="Converters")
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        
        self._input = Text("Input:", "input")
        self._mode = RadioButtons([
            ("Binary -> Decimal", 1),
            ("Decimal -> Binary", 2),
            ("Hex -> Decimal", 3),
            ("Decimal -> Hex", 4),
            ("Binary -> Hex", 5),
            ("Hex -> Binary", 6)
        ], label="Mode:", name="mode")
        
        self._result = Label("Result: ")
        
        layout.add_widget(self._input)
        layout.add_widget(self._mode)
        layout.add_widget(Divider())
        layout.add_widget(self._result)
        
        layout2 = Layout([1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Convert", self._convert), 0)
        layout2.add_widget(Button("Back", self._back), 1)
        self.fix()

    def _convert(self):
        self.save()
        val = self.data['input']
        mode = self.data['mode']
        res = "Error"
        
        try:
            if mode == 1: # Bin -> Dec
                res = str(int(val, 2))
            elif mode == 2: # Dec -> Bin
                res = bin(int(val))[2:]
            elif mode == 3: # Hex -> Dec
                res = str(int(val, 16))
            elif mode == 4: # Dec -> Hex
                res = hex(int(val))[2:].upper()
            elif mode == 5: # Bin -> Hex
                res = hex(int(val, 2))[2:].upper()
            elif mode == 6: # Hex -> Bin
                res = bin(int(val, 16))[2:]
        except:
             res = "Invalid Input"
             
        self._result.text = f"Result: {res}"

    def _back(self): raise NextScene("Utilities")

def get_scene(screen):
    return Scene([ConverterFrame(screen)], -1, name="Converters")
