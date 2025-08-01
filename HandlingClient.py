import threading
board = [' '] * 9
current_turn = 'X'
game_over = False
lock = threading.Lock()

def print_board():
    return (f"{board[0]}|{board[1]}|{board[2]}\n"
            f"-+-+-\n"
            f"{board[3]}|{board[4]}|{board[5]}\n"
            f"-+-+-\n"
            f"{board[6]}|{board[7]}|{board[8]}")


def check_winner():
    win_combos = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                  (0, 3, 6), (1, 4, 7), (2, 5, 8),
                  (0, 4, 8), (2, 4, 6)]
    for a, b, c in win_combos:
        if board[a] == board[b] == board[c] != ' ':
            return board[a]
    return None

def handle_client(conn, player):
    global current_turn, game_over
    conn.send(f"You are Player {player}\n".encode())

    while not game_over:
        with lock:
            conn.send(f"\n{print_board()}\n".encode())
            if current_turn == player:
                conn.send("Your move (0,8): ".encode())
                move = conn.recv(1024).decode().strip()
                if move.isdigit() and int(move) in range(9) and board[int(move)] == ' ':
                    board[int(move)] = player
                    winner = check_winner()
                    if winner:
                        game_over = True
                    elif ' ' not in board:
                        game_over = True
                    current_turn = 'O' if current_turn == 'X' else 'X'
                else:
                    conn.send("Invalid move, try again.\n".encode())
            else:
                conn.send("Wait for your turn...\n".encode())

    # Final board
    conn.send(f"\n{print_board()}\n".encode())
    winner = check_winner()
    if winner:
        conn.send(f"Game Over! Player {winner} wins!\n".encode())
    else:
        conn.send("Game Over! It's a Draw!\n".encode())
    conn.close()

