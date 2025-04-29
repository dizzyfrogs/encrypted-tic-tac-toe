# Encrypted Tic-Tac-Toe

A simple command-line Tic-Tac-Toe messenger that lets two players take turns by exchanging encrypted board-state strings. Every move is encrypted with a shared passphrase using PBKDF2-derived keys + Fernet (AES-CBC + HMAC).

---

## Table of Contents

- [Demo](#demo)  
- [Features](#features)  
- [Prerequisites](#prerequisites)  
- [Installation](#installation)  
- [Usage](#usage)  
- [How It Works](#how-it-works)  

---

## Demo

<details>
<summary>Start a new game (Player X)</summary>

```bash
$ python game.py
Enter encrypted string (or press Enter to start new game):
 
  0 | 1 | 2
 ---+---+---
  3 | 4 | 5
 ---+---+---
  6 | 7 | 8

Where will you place your X? > 4
Choose a passkey to encrypt this: abc
  
Encrypted string:
gAAAAABlZ... (send this to your friend)
```
</details>

<details>
<summary>Continue (Player O)</summary>

```bash
$ python game.py
Enter encrypted string (or press Enter to start new game): gAAAAABlZ...
Enter passkey to decrypt: abc

X placed at 4

  0 | 1 | 2
 ---+---+---
  3 | X | 5
 ---+---+---
  6 | 7 | 8

Where will you place your O? > 0
Enter passkey to encrypt your move: xyz

Encrypted string:
gAAAAABmY... (send back to X)
```
</details>

---

## Features

- **Symmetric encryption** via `cryptography.Fernet`
- **PBKDF2-SHA256** key derivation with a fixed salt  
- Full win/draw detection  
- Single-script CLI—no server required  

---

## Prerequisites

- Python 3.6+  
- [cryptography](https://pypi.org/project/cryptography/)  

---

## Installation

```bash
# Clone this repo
git clone https://github.com/dizzyfrogs/encrypted-tic-tac-toe.git
cd encrypted-tic-tac-toe

# Install dependencies
pip install cryptography
```

---

## Usage

```bash
python game.py
```

1. **New game** → press **Enter** when prompted for an encrypted string.  
2. **Place X** → enter a cell index (0-8).  
3. **Choose passkey** → script outputs an encrypted token.  
4. Send that token to your friend.  
5. **Your friend** runs the same script, pastes the token → decrypts → places **O** → re-encrypts → sends back.  
6. Repeat until someone wins or it’s a draw!

---

## How It Works

1. **Board state** is serialized as JSON:
   ```json
   { "board": "XO2XOO...", "last_move": 5 }
   ```
2. **Key derivation**: PBKDF2-SHA256 with a constant salt → 32-byte key → URL-safe base64.  
3. **Encryption**: `Fernet(key).encrypt(plaintext)` → Base64 token.  
4. **Decryption**: reverse process with the same passphrase.  
5. **Win/draw**: checks all 8 winning triple combinations + full-board condition.
