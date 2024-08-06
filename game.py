import tkinter as tk
from tkinter import messagebox

def check_winner(board, player):
    win_conditions = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[2][0], board[1][1], board[0][2]]
    ]
    for condition in win_conditions:
        if condition == [player, player, player]:
            return True, win_conditions.index(condition)
    return False, None

def is_full(board):
    for row in board:
        if " " in row:
            return False
    return True

def on_click(row, col):
    global current_player, current_player_name
    if board[row][col] == " ":
        board[row][col] = current_player
        buttons[row][col].config(text=current_player, state="disabled")
        won, win_index = check_winner(board, current_player)
        if won:
            highlight_winner(win_index)
            update_score(current_player)
            winner_name = player_x_name if current_player == "X" else player_o_name
            if messagebox.askyesno("Tic Tac Toe", f"{winner_name} wins! Do you want to play again?"):
                reset_game(False)
            else:
                root.quit()
        elif is_full(board):
            if messagebox.askyesno("Tic Tac Toe", "The game is a draw! Do you want to play again?"):
                reset_game(False)
            else:
                root.quit()
        else:
            current_player = "O" if current_player == "X" else "X"
            current_player_name = player_o_name if current_player == "O" else player_x_name
            update_current_player_label()
    else:
        messagebox.showwarning("Tic Tac Toe", "Invalid move, try again.")

def update_score(winner):
    global x_score, o_score
    if winner == "X":
        x_score += 1
        x_score_label.config(text=f"{player_x_name}: {x_score}")
    else:
        o_score += 1
        o_score_label.config(text=f"{player_o_name}: {o_score}")

def reset_game(clear_scores=True):
    global board, current_player, x_score, o_score, current_player_name
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"
    current_player_name = player_x_name
    for row in range(3):
        for col in range(3):
            buttons[row][col].config(text=" ", state="normal", bg='lightblue')
    if clear_scores:
        x_score, o_score = 0, 0
        x_score_label.config(text=f"{player_x_name}: {x_score}")
        o_score_label.config(text=f"{player_o_name}: {o_score}")
    update_current_player_label()

def highlight_winner(win_index):
    win_conditions = [
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 1), (2, 2)],
        [(2, 0), (1, 1), (0, 2)]
    ]
    for row, col in win_conditions[win_index]:
        buttons[row][col].config(bg='lightgreen')

def update_current_player_label():
    current_player_label.config(text=f"Current Player: {current_player_name}")

def start_game():
    global player_x_name, player_o_name, current_player_name
    player_x_name = player_x_entry.get()
    player_o_name = player_o_entry.get()
    if not player_x_name or not player_o_name:
        messagebox.showwarning("Tic Tac Toe", "Please enter names for both players.")
        return
    current_player_name = player_x_name
    player_name_frame.pack_forget()
    game_frame.pack()
    update_current_player_label()

root = tk.Tk()
root.title("Tic Tac Toe")

player_name_frame = tk.Frame(root)
player_name_frame.pack()

tk.Label(player_name_frame, text="Player X Name:").grid(row=0, column=0)
player_x_entry = tk.Entry(player_name_frame)
player_x_entry.grid(row=0, column=1)

tk.Label(player_name_frame, text="Player O Name:").grid(row=1, column=0)
player_o_entry = tk.Entry(player_name_frame)
player_o_entry.grid(row=1, column=1)

start_button = tk.Button(player_name_frame, text="Start Game", command=start_game)
start_button.grid(row=2, column=0, columnspan=2)

game_frame = tk.Frame(root)

board = [[" " for _ in range(3)] for _ in range(3)]
current_player = "X"
buttons = [[None for _ in range(3)] for _ in range(3)]

x_score = 0
o_score = 0

for row in range(3):
    for col in range(3):
        buttons[row][col] = tk.Button(game_frame, text=" ", font='normal 20 bold', bg='lightblue', width=5, height=2,
                                      command=lambda r=row, c=col: on_click(r, c))
        buttons[row][col].grid(row=row, column=col)

reset_button = tk.Button(game_frame, text="Reset", font='normal 15 bold', command=reset_game)
reset_button.grid(row=3, column=0, columnspan=3)

x_score_label = tk.Label(game_frame, text=f"Player X: {x_score}", font='normal 15 bold')
x_score_label.grid(row=4, column=0, columnspan=1)
o_score_label = tk.Label(game_frame, text=f"Player O: {o_score}", font='normal 15 bold')
o_score_label.grid(row=4, column=2, columnspan=1)

current_player_label = tk.Label(game_frame, text=f"Current Player: ", font='normal 15 bold')
current_player_label.grid(row=5, column=0, columnspan=3)

root.mainloop()
