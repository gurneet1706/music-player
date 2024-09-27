import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import *
import pygame
import os
from PIL import Image, ImageTk

root = Tk()
root.title("Music Player")
window_width = 380
window_height = 350

# get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

# set the position of the window to the center of the screen
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

root.iconbitmap("logo.ico")

pygame.mixer.init()

menuBar = Menu(root)
root.config(menu = menuBar)

songs = []
current_song = ""
paused = False
song_length = 0
current_time = 0


# Load and display the default image
def load_default_image():
    global default_image
    image = Image.open("default.png")
    image = image.resize((200, 200), Image.LANCZOS)  # Resize if needed
    default_image = ImageTk.PhotoImage(image)
    icon_label.config(image=default_image)

def adjust_volume(value):
    pygame.mixer.music.set_volume(float(value) / 100.0)

def load_music():
    global current_song
    root.directory = filedialog.askdirectory()
    songs.clear()
    songList.delete(0, END)  # Clear the existing list
    for song in os.listdir(root.directory):
        name, ext = os.path.splitext(song)
        if ext == ".mp3":
            songs.append(song)
    for song in songs:
        songList.insert("end", song)
    songList.selection_set(0)
    current_song = songs[songList.curselection()[0]]

def play_music():
    global current_song, paused, song_length, current_time
    if not paused:
        song = pygame.mixer.Sound(os.path.join(root.directory, current_song))
        song_length = song.get_length()
        pygame.mixer.music.load(os.path.join(root.directory, current_song))
        pygame.mixer.music.play()
        update_progress_bar()
        # Update icon image for the currently playing song
        # (Assuming you have a way to get an image for each song)
    else:
        pygame.mixer.music.unpause()
        paused = False

def pause_music():
    global paused
    pygame.mixer.music.pause()
    paused = True

def next_music():
    global current_song, paused
    try:
        songList.selection_clear(0, END)
        songList.selection_set(songs.index(current_song) + 1)
        current_song = songs[songList.curselection()[0]]
        play_music()
    except:
        pass

def prev_music():
    global current_song, paused
    try:
        songList.selection_clear(0, END)
        songList.selection_set(songs.index(current_song) - 1)
        current_song = songs[songList.curselection()[0]]
        play_music()
    except:
        pass
def update_progress_bar():
    global current_time, song_length
    current_time = pygame.mixer.music.get_pos() / 1000  # Get the current time in seconds
    progress_bar['value'] = (current_time / song_length) * 100
    progress_bar.after(1000, update_progress_bar)  # Update the progress bar every second


organise_menu = Menu(menuBar)
organise_menu.add_command(label = "Select Folder", command = load_music)
menuBar.add_cascade(label = "Organise", menu = organise_menu)

# Create a PanedWindow
paned_window = PanedWindow(root)
paned_window.pack(fill=BOTH, expand=1)

# Create frames for the PanedWindow
list_frame = Frame(paned_window, bg="light blue")
icon_frame = Frame(paned_window, bg="Black")
top_frame = Frame(paned_window)
bottom_frame = Frame(paned_window)
# Add frames to the PanedWindow
paned_window.add(list_frame, width=200)
paned_window.add(icon_frame)
paned_window.add(top_frame)

# Listbox for songs
songList = Listbox(list_frame, bg = "black", fg = "white", width = 40, height = 15)
songList.pack(padx=10, pady=10)

# Default icon
default_image = None
icon_label = Label(icon_frame, bg="gray")
icon_label.pack(padx=10, pady=10)
# Progress bar
progress_bar = ttk.Progressbar(icon_frame, mode='determinate', maximum = 100)
progress_bar.pack(fill = 'x', padx=10, pady=10)
# Load the default image
load_default_image()

# Control buttons
play_btn_image = PhotoImage(file = "Play.png")
pause_btn_image = PhotoImage(file = "Pause.png")
next_btn_image = PhotoImage(file = "Right.png")
prev_btn_image = PhotoImage(file = "Left.png")

control_frame = Frame(root)
control_frame.pack(side=BOTTOM, fill=X)

play_btn = Button(control_frame, image = play_btn_image, borderwidth = 0, command = play_music)
pause_btn = Button(control_frame, image = pause_btn_image, borderwidth = 0, command = pause_music)
next_btn = Button(control_frame, image = next_btn_image, borderwidth = 0, command = next_music)
prev_btn = Button(control_frame, image = prev_btn_image, borderwidth = 0, command = prev_music)
volume_scale = tk.Scale(control_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=adjust_volume, bg="white",
fg="light gray",troughcolor="#2e2e2e", sliderlength=20, width=10)
play_btn.grid(row = 0, column = 4, padx = 7, pady = 10)
pause_btn.grid(row = 0, column = 5, padx = 7, pady = 10)
next_btn.grid(row = 0, column = 6, padx = 7, pady = 10)
prev_btn.grid(row = 0, column = 3, padx = 7, pady = 10)
volume_scale.grid(row = 0, column = 7, padx = 7, pady = 10)
root.mainloop()
