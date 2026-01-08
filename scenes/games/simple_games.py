from asciimatics.widgets import Frame, Layout, Label, Button, Text, Divider
from asciimatics.scene import Scene
from asciimatics.exceptions import NextScene
import random

# --- Hangman ---
HANGMAN_PICS = ['''
  +---+
  |   |
      |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\\  |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\\  |
 /    |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\\  |
 / \\  |
      |
=========''']

WORDS = ["PYTHON", "RUBY", "JAVA", "SWIFT", "KOTLIN", "RUST", "GO", "SHELL"]

class HangmanFrame(Frame):
    def __init__(self, screen):
        super(HangmanFrame, self).__init__(screen, height=20, width=40, title="Hangman", on_load=self._reset)
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        
        self._pic = Label(HANGMAN_PICS[0], height=8)
        self._word_lbl = Label("_ _ _ _ _")
        self._guess = Text("Letter:", "guess")
        self._msg = Label("")
        
        layout.add_widget(self._pic)
        layout.add_widget(self._word_lbl)
        layout.add_widget(self._guess)
        layout.add_widget(self._msg)
        
        layout2 = Layout([1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Guess", self._do_guess), 0)
        layout2.add_widget(Button("Back", self._back), 1)
        self.fix()

    def _reset(self):
        self.word = random.choice(WORDS)
        self.guesses = set()
        self.misses = 0
        self.game_over = False
        self._update_ui()

    def _update_ui(self):
        # Update Pic
        if self.misses < len(HANGMAN_PICS):
            self._pic.text = HANGMAN_PICS[self.misses]
        
        # Update Word
        disp = [c if c in self.guesses else '_' for c in self.word]
        self._word_lbl.text = " ".join(disp)
        
        self._guess.value = ""

    def _do_guess(self):
        if self.game_over: return
        self.save()
        g = self.data['guess'].upper()
        if not g or len(g) != 1: return
        
        if g in self.guesses:
            self._msg.text = "Already guessed!"
            return
            
        self.guesses.add(g)
        if g not in self.word:
            self.misses += 1
            self._msg.text = "Miss!"
        else:
            self._msg.text = "Hit!"
            
        if self.misses >= len(HANGMAN_PICS) - 1:
            self._msg.text = f"GAME OVER! Word: {self.word}"
            self.game_over = True
        elif all(c in self.guesses for c in self.word):
            self._msg.text = "YOU WIN!"
            self.game_over = True
            
        self._update_ui()

    def _back(self): raise NextScene("Games")

# --- Math Game ---
class MathGameFrame(Frame):
    def __init__(self, screen):
        super(MathGameFrame, self).__init__(screen, height=15, width=40, title="Quick Math", on_load=self._new_q)
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        
        self._q_lbl = Label("Q: ?")
        self._ans = Text("Answer:", "ans")
        self._res = Label("")
        self._score = 0
        
        layout.add_widget(self._q_lbl)
        layout.add_widget(self._ans)
        layout.add_widget(self._res)
        
        layout.add_widget(Button("Submit", self._check))
        layout.add_widget(Button("Back", self._back))
        self.fix()

    def _new_q(self):
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        op = random.choice(['+', '-', '*'])
        self.ans = eval(f"{a}{op}{b}")
        self._q_lbl.text = f"Q: {a} {op} {b} = ?"
        self.data['ans'] = ""
        self._ans.value = ""

    def _check(self):
        self.save()
        try:
            val = int(self.data['ans'])
            if val == self.ans:
                self._score += 1
                self._res.text = f"Correct! Score: {self._score}"
                self._new_q()
            else:
                self._res.text = f"Wrong! Ans: {self.ans}"
                self._score = 0
                self._new_q()
        except:
            pass

    def _back(self): raise NextScene("Games")

# --- Lucky Number ---
class LuckyNumberFrame(Frame):
    def __init__(self, screen):
        super(LuckyNumberFrame, self).__init__(screen, height=15, width=40, title="Lucky Number", on_load=self._reset)
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        
        self._msg_lbl = Label("I picked a number 1-100")
        self._guess = Text("Guess:", "guess")
        
        layout.add_widget(self._msg_lbl)
        layout.add_widget(self._guess)
        layout.add_widget(Button("Guess", self._check))
        layout.add_widget(Button("Back", self._back))
        self.fix()

    def _reset(self):
        self.target = random.randint(1, 100)
        self._msg_lbl.text = "I picked a number 1-100"
        self._guess.value = ""

    def _check(self):
        self.save()
        try:
            val = int(self.data['guess'])
            if val == self.target:
                self._msg_lbl.text = f"Correct! {val}!"
            elif val < self.target:
                self._msg_lbl.text = "Too Low!"
            else:
                self._msg_lbl.text = "Too High!"
        except:
            pass

    def _back(self): raise NextScene("Games")

def get_scenes(screen):
    return [
        Scene([HangmanFrame(screen)], -1, name="Hangman"),
        Scene([MathGameFrame(screen)], -1, name="MathGame"),
        Scene([LuckyNumberFrame(screen)], -1, name="LuckyNumber")
    ]
