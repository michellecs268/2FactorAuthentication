import argparse
import hashlib
from datetime import datetime

class Connect:
    def __init__(self, username, password, pin=None):
        self.username = username
        self.password = password
        self.pin = pin

    def register_user(self):
        if self.password == "new":
            print("Registering new user.")
            new_password = input("Enter new password: ")
            
            while len(new_password) < 8 or not any(pw.isupper() for pw in new_password) or not any(pw.islower() for pw in new_password):
                print("Password should have a length of at least 8 and have at least 1 uppercase character and 1 lowercase character")
                new_password = input("Enter new password: ")

            # New user should be prompted to enter a password twice for confirmation
            confirm_password = input("Confirm password: ")
            
            if new_password == confirm_password:
                # Write (save) new user and password into Passwords.txt
                print(f"User '{self.username}' registered with password.")
                with open("Passwords.txt", "a") as f:
                    f.write(self.username + " " + new_password + "\n")
            else:
                print("Passwords do not match. Registration failed.")
        else:
            self.login()

    # Validate PIN for login
    def login(self):
        if self.pin is None:
            print("Error: PIN is required for login.")
            return

        if self.login_valid():
            generated_pin = self.otp()
            valid = (generated_pin == self.pin)
            if valid:
                print("Authentication success!")
            else:
                print("Authentication failed. Invalid PIN.")

    # Validate login credentials (username & password)
    def login_valid(self):
        try:
            with open("Passwords.txt", "r") as f:
                for line in f:
                    registered_user, registered_password = line.strip().split()
                    if registered_user == self.username:
                        if registered_password == self.password:
                            return True
                        else:
                            print("Error: Invalid username or password. Please try again.")
                            return False
            print("Error: User not found.")
            return False
            
        except FileNotFoundError:
            print("Error: File 'Passwords.txt' not found")
        except IOError:
            print("Error: An I/O error occurred while trying to open 'Passwords.txt'")
        return False

    def otp(self):
        original = self.username + self.password
        now = datetime.now()
        time_window = now.timestamp() // 15  # Divide current timestamp by 15 and discard any remainder

        # Concatenate the original username and password with the time window
        concatenated = original + str(time_window)
        
        # Encode and hash the concatenated string
        encoded = concatenated.encode()
        result = hashlib.md5(encoded)
        result_hex = result.hexdigest()

        # Obtain first 6 digits from the hash
        otp = ""
        counter = 0
        while counter != 6:
            if not result_hex[counter].isalpha():
                otp += result_hex[counter]
            else:
                # Convert the letter to a number, a = 1, b = 2, etc.
                lowercase_letter = result_hex[counter].lower()
                otp += str(ord(lowercase_letter) - 96)
            counter += 1

        return otp

def main():
    parser = argparse.ArgumentParser(description="Connect CLI Application")
    parser.add_argument("username", type=str, help="Enter username")
    parser.add_argument("password", type=str, help="Enter password")
    parser.add_argument("pin", type=str, nargs='?', help="Enter PIN to login")

    args = parser.parse_args()
    
    connect = Connect(args.username, args.password, args.pin)
    connect.register_user()

if __name__ == "__main__":
    main()