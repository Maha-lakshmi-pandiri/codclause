import os
import tkinter as tk
from tkinter import filedialog
import vlc
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from PIL import Image, ImageTk
import io

# VLC player instance
instance = vlc.Instance()
player = instance.media_player_new()

# Globals
playlist = []
current_index = 0
duration = 0
is_playing = False
is_slider_dragging = False

def select_folder():
    global playlist, current_index
    folder = filedialog.askdirectory()
    if folder:
        playlist.clear()
        for file in os.listdir(folder):
            if file.endswith(".mp3") or file.endswith(".wav"):
                playlist.append(os.path.join(folder, file))
        current_index = 0
        if playlist:
            load_song(playlist[current_index])

def load_song(path):
    global duration
    media = instance.media_new(path)
    player.set_media(media)
    player.play()

    # Wait for duration to load
    root.after(500, lambda: update_duration(path))

    # Album art
    try:
        audio = MP3(path, ID3=ID3)
        for tag in audio.tags.values():
            if isinstance(tag, APIC):
                img_data = tag.data
                image = Image.open(io.BytesIO(img_data))
                image = image.resize((150, 150))
                photo = ImageTk.PhotoImage(image)
                album_art_label.config(image=photo)
                album_art_label.image = photo
                break
        else:
            album_art_label.config(image='', text="No Album Art")
    except:
        album_art_label.config(image='', text="No Album Art")

def update_duration(path):
    global duration
    duration = player.get_length() // 1000
    if duration > 0:
        progress_bar.config(to=duration)
        update_progress()

def play_music():
    global is_playing
    player.play()
    is_playing = True

def pause_music():
    player.pause()

def stop_music():
    global is_playing
    player.stop()
    is_playing = False
    progress_bar.set(0)

def next_song():
    global current_index
    if playlist:
        current_index = (current_index + 1) % len(playlist)
        load_song(playlist[current_index])

def prev_song():
    global current_index
    if playlist:
        current_index = (current_index - 1) % len(playlist)
        load_song(playlist[current_index])

def seek_music(val):
    global is_slider_dragging
    if not is_slider_dragging:
        player.set_time(int(float(val)) * 1000)

def update_progress():
    if is_playing and not is_slider_dragging:
        current_time = player.get_time() // 1000
        progress_bar.set(current_time)
    root.after(1000, update_progress)

def on_slider_press(event):
    global is_slider_dragging
    is_slider_dragging = True

def on_slider_release(event):
    global is_slider_dragging
    is_slider_dragging = False
    seek_music(progress_bar.get())

# GUI setup
root = tk.Tk()
root.title("Music Player with Seek (VLC)")
root.geometry("320x480")

album_art_label = tk.Label(root, text="No Album Art")
album_art_label.pack(pady=10)

progress_bar = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, length=280,
                        showvalue=True, command=seek_music)
progress_bar.pack(pady=10)
progress_bar.bind("<ButtonPress-1>", on_slider_press)
progress_bar.bind("<ButtonRelease-1>", on_slider_release)

tk.Button(root, text="Select Folder", command=select_folder).pack(pady=10)
tk.Button(root, text="Play", command=play_music).pack(pady=5)
tk.Button(root, text="Pause", command=pause_music).pack(pady=5)
tk.Button(root, text="Stop", command=stop_music).pack(pady=5)
tk.Button(root, text="Next", command=next_song).pack(pady=5)
tk.Button(root, text="Previous", command=prev_song).pack(pady=5)

root.mainloop()
