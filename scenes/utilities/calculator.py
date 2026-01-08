from asciimatics.widgets import Frame, Layout, Button, Text, Label
from asciimatics.scene import Scene
from asciimatics.exceptions import NextScene
import math

class CalculatorFrame(Frame):
    def __init__(self, screen):
        super(CalculatorFrame, self).__init__(screen, height=20, width=40, title="Scientific Calculator")
        
        layout = Layout([100])
        self.add_layout(layout)
        
        self._display = Text("", "display")
        self._display.disabled = True
        layout.add_widget(self._display)
        
        # Buttons Grid
        # 7 8 9 /
        # 4 5 6 *
        # 1 2 3 -
        # 0 . = +
        # C ^ T (Tetration)
        
        grid = Layout([1, 1, 1, 1])
        self.add_layout(grid)
        
        def add_char(c):
            return lambda: self._add(c)
            
        chars = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]
        
        for i, char in enumerate(chars):
            col = i % 4
            if char == '=':
                grid.add_widget(Button(char, self._eval), col)
            else:
                grid.add_widget(Button(char, add_char(char)), col)
                
        grid.add_widget(Button("C", self._clear), 0)
        grid.add_widget(Button("pow", add_char("**")), 1)
        grid.add_widget(Button("tetr", self._tetration), 2)
        grid.add_widget(Button("Back", self._back), 3)

        self.fix()
        self.current_val = ""

    def _add(self, char):
        self.current_val += char
        self._display.value = self.current_val

    def _clear(self):
        self.current_val = ""
        self._display.value = ""

    def _eval(self):
        try:
            # Safe-ish eval
            res = str(eval(self.current_val, {"__builtins__": None, "math": math}))
            self.current_val = res
            self._display.value = res
        except Exception as e:
            self._display.value = "Error"
            self.current_val = ""

    def _tetration(self):
        # x ^^ y. 
        # Parse last number?
        # Format: base, height.
        # User enters "2,3" -> 2^^3 = 16
        try:
            parts = self.current_val.split(',')
            if len(parts) == 2:
                base = float(parts[0])
                height = int(float(parts[1]))
                # Tetration: base^(base^(...)) height times
                res = base
                for _ in range(height - 1):
                    res = base ** res
                self.current_val = str(res)
                self._display.value = self.current_val
            else:
                self._display.value = "Use 'base,height' for tetr"
        except:
             self._display.value = "Error"

    def _back(self):
        raise NextScene("Utilities")

def get_scene(screen):
    return Scene([CalculatorFrame(screen)], -1, name="Calculator")
