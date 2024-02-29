# libraries

import tkinter as tk
from tkinter import font
from typing import NamedTuple
from itertools import cycle  

class Player(NamedTuple):
    label: str
    color: str

class Move(NamedTuple):
    row: int
    col: int
    label: str = ""

DEFAULT_PLAYERS = (
    Player(label="X", color="blue"),
    Player(label="O", color="green")    
)

class TicTacToeGame:
    def __init__(self, players=DEFAULT_PLAYERS): # give it the players
        self._players = cycle(players) #PLAYERS
        self.current_player = next(self._players) # TELL THE GAME WHO TURN IT IS
        self._current_moves = [] # WHAT MOVES THE PLAYER HAS DONE
        self._has_winner = False # TELL THE GAME IF SOMEONE HAS WON THE GAME
        self._winning_combos = [] # WHICH COMBINATIONS MAKE A WINNER
        self.winner_combo = [] # TELL THE GAME WHAT THE WINNING COMBO IS SO WE CAN SHOW THE WORLD
        self._setup_board()

    # MAKE SURE WE RESET THE MOVES
    def _setup_board(self):
        self._current_moves = [ # set empty moves - make array 
            [Move(col=0,row=0), Move(col=0, row=1), Move(col=0, row=2)],
            [Move(col=1,row=0), Move(col=1, row=1), Move(col=1, row=2)],
            [Move(col=2,row=0), Move(col=2, row=1), Move(col=2, row=2)]
            # [Move(row, col) 
            # for col in range(3)]
            # for row in range(3)
        ]
        # print(self._current_moves)
        self._winning_combos = self._get_winning_combos()

    # TELL THE GAME HOW SOMEONE CAN WIN
    def _get_winning_combos(self):
        rows = [
            # [Move(row=0,col=0), Move(row=0,col=1), Move(row=0,col=1)],
            [(0, 0), (0, 1), (0, 2)],
            [(0, 1), (1, 1), (2, 1)], 
            [(0, 2), (2, 1), (2, 2)]
            # [(move.row, move.col) for move in row]
            # for row in self._current_moves
        ]
        # print(rows)
        winning_columns = [
            [(0, 0), (1, 0), (2, 0)],
            [(1, 0), (1, 1), (1, 2)], 
            [(2, 0), (2, 1), (2, 2)]
            
            # [(move.row, move.col) for move in col]
            # for col in self._current_moves
        ]
        # columns = [list(col) for col in zip(*rows)]
        first_diagonal = [(1,1), (2,2), (0,0)]
        # first_diagonal = [row[i] for i, row in enumerate(rows)]
        # second_diagonal = [col[j] for j, col in enumerate(reversed(winning_columns))]
        second_diagonal = [(0,2), (1,1), (2,0)]
        return rows + winning_columns + [first_diagonal, second_diagonal]

        # winning_rows = [
        #     [(move.row, move.col) for move in row]
        #     for row in self._current_moves
        # ]
        # winning_columns = [
        #     [(move.row, move.col) for move in col]
        #     for col in self._current_moves
        # ]
        # first_diagonal = [Move(0,0),Move(1,1), Move(2,2)]
        # second_diagonal = [Move(2,0),Move(1,1), Move(0,2)]
        # return winning_rows + winning_columns + [first_diagonal + second_diagonal]
        
    # MAKE SURE PLAYERS CAN'T SELECT THE SAME SQUARE AND NO ONE HAS WON YET
    def is_valid_move(self, move):
        free_square = self._current_moves[move.col][move.row].label == ""
        no_winner = not self._has_winner
        return no_winner and free_square
    
    def check_if_someone_won(self, move):
        row, col = move.row, move.col
        self._current_moves[col][row] = move
        for combo in self._winning_combos:
            results = set(
                self._current_moves[n][m].label
                for n, m in combo
            )
            is_win = (len(results) == 1) and ("" not in results)
            if is_win:
                self._has_winner = True
                self.winner_combo = combo
                break

    def check_if_game_tied(self):
        no_winner = not self._has_winner
        played_moves = (
            move.label 
            for row in self._current_moves 
            for move in row
        )
        return no_winner and all(played_moves)
    
    # SWITCH PLAYERS
    def toggle_player(self):
        self.current_player = next(self._players)

# START HERE = the game board
class TicTacToeBoard(tk.Tk):
    def __init__(self, game): # ADD game to the board
        super().__init__()
        self.title("Tic-Tac-Toe Game")
        self._cells = {}
        self._game = game # ADD this line 
        self._create_board_display()
        self._create_board_grid()

    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label( # make the text display the title
            master=display_frame,
            text="Ready to play Tic Tac Toe?",
            font=font.Font(size=20, weight="bold"),
        )
        self.display.pack()

    # creates the board grid 
    def _create_board_grid(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        for row in range(3): 
            self.rowconfigure(row, weight=1, minsize=50) 
            self.columnconfigure(row, weight=1, minsize=75) 
            for col in range(3): 
                button = tk.Button(
                    master=grid_frame,
                    text="",
                    font=font.Font(size=36, weight="bold"),
                    fg="green",
                    width=3,
                    height=2,
                    highlightbackground="lightblue",
                )
                self._cells[button] = (row, col)
                button.bind("<ButtonPress-1>", self.play)
                button.grid(
                    row=row,
                    column=col,
                    padx=5,
                    pady=5,
                    sticky="nsew"
                )

    # TELL THE GAME WHAT TO DO ONCE A PLAYER CLICKS ON A SQUARE AND MAKES A MOVE
    def play(self, event):
        clicked_btn = event.widget #how we tell the game which button was clicked
        row, col = self._cells[clicked_btn]
        new_move = Move(col, row, self._game.current_player.label)
        if self._game.is_valid_move(new_move):
            self._update_button(clicked_btn)
            self._game.check_if_someone_won(new_move)
            if self._game.check_if_game_tied():
                self._update_display(msg="Tied game!", color="red")
            elif self._game._has_winner:
                self._highlight_cells()
                msg = f'Player "{self._game.current_player.label}" won!'
                color = self._game.current_player.color
                self._update_display(msg, color)
            else:
                self._game.toggle_player()
                msg = f"{self._game.current_player.label}'s turn"
                self._update_display(msg)

    def _update_button(self, clicked_btn):
        clicked_btn.config(text=self._game.current_player.label)
        clicked_btn.config(fg=self._game.current_player.color)

    def _update_display(self, msg, color="black"):
        self.display["text"] = msg
        self.display["fg"] = color

    def _highlight_cells(self):
        for button, coordinates in self._cells.items():
            if coordinates in self._game.winner_combo:
                button.config(highlightbackground="red")

                
def main(): # method that runs everything
    game = TicTacToeGame()
    board = TicTacToeBoard(game) # give it the game logic!
    board.mainloop()
    
if __name__ == "__main__":
   main()