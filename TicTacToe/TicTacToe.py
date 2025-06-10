def printBoard(board):
    for r in board:
        print(" | ".join(r))
        print("-" * 9)

def isFull(board):
    for r in board:
        for i in r:
            if i == " ":
                return False
    return True

def checkWinner(board, p):
    for i in range(3):
        if all(board[i][j] == p for j in range(3)):
            return True
        if all(board[j][i] == p for j in range(3)):
            return True
    if all(board[i][i] == p for i in range(3)):
        return True
    if all(board[i][2 - i] == p for i in range(3)):
        return True
    return False

def minimax(board, isMaximizing):
    if checkWinner(board, "X"):
        return 1
    if checkWinner(board, "O"):
        return -1
    if isFull(board):
        return 0

    if isMaximizing:
        best = -float("inf")
        for i, j in [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]:
            board[i][j] = "X"
            val = minimax(board, False)
            board[i][j] = " "
            best = max(best, val)
        return best
    else:
        best = float("inf")
        for i, j in [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]:
            board[i][j] = "O"
            val = minimax(board, True)
            board[i][j] = " "
            best = min(best, val)
        return best

def bestMove(board):
    best_score = -float("inf")
    move = None
    for i, j in [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]:
        board[i][j] = "X"
        score = minimax(board, False)
        board[i][j] = " "
        if score > best_score:
            best_score = score
            move = (i, j)
    return move

board = [[" "]*3 for _ in range(3)]
print("Tic-Tac-Toe You = O and AI = X")
print("You can enter move in the format: row column (0-based index)")
printBoard(board)

while True:
    rc = input("Enter Move (ex: 1 1): ").split()
    if len(rc) != 2 or not all(x.isdigit() for x in rc):
        print("Invalid input format! Please enter row and column as numbers separated by space.")
        continue

    r, c = int(rc[0]), int(rc[1])

    if 0 <= r < 3 and 0 <= c < 3 and board[r][c] == " ":
        board[r][c] = "O"
        printBoard(board)
        if checkWinner(board, "O"):
            print("You Won!")
            break
        if isFull(board):
            print("It's a Tie!")
            break

        m = bestMove(board)
        if m:
            board[m[0]][m[1]] = "X"
            print("AI's Move:")
            printBoard(board)
            if checkWinner(board, "X"):
                print("AI Won!")
                break
            if isFull(board):
                print("It's a Tie!")
                break
    else:
        print("Invalid Move... Try again.")
