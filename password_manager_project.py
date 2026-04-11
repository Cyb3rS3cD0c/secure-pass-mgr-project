# Importing Libraries

import os
import json
import string
import secrets
from datetime import datetime
from cryptography.fernet import Fernet

# Generate or load the encryption key
# This ensures the same key is used every time.

KEY_FILE = "secret.key"

def load_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    else:
        with open(KEY_FILE, "rb") as f:
            key = f.read()
    return key

cipher = Fernet(load_key())

# Encrypted File Read/Write Helpers: These functions will replace your normal JSON read/write.
# Encrypt master login file
# Encrypt password storage file

def write_encrypted_json(filename, data):
    json_bytes = json.dumps(data).encode()
    encrypted = cipher.encrypt(json_bytes)
    with open(filename, "wb") as f:
        f.write(encrypted)

def read_encrypted_json(filename):
    if not os.path.exists(filename):
        return {}
    with open(filename, "rb") as f:
        encrypted = f.read()
    decrypted = cipher.decrypt(encrypted)
    return json.loads(decrypted.decode())

# Password Generator

def generate_password(length: int) -> str:
    """Generate a secure random password."""
    if length < 8:
        raise ValueError("Password length must be at least 8 characters.")

    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))

# Master Login System

MASTER_LOGIN = "master_login.json"

def create_master_account():
    print("\n=== Create Master Account ===")
    username = input("Create master username: ")
    password = input("Create master password: ")

    data = {"username": username, "password": password}
    write_encrypted_json(MASTER_LOGIN, data)

    print("Master account created successfully.\n")

def authenticate():
    """Authenticate the user with encrypted master credentials."""
    if not os.path.exists(MASTER_LOGIN):
        print("No master account found. Creating one now.")
        create_master_account()

    stored = read_encrypted_json(MASTER_LOGIN)

    for _ in range(3):
        print("\n=== Login ===")
        u = input("Username: ")
        p = input("Password: ")

        if u == stored["username"] and p == stored["password"]:
            print("Login successful.\n")
            return True

        print("Incorrect credentials.")

    print("Too many failed attempts. Exiting.")
    return False

# Logging

LOG_FILE = "log.txt"

def log_action(action):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} - {action}\n")

# Password Storage

PASSWORD_FILE = "app_password.json"

#Add Password

def add_password():
    print("\n=== Add New Password ===")
    domain = input("Enter domain/application name: ")

    # Let user choose manual or auto-generated password
    pwd = input("Enter password (leave blank to auto-generate): ")

    if not pwd:
        length = int(input("Enter desired password length: "))
        pwd = generate_password(length)
        print(f"Generated password: {pwd}")

    data = read_encrypted_json(PASSWORD_FILE)
    data[domain] = pwd
    write_encrypted_json(PASSWORD_FILE, data)

    log_action(f"Added password for {domain}")
    print("Password saved successfully.\n")

# View Stored Password

def view_passwords():
    print("\n=== Stored Passwords ===")
    data = read_encrypted_json(PASSWORD_FILE)

    if not data:
        print("No passwords stored.\n")
        return

    for domain, pwd in data.items():
        print(f"{domain}: {pwd}")

    log_action("Viewed stored passwords")
    print()

# Update Password

def update_password():
    print("\n=== Update Password ===")
    domain = input("Enter domain/application to update: ")

    data = read_encrypted_json(PASSWORD_FILE)

    if domain not in data:
        print("Domain not found.\n")
        return

    pwd = input("Enter new password (leave blank to auto-generate): ")

    if not pwd:
        length = int(input("Enter desired password length: "))
        pwd = generate_password(length)
        print(f"Generated password: {pwd}")

    data[domain] = pwd
    write_encrypted_json(PASSWORD_FILE, data)

    log_action(f"Updated password for {domain}")
    print("Password updated successfully.\n")

# Delete Password

def delete_password():
    print("\n=== Delete Password ===")
    domain = input("Enter domain/application to delete: ")

    data = read_encrypted_json(PASSWORD_FILE)

    if domain not in data:
        print("Domain not found.\n")
        return

    del data[domain]
    write_encrypted_json(PASSWORD_FILE, data)

    log_action(f"Deleted password for {domain}")
    print("Password deleted successfully.\n")

# Main Menu

def main_menu():
    while True:
        print("=== Password Manager ===")
        print("1. View Stored Passwords")
        print("2. Add New Password")
        print("3. Update Password")
        print("4. Delete Password")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            view_passwords()
        elif choice == "2":
            add_password()
        elif choice == "3":
            update_password()
        elif choice == "4":
            delete_password()
        elif choice == "5":
            print("Exiting Password Manager.")
            break
        else:
            print("Invalid choice. Try again.\n")

# Entry Point for Program

if __name__ == "__main__":
    if authenticate():
        main_menu()
