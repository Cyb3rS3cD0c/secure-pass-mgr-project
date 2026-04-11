import streamlit as st
from password_manager_project import (
    read_encrypted_json,
    write_encrypted_json,
    generate_password,
    log_action,
    MASTER_LOGIN,
    PASSWORD_FILE,
)

# ---------- Authentication helpers ----------

def check_master_credentials(username: str, password: str) -> bool:
    data = read_encrypted_json(MASTER_LOGIN)
    if not data:
        return False
    return username == data.get("username") and password == data.get("password")


def login_screen():
    st.title("Secure Password Manager")

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.subheader("Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if check_master_credentials(username, password):
                st.session_state.authenticated = True
                log_action("Logged in via Streamlit UI")
                st.success("Login successful.")
            else:
                st.error("Invalid credentials.")

    return st.session_state.authenticated


# ---------- Password manager UI ----------

def view_passwords_ui():
    st.subheader("View Stored Passwords")
    data = read_encrypted_json(PASSWORD_FILE)

    if not data:
        st.info("No passwords stored.")
        return

    for domain, pwd in data.items():
        st.write(f"**{domain}**: `{pwd}`")

    log_action("Viewed passwords via Streamlit UI")


def add_password_ui():
    st.subheader("Add New Password")

    domain = st.text_input("Domain / Application")
    manual_pwd = st.text_input("Password (leave blank to auto-generate)", type="password")
    length = st.number_input("Password length (for auto-generate)", min_value=8, value=12, step=1)

    if st.button("Save Password"):
        if not domain:
            st.error("Domain is required.")
            return

        pwd = manual_pwd or generate_password(int(length))

        data = read_encrypted_json(PASSWORD_FILE)
        data[domain] = pwd
        write_encrypted_json(PASSWORD_FILE, data)

        log_action(f"Added password for {domain} via Streamlit UI")
        st.success(f"Password saved for {domain}.")


def update_password_ui():
    st.subheader("Update Password")

    data = read_encrypted_json(PASSWORD_FILE)
    domains = list(data.keys())

    if not domains:
        st.info("No passwords to update.")
        return

    domain = st.selectbox("Select domain to update", domains)
    manual_pwd = st.text_input("New password (leave blank to auto-generate)", type="password")
    length = st.number_input("Password length (for auto-generate)", min_value=8, value=12, step=1)

    if st.button("Update Password"):
        pwd = manual_pwd or generate_password(int(length))
        data[domain] = pwd
        write_encrypted_json(PASSWORD_FILE, data)

        log_action(f"Updated password for {domain} via Streamlit UI")
        st.success(f"Password updated for {domain}.")


def delete_password_ui():
    st.subheader("Delete Password")

    data = read_encrypted_json(PASSWORD_FILE)
    domains = list(data.keys())

    if not domains:
        st.info("No passwords to delete.")
        return

    domain = st.selectbox("Select domain to delete", domains)

    if st.button("Delete Password"):
        del data[domain]
        write_encrypted_json(PASSWORD_FILE, data)

        log_action(f"Deleted password for {domain} via Streamlit UI")
        st.success(f"Password deleted for {domain}.")


# ---------- Main Streamlit app ----------

def main():
    authenticated = login_screen()
    if not authenticated:
        return

    st.sidebar.title("Menu")
    choice = st.sidebar.radio(
        "Go to",
        ("View Passwords", "Add Password", "Update Password", "Delete Password"),
    )

    if choice == "View Passwords":
        view_passwords_ui()
    elif choice == "Add Password":
        add_password_ui()
    elif choice == "Update Password":
        update_password_ui()
    elif choice == "Delete Password":
        delete_password_ui()


if __name__ == "__main__":
    main()