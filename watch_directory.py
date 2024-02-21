import os
import random
import string
from datetime import datetime
import time

source_directory = "C:/Users/mohamad/Desktop/test"
destination_base = "C:/Users/mohamad/Desktop/test"
counter = 1
log_file = "move_log.txt"

def generate_random_string(length=5):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def move_files():
    global counter
    for filename in os.listdir(source_directory):
        if filename.endswith(".cdr"):
            source_path = os.path.join(source_directory, filename)
            destination_folder = f"z{counter}"
            destination_path = os.path.join(destination_base, destination_folder)
            try:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                log_entry = f"{timestamp[:-3]}: Moving file {filename} to {destination_folder}\n"
                print(log_entry.strip())
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(log_entry)
                os.makedirs(destination_path, exist_ok=True)
                destination_file_path = os.path.join(destination_path, filename)
                while os.path.exists(destination_file_path):
                    new_filename = f"{os.path.splitext(filename)[0]}_{generate_random_string()}{os.path.splitext(filename)[1]}"
                    destination_file_path = os.path.join(destination_path, new_filename)
                os.rename(source_path, destination_file_path)
                counter = (counter % 3) + 1
            except Exception as e:
                error_message = f"Error moving file {filename}: {e}\n"
                print(error_message.strip())
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(error_message)

if __name__ == "__main__":
    print("Moving existing files...")
    move_files()
    print("Waiting for 5 seconds...")
    time.sleep(5)
    print("Watching for file creation events...")

    # Now start watching for file creation events
    # Add your event observer code here.
