import argparse
import hashlib
from datetime import datetime, timedelta
import time

def main(username, password):
    # Combine username and password for processing
    original = username + password
    while True:
        # Get the current time
        now = datetime.now()
        # Calculate the 15-second time window
        time_window = now.timestamp() // 15

        # Combine it with window time for hashing
        concatenated = original + str(time_window)
        
        # Hash the combined string
        encoded = concatenated.encode()
        result = hashlib.md5(encoded)
        result_hex = result.hexdigest()

        # Generate 6 digit OTP from the hash
        otp = ""
        counter = 0
        while counter != 6:
            if not result_hex[counter].isalpha():
                otp += result_hex[counter]
            else:
                # Convert letters to numbers (a = 1, b = 2, etc.)
                lowercase_letter = result_hex[counter].lower()
                otp += str(ord(lowercase_letter) - 96)
            counter += 1

        print("Device: " + otp)

        # Find time left until the next 15 second interval
        next_window = (now + timedelta(seconds=15)).replace(second=(now.second // 15 + 1) * 15 % 60, microsecond=0)
        time_until_next_window = (next_window - datetime.now()).total_seconds()
        
        # Pause until the next 15 second interval
        time.sleep(time_until_next_window)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Device CLI Application")
    parser.add_argument("username", type=str, help="Enter your username")
    parser.add_argument("password", type=str, help="Enter your password")
    
    args = parser.parse_args()
    
    main(args.username, args.password)
