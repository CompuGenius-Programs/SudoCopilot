import random


def generate_board_from_spot_inputs():
    board = []
    for i in range(9):
        board.append([])
        for j in range(9):
            board[i].append(0)

    for i in range(9):
        for j in range(9):
            board[i][j] = int(input("Enter a number for spot " + str(i + 1) + "," + str(j + 1) + ": "))

    return board


def generate_sudoku_board():
    board = []
    for i in range(9):
        board.append([])
        for j in range(9):
            board[i].append(0)

    # generate valid numbers for each spot
    for i in range(9):
        for j in range(9):
            board[i][j] = generate_sudoku_number(i, j, board)

    # remove some numbers to make the board harder
    for i in range(9):
        for j in range(9):
            if random.randint(0, 1) == 0:
                board[i][j] = 0
    return board


def generate_sudoku_number(row, col, board):
    # generate a valid sudoku number for this spot
    # check if the spot is already filled
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


def print_board(board):
    # print a sudoku board nicely formatted in ascii
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -")
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")


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
        print_board(board)
        return
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


def main():
    # board = generate_sudoku_board()
    # board = generate_board_from_spot_inputs()
    board = [[0, 0, 6, 0, 9, 0, 2, 0, 0],
             [0, 0, 0, 7, 0, 2, 0, 0, 0],
             [0, 9, 0, 5, 0, 8, 0, 7, 0],
             [9, 0, 0, 0, 3, 0, 0, 0, 6],
             [7, 5, 0, 0, 0, 0, 0, 1, 9],
             [1, 0, 0, 0, 4, 0, 0, 0, 5],
             [0, 1, 0, 3, 0, 9, 0, 8, 0],
             [0, 0, 0, 2, 0, 1, 0, 0, 0],
             [0, 0, 9, 0, 8, 0, 1, 0, 0]]
    print_board(board)

    print()
    print("Solving...")
    solve_sudoku(board)


if __name__ == '__main__':
    main()
