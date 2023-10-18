import tkinter
from tkinter.filedialog import askdirectory
import os
import pygame

player = tkinter.Tk()
player.title("Music Player")

# Set initial music directory
directory = askdirectory()
if not directory:
    print("No directory selected.")
    player.destroy()
    exit()
os.chdir(directory)

# Create music list and check for valid audio files
songlist = [filename for filename in os.listdir(directory) if filename.endswith(".mp3")]
if len(songlist) == 0:
    print("No playable audio files found.")
    player.destroy()
    exit()

# Set up player GUI
player.geometry("310x355")
player.configure(bg="#202020")
player.option_add("*Font", "Helvetica 12")  # Set the default font for the application

var = tkinter.StringVar()
var.set("Select the song to play")
text = tkinter.Label(player, font=("Helvetica", 16, "bold"), textvariable=var, fg="white", bg="#202020")
text.grid(row=0, columnspan=6, pady=10)

playing = tkinter.Listbox(player, font=("Helvetica", 12), width=28, bg="black", fg="white", selectbackground="#FF4081", selectforeground="white", selectmode=tkinter.SINGLE)
for item in songlist:
    playing.insert(tkinter.END, item)
playing.grid(row=1, columnspan=6, pady=10)

# Set up pygame mixer for audio playback
pygame.init()
pygame.mixer.init()

# Define audio control functions
def play():
    try:
        selected = playing.get(tkinter.ACTIVE)
        pygame.mixer.music.load(selected)
        name = selected
        var.set(f"{name[:16]}..." if len(name) > 18 else name)
        pygame.mixer.music.play()
    except pygame.error:
        print("Error playing audio.")

def pause():
    pygame.mixer.music.pause()

def resume():
    pygame.mixer.music.unpause()

def next_song():
    current_index = playing.curselection()
    if current_index:
        next_index = (current_index[0] + 1) % playing.size()
        playing.selection_clear(0, tkinter.END)
        playing.selection_set(next_index)
        play()

def previous_song():
    current_index = playing.curselection()
    if current_index:
        previous_index = (current_index[0] - 1) % playing.size()
        playing.selection_clear(0, tkinter.END)
        playing.selection_set(previous_index)
        play()

def set_volume(volume):
    pygame.mixer.music.set_volume(float(volume) / 100)

def repeat_song():
    pygame.mixer.music.play(loops=-1)  # Set loops to -1 for infinite repetition

# Add player control buttons
playB = tkinter.Button(player, width=8, height=2, font=("Helvetica", 12, "bold"), text="Play", command=play, bg="#FF4081", fg="white")
playB.grid(row=2, column=0, pady=5)
pauseB = tkinter.Button(player, width=8, height=2, font=("Helvetica", 12, "bold"), text="Pause", command=pause, bg="#2962FF", fg="white")
pauseB.grid(row=2, column=1, pady=5)
resumeB = tkinter.Button(player, width=8, height=2, font=("Helvetica", 12, "bold"), text="Resume", command=resume, bg="#00C853", fg="white")
resumeB.grid(row=2, column=2, pady=5)
previousB = tkinter.Button(player, width=8, height=2, font=("Helvetica", 12, "bold"), text="Previous", command=previous_song, bg="#FFD600", fg="black")
previousB.grid(row=2, column=3, pady=5)
repeatB = tkinter.Button(player, width=8, height=2, font=("Helvetica", 12, "bold"), text="Repeat", command=repeat_song, bg="#FF8F00", fg="white")
repeatB.grid(row=2, column=4, pady=5)
nextB = tkinter.Button(player, width=8, height=2, font=("Helvetica", 12, "bold"), text="Next", command=next_song, bg="#FFD600", fg="black")
nextB.grid(row=2, column=5, pady=5)

# Volume control
volume_label = tkinter.Label(player, text="Volume", font=("Helvetica", 12, "bold"), fg="white", bg="#202020")
volume_label.grid(row=3, column=0, pady=5, sticky=tkinter.E)
volume_scale = tkinter.Scale(player, from_=0, to=100, orient=tkinter.HORIZONTAL, command=set_volume, bg="#FF4081", fg="white", highlightbackground="#FF4081")
volume_scale.set(50)  # Set initial volume to 50%
volume_scale.grid(row=3, column=1, columnspan=6, pady=5, padx=5, sticky=tkinter.W+tkinter.E)

player.mainloop()