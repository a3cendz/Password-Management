import os
import json
import string
import random
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import ttk, simpledialog

# Directory where the key and password files will be stored
data_directory = "PassManage"

# Ensure the directory exists
if not os.path.exists(data_directory):
    os.makedirs(data_directory)

# Paths for key and password files
key_path = os.path.join(data_directory, "key.key")
passwords_path = os.path.join(data_directory, "passwords.json")

# Function to generate a key and save it to a file
def generate_key():
    key = Fernet.generate_key()
    with open(key_path, "wb") as key_file:
        key_file.write(key)
    return key

# Function to load the key from a file
def load_key():
    return open(key_path, "rb").read()

# Function to encrypt data
def encrypt_data(data, key):
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data

# Function to decrypt data
def decrypt_data(encrypted_data, key):
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data).decode()
    return decrypted_data

# Function to save password to file
def save_password(service, username, password, key):
    if os.path.exists(passwords_path):
        with open(passwords_path, "r") as file:
            passwords = json.load(file)
    else:
        passwords = {}

    passwords[service] = {
        "username": username,
        "password": encrypt_data(password, key).decode()
    }

    with open(passwords_path, "w") as file:
        json.dump(passwords, file)

# Function to retrieve password from file
def retrieve_password(service, key):
    if os.path.exists(passwords_path):
        with open(passwords_path, "r") as file:
            passwords = json.load(file)
        if service in passwords:
            encrypted_password = passwords[service]["password"].encode()
            password = decrypt_data(encrypted_password, key)
            return passwords[service]["username"], password
        else:
            return None, None
    else:
        return None, None

# Function to update password for a service
def update_password(service, new_password, key):
    if os.path.exists(passwords_path):
        with open(passwords_path, "r") as file:
            passwords = json.load(file)

        if service in passwords:
            passwords[service]["password"] = encrypt_data(new_password, key).decode()
            with open(passwords_path, "w") as file:
                json.dump(passwords, file)
            show_popup("Success", "Password updated successfully.")
        else:
            show_popup("Error", "No password found for the given service.")
    else:
        show_popup("Error", "No password file found.")

# Function to delete password for a service
def delete_password(service):
    if os.path.exists(passwords_path):
        with open(passwords_path, "r") as file:
            passwords = json.load(file)

        if service in passwords:
            del passwords[service]
            with open(passwords_path, "w") as file:
                json.dump(passwords, file)
            show_popup("Success", "Password deleted successfully.")
        else:
            show_popup("Error", "No password found for the given service.")
    else:
        show_popup("Error", "No password file found.")

# Function to generate a random strong password
def generate_random_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(12))
    return password

# Function to show custom pop-up
def show_popup(title, message):
    popup = tk.Toplevel()
    popup.title(title)
    popup.geometry("300x150")
    popup.configure(bg="#f7f7f7")

    style = ttk.Style()
    style.configure("TLabel", font=("Helvetica", 12), background="#f7f7f7")
    style.configure("TButton", font=("Helvetica", 12))

    label = ttk.Label(popup, text=message, style="TLabel")
    label.pack(pady=20)

    ok_button = ttk.Button(popup, text="OK", command=popup.destroy)
    ok_button.pack(pady=10)

    popup.transient(root)
    popup.grab_set()
    root.wait_window(popup)

# Function to manage passwords with GUI
def password_manager_gui():
    if not os.path.exists(key_path):
        key = generate_key()
        show_popup("Info", "Generated new encryption key.")
    else:
        key = load_key()

    def save_password_gui():
        service = simpledialog.askstring("Service", "Enter the service name:")
        if service:
            username = simpledialog.askstring("Username", "Enter the username:")
            if username:
                password = simpledialog.askstring("Password", "Enter the password:")
                if password:
                    save_password(service, username, password, key)
                    show_popup("Success", "Password saved successfully.")

    def retrieve_password_gui():
        service = simpledialog.askstring("Service", "Enter the service name:")
        if service:
            username, password = retrieve_password(service, key)
            if username and password:
                show_popup("Password", f"Username: {username}\nPassword: {password}")
            else:
                show_popup("Error", "No password found for the given service.")

    def update_password_gui():
        service = simpledialog.askstring("Service", "Enter the service name:")
        if service:
            new_password = simpledialog.askstring("New Password", "Enter the new password:")
            if new_password:
                update_password(service, new_password, key)
                show_popup("Success", "Password updated successfully.")

    def delete_password_gui():
        service = simpledialog.askstring("Service", "Enter the service name:")
        if service:
            delete_password(service)
            show_popup("Success", "Password deleted successfully.")

    def generate_password_gui():
        password = generate_random_password()
        show_popup("Generated Password", f"Generated strong password: {password}")

    global root
    root = tk.Tk()
    root.title("Password Manager")
    root.geometry("300x400")
    root.configure(bg="#f7f7f7")

    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 12), padding=10)
    style.configure("TLabel", font=("Helvetica", 14), background="#f7f7f7")

    ttk.Label(root, text="Password Manager").pack(pady=20)

    ttk.Button(root, text="Save a new password", command=save_password_gui).pack(pady=10)
    ttk.Button(root, text="Retrieve a password", command=retrieve_password_gui).pack(pady=10)
    ttk.Button(root, text="Generate a strong password", command=generate_password_gui).pack(pady=10)
    ttk.Button(root, text="Update a password", command=update_password_gui).pack(pady=10)
    ttk.Button(root, text="Delete a password", command=delete_password_gui).pack(pady=10)
    ttk.Button(root, text="Exit", command=root.quit).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    password_manager_gui()
