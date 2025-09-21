import json
from cryptography.fernet import Fernet

def load_key():
    """Load the Fernet key from secret.txt"""
    with open("secret.txt", "r", encoding="utf-8") as key_file:
        key = key_file.read().strip()
    return key.encode("utf-8")

def decrypt_json_file(filename, fernet):
    """Decrypt an encrypted JSON file and return the data as a Python object."""
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    # Decrypt the data and decode it to a string
    decrypted_data = fernet.decrypt(encrypted_data).decode("utf-8")
    return json.loads(decrypted_data)

def main():
    # Load the encryption key and create a Fernet object
    key = load_key()
    fernet = Fernet(key)

    # Prompt for the encrypted JSON file name
    filename = input("Enter the name of the encrypted JSON file (e.g., users.json): ")
    
    try:
        data = decrypt_json_file(filename, fernet)
        print("Decrypted data:")
        print(json.dumps(data, indent=4))
    except Exception as e:
        print(f"Error decrypting file: {e}")

if __name__ == "__main__":
    main()
