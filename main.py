import os
import json
import string
import random
from cryptography.fernet import Fernet

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
            print("Password updated successfully.")
        else:
            print("No password found for the given service.")
    else:
        print("No password file found.")

# Function to delete password for a service
def delete_password(service):
    if os.path.exists(passwords_path):
        with open(passwords_path, "r") as file:
            passwords = json.load(file)

        if service in passwords:
            del passwords[service]
            with open(passwords_path, "w") as file:
                json.dump(passwords, file)
            print("Password deleted successfully.")
        else:
            print("No password found for the given service.")
    else:
        print("No password file found.")

# Function to generate a random strong password
def generate_random_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(12))
    return password

# Main function to manage passwords
def password_manager():
    if not os.path.exists(key_path):
        key = generate_key()
        print("Generated new encryption key.")
    else:
        key = load_key()

    while True:
        print("\nPassword Manager")
        print("1. Save a new password")
        print("2. Retrieve a password")
        print("3. Generate a strong password")
        print("4. Update a password")
        print("5. Delete a password")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            service = input("Enter the service name: ")
            username = input("Enter the username: ")
            password = input("Enter the password: ")
            save_password(service, username, password, key)
            print("Password saved successfully.")
        elif choice == "2":
            service = input("Enter the service name: ")
            username, password = retrieve_password(service, key)
            if username and password:
                print(f"Username: {username}")
                print(f"Password: {password}")
            else:
                print("No password found for the given service.")
        elif choice == "3":
            print(f"Generated strong password: {generate_random_password()}")
        elif choice == "4":
            service = input("Enter the service name: ")
            new_password = input("Enter the new password: ")
            update_password(service, new_password, key)
        elif choice == "5":
            service = input("Enter the service name: ")
            delete_password(service)
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    password_manager()
