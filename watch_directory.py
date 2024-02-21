import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import random
import string
from datetime import datetime
import config  # Importing config.py

source_directory = config.source_directory
destination_base = config.destination_base
destination_folders = config.destination_folders
log_file = config.log_file

counter = 0  # Initialize counter to start with the first folder

def generate_random_string(length=5):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        global counter
        for filename in os.listdir(source_directory):
            if filename.endswith(".cdr"):
                source_path = os.path.join(source_directory, filename)
                destination_folder = destination_folders[counter]
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
                    counter = (counter + 1) % len(destination_folders)  # Update counter
                except Exception as e:
                    error_message = f"Error moving file {filename}: {e}\n"
                    print(error_message.strip())
                    with open(log_file, "a", encoding="utf-8") as f:
                        f.write(error_message)

def move_existing_files():
    global counter
    for filename in os.listdir(source_directory):
        if filename.endswith(".cdr"):
            source_path = os.path.join(source_directory, filename)
            destination_folder = destination_folders[counter]
            destination_path = os.path.join(destination_base, destination_folder)
            try:
                os.makedirs(destination_path, exist_ok=True)
                destination_file_path = os.path.join(destination_path, filename)
                while os.path.exists(destination_file_path):
                    new_filename = f"{os.path.splitext(filename)[0]}_{generate_random_string()}{os.path.splitext(filename)[1]}"
                    destination_file_path = os.path.join(destination_path, new_filename)
                os.rename(source_path, destination_file_path)
                counter = (counter + 1) % len(destination_folders)  # Update counter
            except Exception as e:
                error_message = f"Error moving file {filename}: {e}\n"
                print(error_message.strip())
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(error_message)

if __name__ == "__main__":
    move_existing_files()  # Move existing files before watching for file creation events
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=source_directory, recursive=False)
    observer.start()

    try:
        print("Watching for file creation events...")
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Stopping observer.")
        observer.stop()
    observer.join()
