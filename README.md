# password-manager

A CLI password manager that encrypts and stores your passwords locally using [cryptmoji](https://pypi.org/project/cryptmoji/) — an encryption library that encodes your passwords as emoji sequences. All data is stored locally on your machine, never in the cloud.

---

## Features

- **Secure local storage** — passwords are encrypted and saved to a local `.vault.json` file
- **Master key authentication** — vault access is protected by an encrypted master key stored in `.master.json`
- **Add, view, edit and delete** password entries
- **Password generator** — generates strong random passwords of a chosen length (8–32 characters)
- **Clipboard support** — generated and retrieved passwords can be copied directly to your clipboard
- **Emoji encryption** — passwords are stored and displayed as emoji sequences via cryptmoji

---

## Requirements

- Python 3.10+
- pip

---

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/password-manager.git
cd password-manager

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Usage

```bash
python main.py
```

On first run you will be prompted to set up a master key. On subsequent runs you will be asked to authenticate before accessing your vault.

---

## Main Menu

```
1. Add password
2. Get password
3. List services
0. Exit
```

### Adding a password

```
Add password
Enter the service: CS50
Enter the username: student@cs50
1. Enter the password
2. Generate a strong password
Enter the length of the password [8-32]: 17
Generated password: 🧟❔🆓🈲🩸🆙🈺🩹🧾🪓✅🧢🧹🧞🈁🈵➖
Password copied to clipboard

Password added successfully!
```

### Viewing a password

```
Enter the service: Google

Username: user@gmail.com
Password: 🆙🈁🆚🆕🆕🃏🆖❔🈁🆙

1. Copy to clipboard
2. Show password
0. Go back
```

### Listing services

```
Services
1. Google
2. Facebook
3. GitHub
0. Go back
```

From the list you can select any service to view, edit, or delete its entry.

---

## How It Works

- **Vault** — the core class responsible for creating and managing the vault, authenticating the user, and handling all CRUD operations on password entries
- **Encryption** — all passwords are encrypted with `cryptmoji` before being stored, and decrypted only when explicitly requested by the authenticated user
- **Storage** — `.vault.json` stores encrypted password entries, `.master.json` stores the encrypted master key. Both files are created automatically on first run
- **Password generation** — uses Python's `random` and `string` modules to generate cryptographically random printable passwords
- **CLI** — built with [click](https://click.palletsprojects.com/) for clean and easy terminal interaction

---

## Security Notes

- Passwords never leave your machine — there is no network communication or cloud sync
- Both the vault and master key are encrypted at rest
- The master key is never stored in plaintext
