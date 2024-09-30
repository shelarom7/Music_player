import os
import json
import tkinter as tk
from tkinter import filedialog
from pygame import mixer

# Initialize the mixer
mixer.init()

# Define the JSON file path
json_file_path = 'songs.json'

# Load the song library from the JSON file
def load_song_library():
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            return json.load(file)
    else:
        return {}  # Return an empty dictionary if the file doesn't exist

# Save the song library to the JSON file
def save_song_library():
    with open(json_file_path, 'w') as file:
        json.dump(song_library, file, indent=4)

# Create the main application window
root = tk.Tk()
root.title("Music Player")
root.geometry("400x700")  # Adjusted height for the new button and status
root.configure(bg="#1e1e1e")  # Dark background for the app

# Load song library from JSON
song_library = load_song_library()

# Create a list to store the current view of songs in the listbox
displayed_songs = sorted(song_library.keys())  # Sort songs alphabetically initially
played_songs = []  # List to store played songs

# Define functions for music controls and status update
def update_status(message):
    status_label.config(text=f"Status: {message}")

def play_music():
    selected_song = song_listbox.get(tk.ACTIVE)  # Get the selected song
    if selected_song in played_songs:
        update_status("Already Played")
        return  # Do not play the song again if it's already been played
    track = song_library[selected_song]
    mixer.music.load(track)
    mixer.music.play()
    highlight_playing_song()
    update_status("Playing")
    played_songs.append(selected_song)  # Add the song to played songs

def pause_music():
    mixer.music.pause()
    update_status("Paused")

def unpause_music():
    mixer.music.unpause()
    update_status("Playing")

def stop_music():
    mixer.music.stop()
    update_status("Stopped")
    clear_highlight()
    played_songs.clear()  # Clear played songs when stopping music

# New function to add a song
def add_song():
    # Open file dialog to select a song file
    file_path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
    
    if file_path:  # Check if a file was selected
        # Extract the file name from the path
        song_name = os.path.basename(file_path).replace(".mp3", "")
        
        if song_name not in song_library:
            # Add the song to the song library and the list
            song_library[song_name] = file_path
            displayed_songs.append(song_name)
            displayed_songs.sort()  # Sort the list after adding the new song
            update_song_listbox()
            save_song_library()  # Save the updated song library to JSON
        else:
            update_status("Song already exists")

# New function to delete a song
def delete_song():
    selected_song = song_listbox.get(tk.ACTIVE)  # Get the selected song
    if selected_song:  # Ensure a song is selected
        # Remove the song from both the library and the displayed list
        if selected_song in song_library:
            del song_library[selected_song]  # Remove from library
            displayed_songs.remove(selected_song)  # Remove from displayed list
            update_song_listbox()  # Update the listbox
            save_song_library()  # Save the updated library to JSON
            update_status(f"{selected_song} deleted")
        else:
            update_status("Song not found in library")

# Function to highlight the currently playing song
def highlight_playing_song():
    selected_index = song_listbox.curselection()  # Get the selected song index
    clear_highlight()  # First clear the previous highlights
    if selected_index:  # If there is a selected song
        song_listbox.itemconfig(selected_index, {'bg': '#2edbb9', 'fg': 'black'})  # Highlight the playing song

# Function to clear the highlight from all songs
def clear_highlight():
    for i in range(song_listbox.size()):
        song_listbox.itemconfig(i, {'bg': '#333333', 'fg': 'white'})  # Reset all songs to default style

# Function to check and display the current status of the song
def check_status():
    if mixer.music.get_busy():  # Check if music is playing
        update_status("Playing")
    elif mixer.music.get_pos() == -1:  # Check if music is stopped
        update_status("Stopped")
    else:
        update_status("Paused")
    
    # Re-run this function after 1 second to keep checking the status
    root.after(1000, check_status)

# Function to search and filter songs
def search_song(event=None):
    search_query = search_entry.get().lower()  # Get the search query and make it lowercase
    filtered_songs = [song for song in song_library.keys() if search_query in song.lower()]  # Filter songs based on query
    global displayed_songs
    displayed_songs = filtered_songs  # Update the displayed songs list
    update_song_listbox()  # Update the listbox display

# Function to update the songs in the listbox
def update_song_listbox():
    song_listbox.delete(0, tk.END)  # Clear current listbox items
    for song in displayed_songs:
        song_listbox.insert(tk.END, song)  # Insert the filtered songs into the listbox

# Styling
button_style = {
    "font": ("Helvetica", 12),
    "bg": "#2edbb9",
    "fg": "white",
    "activebackground": "#1d9980",
    "relief": "flat",
    "width": 12,
    "pady": 5
}

label_style = {
    "font": ("Helvetica", 14),
    "bg": "#1e1e1e",
    "fg": "#ffffff",
    "pady": 10
}

# Create GUI elements
song_label = tk.Label(root, text="Select a Song", **label_style)
song_label.pack(pady=10)

# Search bar to filter songs
search_entry = tk.Entry(root, font=("Helvetica", 12), width=30)
search_entry.pack(pady=10)
search_entry.bind("<KeyRelease>", search_song)  # Bind the search function to key releases

# Listbox to display available songs
song_listbox = tk.Listbox(root, bg="#333333", fg="white", font=("Helvetica", 12), selectbackground="#2edbb9", selectforeground="black")
update_song_listbox()  # Initially populate the listbox with all songs
song_listbox.pack(pady=(0, 10), padx=10, fill=tk.X)  # Set top padding to 0

# Placeholder for album artwork (you can later add images)
artwork_placeholder = tk.Label(root, text="Album Art", bg="#1e1e1e", fg="white", font=("Helvetica", 16), width=15, height=5)
artwork_placeholder.pack(pady=10)

# Control buttons
control_frame = tk.Frame(root, bg="#1e1e1e")
control_frame.pack(pady=10)

play_button = tk.Button(control_frame, text="Play", command=play_music, **button_style)
play_button.grid(row=0, column=0, padx=5)

pause_button = tk.Button(control_frame, text="Pause", command=pause_music, **button_style)
pause_button.grid(row=0, column=1, padx=5)

unpause_button = tk.Button(control_frame, text="Unpause", command=unpause_music, **button_style)
unpause_button.grid(row=0, column=2, padx=5)

stop_button = tk.Button(control_frame, text="Stop", command=stop_music, **button_style)
stop_button.grid(row=0, column=3, padx=5)

# Add Song button
add_song_button = tk.Button(root, text="Add Song", command=add_song, **button_style)
add_song_button.pack(pady=10)

# Delete Song button
delete_song_button = tk.Button(root, text="Delete Song", command=delete_song, **button_style)
delete_song_button.pack(pady=10)

# Label to display song status
status_label = tk.Label(root, text="Status: Stopped", **label_style)
status_label.pack(pady=10)

# Call the check_status function to start updating song status
check_status()

# Run the application
root.mainloop()
