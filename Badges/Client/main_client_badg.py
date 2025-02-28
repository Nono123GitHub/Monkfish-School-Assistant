import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import socket
from io import BytesIO
import threading

SERVER_IP = "127.0.0.1"
SERVER_PORT = 65432
STUDENT_PORT = 65433

def add_images(frame, canvas, image):
    label = tk.Label(frame, image=image)
    label.image = image  # Keep a reference to prevent garbage collection
    label.pack(pady=5)
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

root = tk.Tk()
root.title('Student Badge Display')
root.geometry("720x720")
root.configure(bg="powder blue")
canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.config(yscrollcommand=scrollbar.set)

frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="nw")
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")



STUDENT_NAME = "Noah Sheikh"

header = tk.Label(
    root,
    text=f"Student Badge Display:\n{STUDENT_NAME}",
    font=("Arial", 16, "bold"),
    bg="powder blue"
)
header.pack(pady=20)

badge_frame = tk.Frame(root, bg="powder blue")
badge_frame.pack(pady=20)

badge_label = tk.Label(
    badge_frame,
    text="Waiting for badges...",
    font=("Arial", 12),
    bg="powder blue"
)
badge_label.pack()

def display_badge(image_data):
    try:
        image = Image.open(BytesIO(image_data))
        image = image.resize((200, 200), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        
        badge_display = tk.Label(badge_frame,image=photo,bg="powder blue")
        badge_display.image = photo
        badge_label.pack_forget()
        add_images(frame, canvas, photo)

    except:
        pass

def start_listener():
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind((SERVER_IP, STUDENT_PORT))
    listener.listen(1)
    
    while True:
        try:
            conn, addr = listener.accept()
            data = conn.recv(1024)
            image_data = b""
            
            while data:
                image_data += data
                data = conn.recv(1024)
                
            if image_data:
                root.after(0, display_badge, image_data)
        except:
            pass
        finally:
            conn.close()

def register_client():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_IP, SERVER_PORT))
            message = f"REGISTER:{STUDENT_NAME}"
            s.sendall(message.encode('utf-8'))
    except:
        pass

register_client()
threading.Thread(target=start_listener, daemon=True).start()
root.mainloop()