import tkinter as tk
from tkinter import filedialog, ttk
import socket
from pathlib import Path

SERVER_IP = "192.168.52.244"
SERVER_PORT = 65432

root = tk.Tk()
root.title("Teacher Badge Sender")
root.geometry("700x700")
root.configure(bg="powder blue")

header = tk.Label(root, text="Teacher Badge Control Panel", font=("Arial", 16, "bold"), bg="powder blue")
header.pack(pady=20)

student_frame = tk.Frame(root, bg="powder blue")
student_frame.pack(pady=20)

tk.Label(student_frame, text="Student Initials:", font=("Arial", 12), bg="powder blue").pack(side=tk.LEFT, padx=5)
initials_entry = ttk.Entry(student_frame, font=("Arial", 12), width=10)
initials_entry.pack(side=tk.LEFT, padx=5)

status_label = tk.Label(root, text="Ready to send badges", font=("Arial", 12), bg="powder blue")
status_label.pack(pady=20)

def send_badge(badge_path, initials):
     try:
         with open(badge_path, "rb") as f:
             image_data = f.read()

         print(f"Sending {len(image_data)} bytes to {initials}")  #


         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
             s.connect((SERVER_IP, SERVER_PORT))

             # Send student initials first (fixed size 50 bytes, paddedwith spaces)
             padded_initials = initials.ljust(50).encode()  # Ensure it's always 50 bytes
             s.sendall(padded_initials)

             # Send the image binary data
             s.sendall(image_data)

         status_label.config(text=f"Badge sent to {initials}", fg="green")

     except Exception as e:
         status_label.config(text=f"Error sending badge: {str(e)}",
fg="red")

def select_badge(badge_file_path):
    initials = initials_entry.get().strip()
    if not initials:
        status_label.config(text="Please enter student initials", fg="red")
        return
    image_path = Path(badge_file_path)
    if image_path.exists():
        send_badge(str(image_path), initials)
    else:
        status_label.config(text="Badge file not found", fg="red")

def select_custom_badge():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif"), ("All Files", "*.*")])
    if file_path:
        initials = initials_entry.get().strip()
        if not initials:
            status_label.config(text="Please enter student initials", fg="red")
            return
        send_badge(file_path, initials)

# Create two lists: one for labels and one for image file paths
badge_labels = ["Water Polo King", "10 Points", "Peace Badge"]
badge_file_paths = ["C:\\Users\\nshei\\Downloads\\client\\water polo king-poke-card.png", "C:\\Users\\nshei\\Downloads\\client\\10 points-poke-card.png", "C:\\Users\\nshei\\Downloads\\client\\peacemaker-poke-card.png"]

badge_frame = tk.Frame(root, bg="powder blue")
badge_frame.pack(pady=20)

tk.Label(badge_frame, text="Select Badge:", font=("Arial", 14), bg="powder blue").pack(pady=10)

# Loop over both lists together to create buttons for each badge
for label, path in zip(badge_labels, badge_file_paths):
    # Using a default argument in the lambda to capture the current 'path'
    ttk.Button(badge_frame, text=label, command=lambda p=path: select_badge(p)).pack(pady=5)

# Button for a custom badge that lets the user select a file
ttk.Button(badge_frame, text="Custom Badge", command=select_custom_badge).pack(pady=5)

root.mainloop()
