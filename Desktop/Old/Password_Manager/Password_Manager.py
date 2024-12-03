import os
import uuid
import pickle
import base64
import hashlib
import string
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from ctypes import windll
import re

class PasswordManager:
    def __init__(self):
        self.salt_length = 32
        self.iterations = 100000

    def get_usb_drive(self):
        bitmask = windll.kernel32.GetLogicalDrives()
        for letter in string.ascii_uppercase:
            if bitmask & 1:
                drive = f"{letter}:\\"
                if windll.kernel32.GetDriveTypeW(drive) == 2:
                    return drive
            bitmask >>= 1
        return None

    def check_password_strength(self, password):
        checks = [
            (len(password) >= 8, "Password must be at least 8 characters long"),
            (re.search(r"[A-Z]", password), "Must contain uppercase letters"),
            (re.search(r"[a-z]", password), "Must contain lowercase letters"), 
            (re.search(r"\d", password), "Must contain numbers"),
            (re.search(r"[!@#$%^&*(),.?\":{}|<>]", password), "Must contain special characters")
        ]
        
        for check, message in checks:
            if not check:
                return False, message
        return True, "Password meets requirements"

    def generate_key(self, password, salt=None):
        if salt is None:
            salt = os.urandom(self.salt_length)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=self.iterations
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt

    def encrypt_password(self, password, master_key):
        try:
            # Convert password to bytes and pad
            password_bytes = password.encode('utf-8')
            padding_length = 16 - (len(password_bytes) % 16)
            padded = password_bytes + (bytes([padding_length]) * padding_length)
            
            # Generate IV for AES
            iv = os.urandom(16)
            
            # AES encryption
            cipher = Cipher(algorithms.AES(master_key[:32]), modes.CBC(iv))
            encryptor = cipher.encryptor()
            encrypted = encryptor.update(padded) + encryptor.finalize()
            
            # Additional Fernet layer
            f = Fernet(base64.urlsafe_b64encode(hashlib.sha256(master_key).digest()))
            final_encrypted = f.encrypt(encrypted)
            
            return {'encrypted': final_encrypted, 'iv': iv}
        except Exception as e:
            print(f"\nEncryption error: {e}")
            return None

    def decrypt_password(self, encrypted_data, master_key):
        try:
            # Fernet decryption
            f = Fernet(base64.urlsafe_b64encode(hashlib.sha256(master_key).digest()))
            encrypted = f.decrypt(encrypted_data['encrypted'])
            
            # AES decryption
            cipher = Cipher(algorithms.AES(master_key[:32]), modes.CBC(encrypted_data['iv']))
            decryptor = cipher.decryptor()
            padded = decryptor.update(encrypted) + decryptor.finalize()
            
            # Remove padding
            padding_length = padded[-1]
            password_bytes = padded[:-padding_length]
            
            return password_bytes.decode('utf-8')
        except Exception as e:
            print(f"\nDecryption error: {e}")
            return None

    def save_to_usb(self, username, data):
        usb_drive = self.get_usb_drive()
        if not usb_drive:
            print("\nCan not decrypt the password. Is USB inserted?")
            return False
        
        try:
            usb_path = os.path.join(usb_drive, "passwords")
            os.makedirs(usb_path, exist_ok=True)
            file_path = os.path.join(usb_path, f"{username}.enc")
            
            with open(file_path, 'wb') as f:
                pickle.dump(data, f)
            print(f"\nPassword saved to USB: {file_path}")
            return True
        except Exception as e:
            print(f"\nError saving to USB: {e}")
            return False

    def load_from_usb(self, username):
        usb_drive = self.get_usb_drive()
        if not usb_drive:
            print("\nPlease insert a USB drive")
            return None
        
        try:
            file_path = os.path.join(usb_drive, "passwords", f"{username}.enc")
            with open(file_path, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            print(f"\nNo password found for {username}")
            return None
        except Exception as e:
            print(f"\nError loading from USB: {e}")
            return None

    def encrypt_new_password(self):
        print("\n=== Password Encryption ===")
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
        
        is_strong, message = self.check_password_strength(password)
        if not is_strong:
            print(f"\nWeak password: {message}")
            return
        
        master_password = input("Enter master password: ").strip()
        master_key, salt = self.generate_key(master_password)
        encrypted_data = self.encrypt_password(password, master_key)
        
        if encrypted_data:
            data = {
                'username': username,
                'encrypted': encrypted_data,
                'salt': salt
            }
            
            if self.save_to_usb(username, data):
                print("\nPassword encrypted and saved successfully")
            else:
                print("\nFailed to save encrypted password! Is USB inserted?")

    def decrypt_existing_password(self):
        print("\n=== Password Decryption ===")
        username = input("Enter username: ").strip()
        data = self.load_from_usb(username)
        
        if data:
            master_password = input("Enter master password: ").strip()
            master_key, _ = self.generate_key(master_password, data['salt'])
            decrypted = self.decrypt_password(data['encrypted'], master_key)
            
            if decrypted:
                print(f"\nDecrypted password for {username}: {decrypted}")
            else:
                print("\nDecryption failed - incorrect master password")

def main():
    pm = PasswordManager()
    
    while True:
        print("\n=== Password Manager ===")
        print("1. Encrypt New Password")
        print("2. Decrypt Password")
        print("3. Exit")
        
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == '1':
            pm.encrypt_new_password()
        elif choice == '2':
            pm.decrypt_existing_password()
        elif choice == '3':
            print("\nExiting...")
            break
        else:
            print("\nInvalid choice")

if __name__ == "__main__":
    main()