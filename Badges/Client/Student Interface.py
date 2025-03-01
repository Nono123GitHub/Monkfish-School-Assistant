import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import socket
from io import BytesIO
import threading

SERVER_IP = "192.168.52.244"
STUDENT_PORT = 65433
STUDENT_NAME = "Noah"  # Change to student's actual initials

# Global list to store PhotoImage objects
badge_images = []

def display_badge(image_data):
    try:
        # Convert image data to a PIL Image
        image = Image.open(BytesIO(image_data))
        image.thumbnail((200, 200), Image.LANCZOS)  # Resize to fit list
        
        # Convert to Tkinter-compatible PhotoImage
        photo = ImageTk.PhotoImage(image)
        badge_images.append(photo)  # Store the image
        
        # Create a button with the image and add it to the frame
        img_button = tk.Button(scrollable_frame, image=photo, command=lambda img=image: enlarge_image(img), relief="flat")
        img_button.pack(pady=5)
        
        # Update canvas scroll region
        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    except Exception as e:
        print("Error displaying badge:", e)

def enlarge_image(image):
    """Displays the selected image in full size in a separate window."""
    top = tk.Toplevel(root)
    top.title("Enlarged Badge")
    
    # Resize image to be larger for better visibility
    image = image.resize((600, 800), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    
    label = tk.Label(top, image=photo)
    label.image = photo  # Keep reference
    label.pack(padx=10, pady=10)

def start_listener():
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.connect((SERVER_IP, STUDENT_PORT))
    listener.send(STUDENT_NAME.encode())  # Send student name to server

    print("Waiting for badge...")  # Debugging log ////////////////////////////////////////#///#///////////////////

    image_data = b""
    while True:
        try:
            data = listener.recv(4096)  # Receive image in chunks
            if not data:  # Exit loop when no more data is received
                break
            image_data += data
            print(f"Received {len(data)} bytes (Total so far: {len(image_data)} bytes)")
        except Exception as e:
            print("Error receiving image:", e)
            break

    listener.close()
    print(f"✅ Total image size received: {len(image_data)} bytes")
    if image_data:
        root.after(0, display_badge, image_data)
    else:
        print("❌ No image received!")

# Initialize GUI
DARK_GRAY = "#36393f"
root = tk.Tk()
root.title("Noah's badges")
root.geometry("720x720")
root.configure(bg=DARK_GRAY)

# Create a frame for scrolling images
container = tk.Frame(root)
canvas = tk.Canvas(container, bg="dim gray")
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)

scrollable_frame = tk.Frame(canvas, bg="dim gray")
scrollable_frame.bind("<Configure>", lambda e: canvas.config(scrollregion=canvas.bbox("all")))

# Embed the frame in the canvas
window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Pack the elements to fill the majority of the screen
container.pack(fill=tk.BOTH, expand=True)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Start the listener thread to receive images
threading.Thread(target=start_listener, daemon=True).start()

root.mainloop()
