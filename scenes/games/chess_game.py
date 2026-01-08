from asciimatics.widgets import Frame, Layout, Label, Widget
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.event import KeyboardEvent
from asciimatics.exceptions import NextScene
import random

# Simple Chess Logic
EMPTY = '.'
WHITE = 'white'
BLACK = 'black'

class ChessEngine:
    def __init__(self):
        self.board = self._init_board()
        self.turn = WHITE
        self.selected = None
        self.msg = "White's Turn"
        self.game_over = False

    def _init_board(self):
        # r n b q k b n r
        # p p p p p p p p
        # . . . . . . . .
        board = [[EMPTY]*8 for _ in range(8)]
        # Black
        board[0] = ['r','n','b','q','k','b','n','r']
        board[1] = ['p']*8
        # White
        board[6] = ['P']*8
        board[7] = ['R','N','B','Q','K','B','N','R']
        return board

    def _get_color(self, piece):
        if piece == EMPTY: return None
        return WHITE if piece.isupper() else BLACK

    def move(self, sx, sy, dx, dy):
        # Very Valid Move Logic is omitted for brevity, essentially assuming user knows rules or basic collision check
        # Implementing full chess rules is huge. I'll implement basic connectivity.
        piece = self.board[sy][sx]
        target = self.board[dy][dx]
        
        # Capture self check
        if self._get_color(target) == self.turn:
            return False

        # Apply Move
        self.board[dy][dx] = piece
        self.board[sy][sx] = EMPTY
        
        # Switch Turn
        self.turn = BLACK if self.turn == WHITE else WHITE
        self.msg = f"{self.turn.capitalize()}'s Turn"
        return True

    def ai_move(self):
        # Random valid move for Black
        # Find all black pieces
        pieces = []
        for y in range(8):
            for x in range(8):
                if self._get_color(self.board[y][x]) == BLACK:
                    pieces.append((x, y))
        
        # Try to find a valid move (randomly)
        random.shuffle(pieces)
        for sx, sy in pieces:
            # Try random target
            for _ in range(10): # retry count
                dx, dy = random.randint(0,7), random.randint(0,7)
                if self.move(sx, sy, dx, dy):
                    return
        self.msg = "AI Pass"

class ChessBoardWidget(Widget):
    def __init__(self, engine):
        super(ChessBoardWidget, self).__init__("ChessBoard")
        self._engine = engine
        self._cursor = [4, 6] # Start at e2
        self._h = 10 # 8 lines + border
        self._w = 20 # 8 * 2 chars + border

    def update(self, frame_no):
        self._draw_label()

    def reset(self):
        pass

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            key = event.key_code
            if key == Screen.KEY_UP:
                self._cursor[1] = max(0, self._cursor[1] - 1)
            elif key == Screen.KEY_DOWN:
                self._cursor[1] = min(7, self._cursor[1] + 1)
            elif key == Screen.KEY_LEFT:
                self._cursor[0] = max(0, self._cursor[0] - 1)
            elif key == Screen.KEY_RIGHT:
                self._cursor[0] = min(7, self._cursor[0] + 1)
            elif key == 10 or key == 13: # Enter
                self._handle_select()
            else:
                return event # Pass through
            return None # Consumed
        return event

    def _handle_select(self):
        x, y = self._cursor
        piece = self._engine.board[y][x]
        
        if self._engine.selected:
            # Move attempt
            sx, sy = self._engine.selected
            if self._engine.move(sx, sy, x, y):
                self._engine.selected = None
                # Trigger AI
                if not self._engine.game_over:
                    self._engine.ai_move()
            else:
                self._engine.selected = None # Deselect on invalid
        else:
            # Select
            if self._engine._get_color(piece) == self._engine.turn:
                self._engine.selected = (x, y)

    def _draw_label(self):
        # Draw board relative to self._x, self._y
        # 8 rows
        for y in range(8):
            row_str = ""
            for x in range(8):
                bg = Screen.COLOUR_BLACK if (x+y)%2==0 else Screen.COLOUR_BLUE
                fg = Screen.COLOUR_WHITE
                
                piece = self._engine.board[y][x]
                if self._engine._get_color(piece) == BLACK:
                    fg = Screen.COLOUR_RED
                
                # Check Cursor/Selection
                attr = Screen.A_NORMAL
                if (x,y) == tuple(self._cursor):
                    attr = Screen.A_REVERSE
                elif self._engine.selected == (x,y):
                    bg = Screen.COLOUR_GREEN
                
                # Draw 2 chars per cell
                char = piece if piece != '.' else ' '
                self._frame.canvas.print_at(
                    f" {char}", 
                    self._x + x*2, 
                    self._y + y, 
                    colour=fg, 
                    attr=attr, 
                    bg=bg
                )

    def required_height(self, offset, width):
        return 8

    @property
    def value(self):
        return self._engine.board

    @value.setter
    def value(self, val):
        pass

class ChessFrame(Frame):
    def __init__(self, screen):
        super(ChessFrame, self).__init__(screen, height=15, width=40, title="Chess")
        self.engine = ChessEngine()
        
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        
        layout.add_widget(Label(lambda: self.engine.msg))
        layout.add_widget(ChessBoardWidget(self.engine))
        layout.add_widget(Label("Arrows to move, Enter to select."))
        
        self.fix()

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
             if event.key_code == ord('q') or event.key_code == ord('Q'):
                 raise NextScene("Games")
                 
        return super(ChessFrame, self).process_event(event)

def get_scene(screen):
    return Scene([ChessFrame(screen)], -1, name="Chess")
