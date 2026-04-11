# 🔐 Secure Password Manager (Python + Streamlit)

A fully encrypted password manager built in Python, featuring:

- Master login authentication
- Encrypted password storage using Fernet (AES-128)
- Random password generator with user-defined length
- Add, view, update, and delete password entries
- Streamlit web interface for easy access
- Logging of all user actions

This project demonstrates secure credential handling, encryption best practices, and full-stack Python development.

---

## 🚀 Features

### 🔑 Master Authentication
- Users must log in before accessing any passwords.
- Credentials are encrypted and stored securely.

### 🔐 Encrypted Password Storage
- All passwords are encrypted using `cryptography.fernet`.
- No plaintext credentials are ever written to disk.

### 🔄 Password Management
- Add new passwords (manual or auto-generated)
- Update existing passwords
- Delete passwords
- View all stored passwords securely

### 🌐 Streamlit Web App
- Clean, simple UI
- Login screen
- Dashboard for password operations

---

## 🛠️ Technologies Used

- **Python 3**
- **Streamlit** (UI)
- **cryptography.fernet** (encryption)
- **JSON** (encrypted storage)
- **VS Code** (development)

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/secure-password-manager.git
cd secure-password-manager
