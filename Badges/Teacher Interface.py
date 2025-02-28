import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import socket
from pathlib import Path
import os

SERVER_IP = "127.0.0.1"
SERVER_PORT = 65432

root = tk.Tk()
root.title("Teacher Badge Sender")
root.geometry("700x700")
root.configure(bg="powder blue")

header = tk.Label(
    root,
    text="Teacher Badge Control Panel",
    font=("Arial", 16, "bold"),
    bg="powder blue"
)
header.pack(pady=20)

student_frame = tk.Frame(root, bg="powder blue")
student_frame.pack(pady=20)

tk.Label(
    student_frame,
    text="Student Name:",
    font=("Arial", 24),
    bg="powder blue"
).pack(side=tk.LEFT, padx=5)

initials_entry = ttk.Entry(
    student_frame,
    font=("Arial", 12),
    width=10
)
initials_entry.pack(side=tk.LEFT, padx=5)

status_label = tk.Label(
    root,
    text="Ready to send badges",
    font=("Arial", 20),
    bg="powder blue"
)
status_label.pack(pady=20)

def send_badge(badge_path, initials):
    try:
        with open(badge_path, "rb") as f:
            image_data = f.read()
            
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_IP, SERVER_PORT))
            s.sendall(f"{initials}:".encode('utf-8') + image_data)
            
        status_label.config(
            text=f"Badge sent to {initials}",
            fg="green"
        )
    except Exception as e:
        status_label.config(
            text=f"Error sending badge",
            fg="red"
        )

def select_badge(badge_name):
    initials = initials_entry.get().strip()
    if not initials:
        status_label.config(text="Please enter student initials", fg="red")
        return
        
    image_path = Path(__file__).with_name(badge_name)
    if image_path.exists():
        send_badge(image_path, initials)
    else:
        status_label.config(text=f"Badge file not found", fg="red")

def select_custom_badge():
    file_path = filedialog.askopenfilename(
        title="Select Badge Image",
        filetypes=[
            ("Image Files", "*.png *.jpg *.jpeg *.gif"),
            ("All Files", "*.*")
        ]
    )
    
    if file_path:
        initials = initials_entry.get().strip()
        if not initials:
            status_label.config(text="Please enter student name", fg="red")
            return
            
        send_badge(file_path, initials)

badge_frame = tk.Frame(root, bg="powder blue")
badge_frame.pack(pady=20)

tk.Label(
    badge_frame,
    text="Select Badge:",
    font=("Arial", 14),
    bg="powder blue"
).pack(pady=10)

badges = ["sport", "effort", "kind"]
for badge in badges:
    ttk.Button(badge_frame, text=f"{badge.title()} Badge", command=lambda b=badge: select_badge(f"{b}.png")).pack(pady=5, ipadx=40, ipady=20)

ttk.Button(badge_frame,text="Custom Badge",command=select_custom_badge).pack(pady=5,ipadx=35, ipady=20)

root.mainloop()