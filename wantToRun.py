import tkinter as tk
from tkinter import filedialog
import threading
import time
import os
import random
import string
from datetime import datetime
import sys

# Importing watch_directory.py code here


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("File Mover")
        
        # Variables for user configurations
        self.source_directory_var = tk.StringVar()
        self.destination_base_var = tk.StringVar()
        
        # Initialize GUI components
        self.create_widgets()
        
    def create_widgets(self):
        # Labels
        tk.Label(self.root, text="Source Directory:").grid(row=0, column=0, sticky="w")
        tk.Label(self.root, text="Destination Base:").grid(row=1, column=0, sticky="w")
        
        # Entries
        self.source_directory_entry = tk.Entry(self.root, textvariable=self.source_directory_var)
        self.source_directory_entry.grid(row=0, column=1)
        self.destination_base_entry = tk.Entry(self.root, textvariable=self.destination_base_var)
        self.destination_base_entry.grid(row=1, column=1)
        
        # Browse buttons
        tk.Button(self.root, text="Browse", command=self.browse_source_directory).grid(row=0, column=2)
        tk.Button(self.root, text="Browse", command=self.browse_destination_base).grid(row=1, column=2)
        
        # Start and Stop Buttons
        self.start_button = tk.Button(self.root, text="Start", command=self.start_script)
        self.start_button.grid(row=2, column=0, sticky="we", padx=5, pady=5)
        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_script, state=tk.DISABLED)
        self.stop_button.grid(row=2, column=1, sticky="we", padx=5, pady=5)
        
        # Log Textbox
        self.log_text = tk.Text(self.root, height=10, width=50)
        self.log_text.grid(row=3, column=0, columnspan=3, padx=5, pady=5)
        
    def browse_source_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.source_directory_var.set(directory)
            
    def browse_destination_base(self):
        directory = filedialog.askdirectory()
        if directory:
            self.destination_base_var.set(directory)
        
    def start_script(self):
        # Get user configurations
        source_directory = self.source_directory_var.get()
        destination_base = self.destination_base_var.get()
        
        # Start the script in a separate thread
        self.script_thread = threading.Thread(target=self.run_script, args=(source_directory, destination_base))
        self.script_thread.start()
        
        # Disable start button and enable stop button
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
    def stop_script(self):
        # Stop the script
        os._exit(0)  # Not recommended, but for simplicity
        
    def run_script(self, source_directory, destination_base):
        # Execute the script logic
        global counter
        while True:
            for filename in os.listdir(source_directory):
                if filename.endswith(".cdr"):
                    source_path = os.path.join(source_directory, filename)
                    destination_folder = destination_folders[counter]
                    destination_path = os.path.join(destination_base, destination_folder)
                    try:
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                        log_entry = f"{timestamp[:-3]}: Moving file {filename} to {destination_folder}\n"
                        self.update_log(log_entry)
                        os.makedirs(destination_path, exist_ok=True)
                        destination_file_path = os.path.join(destination_path, filename)
                        while os.path.exists(destination_file_path):
                            new_filename = f"{os.path.splitext(filename)[0]}_{generate_random_string()}{os.path.splitext(filename)[1]}"
                            destination_file_path = os.path.join(destination_path, new_filename)
                        os.rename(source_path, destination_file_path)
                        counter = (counter + 1) % len(destination_folders)  # Update counter
                    except Exception as e:
                        error_message = f"Error moving file {filename}: {e}\n"
                        self.update_log(error_message)
            time.sleep(10)  # Adjust as needed
    
    def update_log(self, message):
        self.log_text.insert(tk.END, message)
        self.log_text.see(tk.END)  # Scroll to the end of the log


def generate_random_string(length=5):
    return ''.join(random.choices(string.ascii_lowercase, k=length))


if __name__ == "__main__":
    counter = 0  # Initialize counter to start with the first folder
    
    # GUI
    root = tk.Tk()
    app = App(root)
    root.mainloop()
