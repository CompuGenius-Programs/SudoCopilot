import random
import tkinter as tk


def empty_board():
    # create an empty board
    board = []
    for i in range(9):
        board.append([])
        for j in range(9):
            board[i].append(0)
    return board


def generate_sudoku_board():
    try:
        board = empty_board()

        # generate valid numbers for each spot
        for i in range(9):
            for j in range(9):
                spot = generate_sudoku_number(i, j, board)
                if spot == 0:
                    return generate_sudoku_board()
                board[i][j] = spot

        global original_board
        original_board = board

        # change some spots to 0 to ensure only one correct solution
        for i in range(9):
            for j in range(9):
                if random.randint(0, 9) == 0:
                    board[i][j] = 0
        return board
    except RecursionError:
        return generate_sudoku_board()


def generate_sudoku_number(row, col, board):
    # generate a valid sudoku number for this spot
    # check if the spot is already filled
    try:
        if board[row][col] != 0:
            return board[row][col]
        # generate a valid number
        valid_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        # remove numbers that are already in the row
        for i in range(9):
            if board[row][i] in valid_numbers:
                valid_numbers.remove(board[row][i])
        # remove numbers that are already in the column
        for i in range(9):
            if board[i][col] in valid_numbers:
                valid_numbers.remove(board[i][col])
        # remove numbers that are already in the 3x3 box
        for i in range(3):
            for j in range(3):
                if board[row - row % 3 + i][col - col % 3 + j] in valid_numbers:
                    valid_numbers.remove(board[row - row % 3 + i][col - col % 3 + j])
        # if there are no valid numbers, return 0
        if len(valid_numbers) == 0:
            return 0
        # return a valid number considering all other spots
        return random.choice(valid_numbers)
    except RecursionError:
        return 0


def display_board(board):
    # display the board in the GUI
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                entry_fields[i][j].delete(0, tk.END)
            else:
                entry_fields[i][j].delete(0, tk.END)
                entry_fields[i][j].insert(0, board[i][j])


def is_solved(board):
    # check if the board is solved
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return False
    return True


def is_valid_number(num, row, col, board):
    # check if the number is valid for this spot
    # check if the number is already in the row
    for i in range(9):
        if board[row][i] == num:
            return False
    # check if the number is already in the column
    for i in range(9):
        if board[i][col] == num:
            return False
    # check if the number is already in the 3x3 box
    for i in range(3):
        for j in range(3):
            if board[row - row % 3 + i][col - col % 3 + j] == num:
                return False
    return True


def solve_sudoku(board):
    # solve the sudoku board
    # check if the board is already solved
    if is_solved(board):
        global solved_board
        solved_board = board
        display_board(board)
        return
    row = 0
    col = 0
    # find the first empty spot
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                row = i
                col = j
                break
        else:
            continue
        break
    # try all valid numbers for this spot
    for num in range(1, 10):
        if is_valid_number(num, row, col, board):
            board[row][col] = num
            solve_sudoku(board)
            board[row][col] = 0
    else:
        return


def generate_board_gui():
    button = tk.Button(root, text="Solve", command=solve_gui_board)
    reset_button = tk.Button(root, text="Reset", command=reset_gui_board)
    button.grid(row=10, column=0, columnspan=4, sticky="nsew")
    reset_button.grid(row=10, column=4, columnspan=4, sticky="nsew")

    entry_fields[0][0].focus_set()

    root.mainloop()


def reset_gui_board():
    # reset the board to the original state
    global entry_fields
    entry_fields = create_entry_fields()
    display_board(empty_board())

    entry_fields[0][0].focus_set()


def create_entry_fields():
    # create entry fields for the board. make the border of each 3 by 3 box a different color
    fields = []
    for i in range(9):
        fields.append([])
        for j in range(9):
            if (i < 3 or i > 5) and (j < 3 or j > 5) or (2 < i < 6) and (2 < j < 6):
                entry = tk.Entry(root, width=2, font="Arial 20 bold", fg="black", bg="white", justify="center")
            else:
                entry = tk.Entry(root, width=2, font="Arial 20 bold", fg="black", bg="#CCCCCC", justify="center")
            entry.bind('<Key>', lambda event, row=i, col=j: handle_key(event, row, col))
            entry.grid(row=i, column=j)
            fields[i].append(entry)
    return fields


def handle_key(event, row, col):
    entry = entry_fields[row][col]
    entry.delete(0, tk.END)
    if event.keysym.isdigit() or event.keysym == 'Tab':
        if event.keysym == '0':
            root.after(0, entry.delete, 0, tk.END)
        next_col = (col + 1) % 9
        next_row = row + 1 if next_col == 0 else row
        if next_row != 9:
            entry_fields[next_row][next_col].focus()
        else:
            root.after(0, solve_gui_board)

    elif event.keysym == 'BackSpace':
        prev_col = (col - 1) % 9
        prev_row = row - 1 if prev_col == 8 else row
        entry = entry_fields[prev_row][prev_col]
        entry.delete(0, tk.END)
        entry.focus()


def solve_gui_board():
    board = empty_board()

    for i in range(9):
        for j in range(9):
            num = entry_fields[i][j].get()
            if num == '':
                num = 0
            board[i][j] = int(num)

    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                entry_fields[i][j].config(fg="gray")

    solve_sudoku(board)


def main():
    generate_board = False
    if generate_board:
        board = generate_sudoku_board()
        display_board(board)

    generate_board_gui()


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Sudoku Solver")

    entry_fields = create_entry_fields()

    original_board = empty_board()
    solved_board = empty_board()

    main()
