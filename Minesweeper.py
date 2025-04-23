import random

def get_settings():
    print("Choose difficulty:")
    print("[1] Easy (8x8, 10 mines)")
    print("[2] Medium (12x12, 25 mines)")
    print("[3] Hard (16x16, 40 mines)")
    choice = input("Enter 1, 2, or 3: ").strip()
    if choice == '1':
        return 8, 8, 10
    elif choice == '2':
        return 12, 12, 25
    elif choice == '3':
        return 16, 16, 40
    else:
        print("Invalid choice. Defaulting to Easy.")
        return 8, 8, 10

def create_board(rows, cols, num_mines):
    board = [[' ' for _ in range(cols)] for _ in range(rows)]
    revealed = [[False for _ in range(cols)] for _ in range(rows)]

    mines = set()
    while len(mines) < num_mines:
        r = random.randint(0, rows - 1)
        c = random.randint(0, cols - 1)
        mines.add((r, c))

    for r in range(rows):
        for c in range(cols):
            if (r, c) in mines:
                board[r][c] = 'M'
            else:
                count = sum((nr, nc) in mines for nr in range(r - 1, r + 2)
                            for nc in range(c - 1, c + 2)
                            if 0 <= nr < rows and 0 <= nc < cols)
                board[r][c] = str(count) if count > 0 else ' '
    return board, revealed, mines

def print_board(board, revealed):
    cols = len(board[0])
    print("    " + " ".join(f"{i:2}" for i in range(cols)))
    print("   +" + "---"*cols + "+")
    for r, row in enumerate(board):
        row_str = f"{r:2} |" + " ".join(f"{cell:2}" if revealed[r][c] else "##" for c, cell in enumerate(row)) + " |"
        print(row_str)
    print("   +" + "---"*cols + "+")

def reveal(board, revealed, r, c):
    rows, cols = len(board), len(board[0])
    if not (0 <= r < rows and 0 <= c < cols) or revealed[r][c]:
        return
    revealed[r][c] = True
    if board[r][c] == ' ':
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if dr != 0 or dc != 0:
                    reveal(board, revealed, r + dr, c + dc)

def check_win(revealed, mines):
    for r in range(len(revealed)):
        for c in range(len(revealed[0])):
            if not revealed[r][c] and (r, c) not in mines:
                return False
    return True

def play():
    rows, cols, num_mines = get_settings()
    board, revealed, mines = create_board(rows, cols, num_mines)

    while True:
        print_board(board, revealed)
        try:
            raw_input = input("Enter row and column (e.g. '3 4'): ").strip()
            if not raw_input:
                continue
            r, c = map(int, raw_input.split())
            if (r, c) in mines:
                print("BOOM! You hit a mine!")
                for mr, mc in mines:
                    revealed[mr][mc] = True
                print_board(board, revealed)
                print("Game Over.")
                break
            reveal(board, revealed, r, c)
            if check_win(revealed, mines):
                print_board(board, revealed)
                print("Congratulations! You cleared the minefield! 🎉")
                break
        except (ValueError, IndexError):
            print("Invalid input. Please enter row and column numbers separated by a space.")

play()
