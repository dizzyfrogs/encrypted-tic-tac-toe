import json, base64, sys
from getpass import getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

SALT = b"tictactoe_game_salt"
WIN_COMBOS = [
    (0,1,2), (3,4,5), (6,7,8),  # rows
    (0,3,6), (1,4,7), (2,5,8),  # cols
    (0,4,8), (2,4,6)            # diags
]

def derive_key(password: str) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=100_000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt(plaintext: str, password: str) -> str:
    return Fernet(derive_key(password)).encrypt(plaintext.encode()).decode()

def decrypt(token: str, password: str) -> str:
    return Fernet(derive_key(password)).decrypt(token.encode()).decode()

def display_board(board: str):
    c = list(board)
    print(f"""
         {c[0]} | {c[1]} | {c[2]}
        ---+---+---
         {c[3]} | {c[4]} | {c[5]}
        ---+---+---
         {c[6]} | {c[7]} | {c[8]}
        """)

def ask_move(board: str, symbol: str) -> int:
    while True:
        try:
            mv = int(input(f"Where will you place your {symbol}? > "))
            if 0 <= mv < 9 and board[mv] not in ("X","O"):
                return mv
        except ValueError:
            pass
        print("Invalid spot. Try 0-8 on an empty cell.")

def check_result(board: str):
    # Return 'X' or 'O' if someone won, 'Draw' if full, else None.
    for a,b,c in WIN_COMBOS:
        if board[a] == board[b] == board[c] and board[a] in ("X","O"):
            return board[a]
    if all(cell in ("X","O") for cell in board):
        return "Draw"
    return None

def main():
    token = input("Enter encrypted string (or press Enter to start new game): ").strip()

    # NEW GAME
    if not token:
        board = [str(i) for i in range(9)]
        display_board("".join(board))
        mv = ask_move("".join(board), "X")
        board[mv] = "X"
        result = check_result("".join(board))
        if result:
            print("Game over right away:", result)
        payload = {"board":"".join(board), "last_move": mv}
        pwd = getpass("Choose a passkey to encrypt this: ")
        print("\nEncrypted string:\n" + encrypt(json.dumps(payload), pwd))
        sys.exit(0)

    # CONTINUE GAME
    pwd = getpass("Enter passkey to decrypt: ")
    try:
        plain = decrypt(token, pwd)
    except Exception as e:
        print("Decryption failed.", e)
        sys.exit(1)

    data = json.loads(plain)
    board = list(data["board"])
    lm = data["last_move"]
    last_sym = board[lm]
    print(f"\n{last_sym} placed at {lm}.")
    display_board("".join(board))

    # check if that was a terminal board
    result = check_result("".join(board))
    if result:
        msg = "It's a draw!" if result=="Draw" else f"{result} won!"
        print("Game over on your friend's move:", msg)
        sys.exit(0)

    # your move
    symbol = "O" if last_sym=="X" else "X"
    mv = ask_move("".join(board), symbol)
    board[mv] = symbol

    # check your move for win/draw
    result = check_result("".join(board))
    if result:
        msg = "You've drawn the game." if result=="Draw" else f"You win as {symbol}!"
        print(msg)

    payload = {"board":"".join(board), "last_move": mv}
    pwd2 = getpass("Enter passkey to encrypt your move: ")
    print("\nEncrypted string to send:\n" + encrypt(json.dumps(payload), pwd2))

if __name__ == "__main__":
    main()
