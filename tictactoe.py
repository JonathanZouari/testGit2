"""Two-player tic-tac-toe played in the terminal."""
print("pie")
WIN_LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)


def render(board):
    cells = [cell if cell else str(index + 1) for index, cell in enumerate(board)]
    rows = (
        f" {cells[0]} | {cells[1]} | {cells[2]} ",
        f" {cells[3]} | {cells[4]} | {cells[5]} ",
        f" {cells[6]} | {cells[7]} | {cells[8]} ",
    )
    print("\n" + "\n---+---+---\n".join(rows) + "\n")


def winner(board):
    for a, b, c in WIN_LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    return None


def ask_move(board, player):
    while True:
        raw = input(f"Player {player}, choose a square (1-9): ").strip()
        if not raw.isdigit():
            print("Enter a number from 1 to 9.")
            continue
        index = int(raw) - 1
        if index < 0 or index > 8:
            print("That square is out of range.")
            continue
        if board[index]:
            print("That square is already taken.")
            continue
        return index


def play():
    board = [""] * 9
    player = "X"

    print("Tic-Tac-Toe")
    print("Squares are numbered 1-9. X goes first.")

    for _ in range(9):
        render(board)
        board[ask_move(board, player)] = player
        if winner(board):
            render(board)
            print(f"Player {player} wins.")
            return
        player = "O" if player == "X" else "X"

    render(board)
    print("It's a draw.")


def main():
    while True:
        play()
        again = input("Play again? (y/n): ").strip().lower()
        if again not in ("y", "yes"):
            print("Thanks for playing.")
            return


if __name__ == "__main__":
    main()
