import time
import itertools
import tkinter as tk
from tkinter import messagebox
from playsound import playsound
import threading
import pygame 
import sys
import os
from tkinter import messagebox, filedialog, ttk
from PIL import Image, ImageTk 
import cv2
import chardet  
from playsound import playsound # type: ignore

pygame.init()

def exit_program():
    root.quit()

def get_resource_path(filename):
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.dirname(__file__), filename)

sound = get_resource_path('passreddead.mp3')

def play_sound(sound):
    playsound(sound)

def dead(ehe):
    sound_thread = threading.Thread(target=play_sound, args=(sound,))
    sound_thread.start()

def play_video():
    global video
    video = cv2.VideoCapture(get_resource_path('passredvideo.mp4'))
    toggle_fullscreen()

    def video_loop():
        while True:
            ret, frame = video.read()
            if not ret:
                video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = ImageTk.PhotoImage(img)

            video_label.config(image=img)
            video_label.image = img

            root.update_idletasks()
            root.after(10)

        video.release()

    threading.Thread(target=video_loop, daemon=True).start()


def toggle_fullscreen(event=None):
    global fullscreen
    fullscreen = True
    root.attributes("-fullscreen", fullscreen)
    root.attributes("-topmost", False)
    video_label.place(relwidth=1.0, relheight=1.0)

def end_fullscreen(event=None):
    global fullscreen
    fullscreen = False
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 1500
    window_height = 900
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    root.attributes("-fullscreen", False)
    root.attributes("-topmost", False)
    video_label.place(relx=0.5, rely=0.5, anchor="center")


def brute_force_attack(user_pass, char_set, length, result_label, attempts_label, speed_label):
    start_time = time.time()
    attempts = 0

    for guess in itertools.product(char_set, repeat=length):
        guess_str = ''.join(guess)
        attempts += 1

        if guess_str == user_pass:
            elapsed_time = time.time() - start_time
            attempts_per_second = attempts / elapsed_time
            result_label.config(text=f"Şifre bulundu: {guess_str}")
            attempts_label.config(text=f"Denemeler: {attempts}")
            speed_label.config(text=f"Saniye başına deneme sayısı: {attempts_per_second:.2f}")
            return guess_str
        
        if attempts % 5000 == 0:
            elapsed_time = time.time() - start_time
            attempts_per_second = attempts / elapsed_time
            result_label.config(text=f"Deneme: {guess_str}")
            attempts_label.config(text=f"Denemeler: {attempts}")
            speed_label.config(text=f"Saniye başına deneme sayısı: {attempts_per_second:.2f}")
            root.update()  

def start_attack():
    user_pass = entry.get()
    password = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']  
    char_set = ''.join(password)
    length = len(user_pass)
    result_label.config(text="Deneme başlıyor...")
    attempts_label.config(text="Deneme sayısı: 0")
    speed_label.config(text="Saniye başına deneme sayısı: 0.00")
    root.update()  
    brute_force_attack(user_pass, char_set, length, result_label, attempts_label, speed_label)


root = tk.Tk()
root.title("passred")
fullscreen = False
root.configure(bg='black')  

video_label = tk.Label(root)
video_label.place(relx=0.5, rely=0.5, anchor="center")

style = ttk.Style()
style.configure("TLabel", foreground='white', background='black', font=("Helvetica", 36))
style.configure("TButton", foreground='black', background='lime', font=("Helvetica", 36), padding=(20, 10))
style.configure("TEntry", foreground='black', font=("Helvetica", 42), padding=(20, 10))

title_label = ttk.Label(root, text="Şifre Kırma Aracı", style="TLabel", font=("Helvetica", 48))
title_label.place(relx=0.5, rely=0.05, anchor="center")

entry_label = ttk.Label(root, text="Şifreyi girin:", style="TLabel")
entry_label.place(relx=0.5, rely=0.25, anchor="center")

entry = ttk.Entry(root, width=20, style="TEntry")
entry.place(relx=0.5, rely=0.4, anchor="center")

start_button = ttk.Button(root, text="Denemeye Başla", command=start_attack, style="TButton")
start_button.place(relx=0.5, rely=0.55, anchor="center")

exit_button = ttk.Button(root, text="Çıkış", command=exit_program, style="TButton")
exit_button.place(relx=0.5, rely=0.7, anchor="center")

result_label = ttk.Label(root, text="", style="TLabel")
result_label.place(relx=0.5, rely=0.85, anchor="center")

attempts_label = ttk.Label(root, text="", style="TLabel")
attempts_label.place(relx=0.5, rely=0.9, anchor="center")

speed_label = ttk.Label(root, text="", style="TLabel")
speed_label.place(relx=0.5, rely=0.95, anchor="center")

play_video()

root.bind("<Escape>", end_fullscreen)
root.bind("<F11>", toggle_fullscreen)
root.bind("<r>", dead)

root.mainloop()
