from asciimatics.widgets import Frame, Layout, Button, Label, Divider
from asciimatics.scene import Scene
from asciimatics.exceptions import NextScene
import random

ROCK_ART = """
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
"""

PAPER_ART = """
     _______
---'    ____)____
           ______)
          _______)
         _______)
---.__________)
"""

SCISSORS_ART = """
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
"""

ARTS = {"R": ROCK_ART, "P": PAPER_ART, "S": SCISSORS_ART}
NAMES = {"R": "Rock", "P": "Paper", "S": "Scissors"}

class RPSFrame(Frame):
    def __init__(self, screen):
        super(RPSFrame, self).__init__(screen, height=20, width=50, title="Rock Paper Scissors")
        
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        
        self._player_lbl = Label("Choose your move:")
        self._bot_lbl = Label("")
        self._result_lbl = Label("")
        self._art_lbl = Label("", height=8)
        
        layout.add_widget(self._player_lbl)
        layout.add_widget(self._art_lbl)
        
        btn_layout = Layout([1, 1, 1])
        self.add_layout(btn_layout)
        btn_layout.add_widget(Button("Rock", lambda: self._play("R")), 0)
        btn_layout.add_widget(Button("Paper", lambda: self._play("P")), 1)
        btn_layout.add_widget(Button("Scissors", lambda: self._play("S")), 2)
        
        footer = Layout([100])
        self.add_layout(footer)
        footer.add_widget(Divider())
        footer.add_widget(self._result_lbl)
        footer.add_widget(self._bot_lbl)
        footer.add_widget(Divider())
        footer.add_widget(Button("Back", self._back))
        
        self.fix()

    def _play(self, move):
        bot = random.choice(["R", "P", "S"])
        
        # Show Art
        art = f"You:\n{ARTS[move]}\nBot:\n{ARTS[bot]}" 
        # ASCII art might need side-by-side logic, simplified to vertical for now
        self._art_lbl.text = art.replace("\n", " ") # Label doesn't supportnewlines well in simple mode? Asciimatics Label is single line mostly unless height set?
        # Re-using Label for multi-line is tricky.
        # Let's just state text.
        
        res = "Draw"
        if move == bot:
            res = "Draw!"
        elif (move == "R" and bot == "S") or \
             (move == "P" and bot == "R") or \
             (move == "S" and bot == "P"):
            res = "You Win!"
        else:
            res = "You Lose!"
            
        self._player_lbl.text = f"You chose: {NAMES[move]}"
        self._bot_lbl.text = f"Bot chose: {NAMES[bot]}"
        self._result_lbl.text = f"Result: {res}"

    def _back(self):
        raise NextScene("Games")

def get_scene(screen):
    return Scene([RPSFrame(screen)], -1, name="RPS")
