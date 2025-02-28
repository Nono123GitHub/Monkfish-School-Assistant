import socket
import threading
import tkinter as tk
import random
import string

# -config
SERVER_IP = '127.0.0.1'
SERVER_PORT = 65432  # port server
STUDENT_PORT = 65433  # port listener

# glob vars
friend_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
username = input("Enter your username: ")

# friends notifications and accepted friends
friend_requests = []
accepted_friends = {}  # mapping friend_code -> button widget
private_chat_windows = {} # Mapping friend_code to chat window
friend_usernames = {}  # Maps friend codes to usernames
reverse_usermap = {}   # Maps usernames back to friend codes

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))
registration_msg = f"REGISTER:{friend_code}:{username}"
client_socket.sendall(registration_msg.encode())

# Wait for confirmation from the server
registration_response = client_socket.recv(1024).decode()
if registration_response.startswith("SERVER: Welcome"):
    print("Registration successful!")
    print(registration_response)  # Print the welcome message
else:
    print(f"Registration failed: {registration_response}")
    # Handle registration failure (e.g., exit the program or retry)

# colors
DARK_GRAY = "#36393f"
LIGHT_GRAY = "#2f3136"
LIGHTER_GRAY = "#40444b"
WHITE = "#ffffff"
BLUE = "#7289da"

root = tk.Tk()
root.title("Monkfish")
root.configure(bg=DARK_GRAY)
root.geometry("720x720")

# main frame (contains sidebar and chat area)
main_frame = tk.Frame(root, bg=DARK_GRAY)
main_frame.pack(fill=tk.BOTH, expand=True)

# left sidebar
sidebar = tk.Frame(main_frame, bg=DARK_GRAY, width=200)
sidebar.pack(side=tk.LEFT, fill=tk.Y)

# user info on sidebar
user_info = tk.Frame(sidebar, bg=DARK_GRAY)
user_info.pack(fill=tk.X, padx=10, pady=10)

label_username = tk.Label(user_info, text=username, bg=DARK_GRAY, fg=WHITE, font=('Arial', 10))
label_username.pack(fill=tk.X)
label_code = tk.Label(user_info, text=f"Your Friend Code: {friend_code}", bg=DARK_GRAY, fg=WHITE, font=('Arial', 10))
label_code.pack(fill=tk.X)

# Frame for sidebar buttons (Friends, Notifications)
sidebar_buttons_frame = tk.Frame(sidebar, bg=DARK_GRAY)
sidebar_buttons_frame.pack(fill=tk.X, padx=10, pady=10, anchor='n')

# Sidebar buttons for Friends and Notifications
fren_but = tk.Button(sidebar_buttons_frame, text="Friends", bg=BLUE, fg=WHITE, command=lambda: friends())
fren_but.pack(fill=tk.X, pady=5)
btn_notifications = tk.Button(sidebar_buttons_frame, text="Notifications", bg=BLUE, fg=WHITE, command=lambda: show_notifications())
btn_notifications.pack(fill=tk.X, pady=5)

# New frame for friend icons (private chats)
friends_icons_frame = tk.Frame(sidebar, bg=DARK_GRAY)
friends_icons_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

def open_private_chat(friend_id):
    if friend_id in private_chat_windows:
        private_chat_windows[friend_id].lift()  # Bring to front if already open
        return

    chat_window = tk.Toplevel(root)
    chat_window.title(f"Chat with {friend_id}")
    chat_window.geometry("700x700")
    chat_window.configure(bg=DARK_GRAY)

    # Chat display area
    chat_display = tk.Text(chat_window, bg=DARK_GRAY, fg='lime green', font=('Lexend', 16), wrap=tk.WORD)
    chat_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    chat_display.insert(tk.END, f"Private chat with {friend_id}\n")
    chat_display.config(state=tk.DISABLED) # Make it read-only

    # Input area
    input_frame_pc = tk.Frame(chat_window, bg=DARK_GRAY)
    input_frame_pc.pack(fill=tk.X, padx=10, pady=(0,10), side = tk.BOTTOM)
    entry_pc = tk.Entry(input_frame_pc, bg=LIGHTER_GRAY, fg=WHITE, font=('Arial', 10))
    entry_pc.pack(side=tk.LEFT, fill=tk.X, expand=True)
    send_pc = tk.Button(input_frame_pc, text="Send", bg=BLUE, fg=WHITE, command=lambda: send_private_message(friend_id, entry_pc, chat_display))
    send_pc.pack(side=tk.RIGHT, padx=(5,0))

    # Store window reference and on close, remove from dict
    private_chat_windows[friend_id] = chat_window
    chat_window.protocol("WM_DELETE_WINDOW", lambda: close_private_chat(friend_id, chat_window))

def close_private_chat(friend_id, chat_window):
    if friend_id in private_chat_windows:
        del private_chat_windows[friend_id]
    chat_window.destroy()

def send_private_message(friend_id, entry_widget, display_widget):
    message = entry_widget.get()
    if message:
        full_message = f"PRIVATE:{friend_code}:{friend_id}:{message}" # includes recipient
        client_socket.sendall(full_message.encode())
        display_widget.config(state=tk.NORMAL)  # Enable editing temporarily
        display_widget.insert(tk.END, f"{username}: {message}\n")
        display_widget.config(state=tk.DISABLED) # Disable editing
        entry_widget.delete(0, tk.END)

def add_friend_icon(friend_id):
    if friend_id in accepted_friends:
        return
    btn = tk.Button(friends_icons_frame, text=friend_id, bg=BLUE, fg=WHITE, command=lambda: open_private_chat(friend_id))
    btn.pack(fill=tk.X, pady=2)
    accepted_friends[friend_id] = btn

# chat area frame
chat_frame = tk.Frame(main_frame, bg=DARK_GRAY)
chat_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# chat messages area with scrollbar
chat_text_frame = tk.Frame(chat_frame, bg=DARK_GRAY)
chat_text_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
chat_list = tk.Text(chat_text_frame, bg=DARK_GRAY, fg='lime green', font=('Lexend', 20), wrap=tk.WORD)
chat_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
chat_list.config(state=tk.DISABLED)  # Make main chat read-only
chat_scroll = tk.Scrollbar(chat_text_frame, command=chat_list.yview)
chat_scroll.pack(side=tk.RIGHT, fill=tk.Y)
chat_list.config(yscrollcommand=chat_scroll.set)
chat_frame.grid_rowconfigure(0, weight=1)
chat_frame.grid_columnconfigure(0, weight=1)

def show_notifications():
    notif_window = tk.Toplevel(root)
    notif_window.title("Friend Requests")
    notif_window.configure(bg=DARK_GRAY)
    notif_frame = tk.Frame(notif_window, bg=DARK_GRAY)
    notif_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    notif_list = tk.Listbox(notif_frame, bg=LIGHTER_GRAY, fg=WHITE, font=('Arial', 10))
    notif_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Scrollbar for notifications listbox
    notif_scroll = tk.Scrollbar(notif_frame, command=notif_list.yview)
    notif_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    notif_list.config(yscrollcommand=notif_scroll.set)

    if friend_requests:
        for req in friend_requests:
            notif_list.insert(tk.END, req)
    else:
        notif_list.insert(tk.END, "No friend requests.")

    close_button = tk.Button(notif_window, text="Close", bg=BLUE, fg=WHITE, command=notif_window.destroy)
    close_button.pack(pady=(0,10))

def receive_messages():
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            if msg:
                print(f"Received: {msg}")

                if "PRIVATE" in msg:
                    parts = msg.split(":")
                    sender_id = parts[1]
                    recipient_id = parts[2] #NEW
                    message_content = parts[3]

                    #check if message is for you
                    if recipient_id == friend_code:

                        if sender_id in private_chat_windows:
                            chat_display = private_chat_windows[sender_id].children['!text'] # Access text widget this way
                            chat_display.config(state=tk.NORMAL)  # Enable editing temporarily
                            chat_display.insert(tk.END, f"{sender_id}: {message_content}\n")
                            chat_display.config(state=tk.DISABLED) # Disable editing
                        else:
                            print(f"Private chat window with {sender_id} not open.")
                            open_private_chat(sender_id) #open chat if not already
                            chat_display = private_chat_windows[sender_id].children['!text'] # Access text widget this way
                            chat_display.config(state=tk.NORMAL)  # Enable editing temporarily
                            chat_display.insert(tk.END, f"{sender_id}: {message_content}\n")
                            chat_display.config(state=tk.DISABLED) # Disable editing

                elif 'accepted your friend request' in msg:
                    add_friend_icon(msg.split("-")[1])
                elif msg.startswith("ACCEPTED_FRIEND"):
                    # Split into 4 components using maxsplit
                    _, user_fc, friend_fc, friend_name = msg.split(":", 3)
    
                    # Update friend mappings
                    friend_usernames[friend_fc] = friend_name
                    reverse_usermap[friend_name] = friend_fc
    
                    # Add to UI
                    add_friend_icon(friend_fc)
    
                    # Update chat display
                    chat_list.config(state=tk.NORMAL)
                    chat_list.insert(tk.END, f"You are now friends with {friend_name} ({friend_fc})\n")
                    chat_list.config(state=tk.DISABLED)
                    chat_list.see(tk.END)


                elif msg.startswith("FRIEND_REQUEST"):
                    print("Added request")
                    friend_requests.append(msg)
                    chat_list.config(state=tk.NORMAL)
                    chat_list.insert(tk.END, f"Friend Request Received: {msg}\n")
                    chat_list.config(state=tk.DISABLED)
                    chat_list.see(tk.END)

                elif msg.startswith("SERVER") and "No pending friend request from this user" in msg:
                    pass #silence message from server

                chat_list.config(state=tk.NORMAL) #Enable editing
                chat_list.insert(tk.END, msg + "\n")
                chat_list.config(state=tk.DISABLED)  # Disable editing
                chat_list.see(tk.END)
            else:
                break
        except Exception as e:
            print("Receive error:", e)
            break

def send_broadcast():
    message = entry_message.get()
    if message:
        full_message = f"BROADCAST:{message}"
        client_socket.sendall(full_message.encode())
        entry_message.delete(0, tk.END)

def friends():
    global entry_target

    fren_window = tk.Toplevel(root)
    fren_window.title("Friends")
    fren_window.configure(bg=DARK_GRAY)

    list_frame = tk.Frame(fren_window, bg=DARK_GRAY)
    list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    notif_list = tk.Listbox(list_frame, bg=LIGHTER_GRAY, fg=WHITE, font=('Arial', 10),
                            selectbackground=BLUE, selectforeground=WHITE)
    notif_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    list_scroll = tk.Scrollbar(list_frame, command=notif_list.yview)
    list_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    notif_list.config(yscrollcommand=list_scroll.set)

    if friend_requests:
        for req in friend_requests:
            notif_list.insert(tk.END, req)
    else:
        notif_list.insert(tk.END, "No friend requests.")

    control_frame = tk.Frame(fren_window, bg=DARK_GRAY)
    control_frame.pack(fill=tk.X, padx=10, pady=10)

    entry_target = tk.Entry(control_frame, bg=LIGHTER_GRAY, fg=WHITE, font=('Arial', 10))
    entry_target.insert(0, "Target Friend Code")
    entry_target.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=30)

    accept_friend_button = tk.Button(control_frame, text="Accept Friend", bg=BLUE, fg=WHITE,
                                    command=lambda: (accept_friend_request(),
                                                     add_friend_icon(entry_target.get().strip()))) #added target and other function call.
    accept_friend_button.pack(side=tk.RIGHT, padx=(10, 0))

    add_friend_button = tk.Button(control_frame, text="Add Friend", bg=BLUE, fg=WHITE,
                                 command=send_friend_request)
    add_friend_button.pack(side=tk.RIGHT, padx=(10, 0))

    close_button = tk.Button(control_frame, text="Close", bg=BLUE, fg=WHITE, command=fren_window.destroy)
    close_button.pack(side=tk.RIGHT, padx=(10, 0))

def send_private():
    target = entry_target.get().strip()
    message = entry_message.get()
    if target and message:
        full_message = f"PRIVATE:{friend_code}:{target}:{message}"
        client_socket.sendall(full_message.encode())
        entry_message.delete(0, tk.END)

def send_friend_request():
    target = entry_target.get().strip()
    if target:
        request_msg = f"FRIEND_REQUEST:{friend_code}:{target}"
        client_socket.sendall(request_msg.encode())
        chat_list.config(state=tk.NORMAL)
        chat_list.insert(tk.END, f"Friend Request Sent to: {target}\n")
        chat_list.config(state=tk.DISABLED)
        chat_list.see(tk.END)

def accept_friend_request():
    target = entry_target.get().strip()
    if target:
        accept_msg = f"FRIEND_ACCEPT:{friend_code}:{target}"
        client_socket.sendall(accept_msg.encode())
        chat_list.config(state=tk.NORMAL)
        chat_list.insert(tk.END, f"Accepting Friend Request from: {target}\n")
        chat_list.config(state=tk.DISABLED)
        chat_list.see(tk.END)

def friend_request_listener():
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(('', STUDENT_PORT))
    listener.listen(5)
    print(f"Friend Request Listener started on port {STUDENT_PORT}")
    while True:
        try:
            conn, addr = listener.accept()
            data = conn.recv(1024).decode()
            if data:
                friend_requests.append(data)
                chat_list.config(state=tk.NORMAL)
                chat_list.insert(tk.END, f"Friend Request Received: {data}\n")
                chat_list.config(state=tk.DISABLED)
                chat_list.see(tk.END)
            conn.close()
        except Exception as e:
            print("Friend request listener error:", e)
            break

# input area for messages
input_frame = tk.Frame(chat_frame, bg=DARK_GRAY)
input_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0,10))
entry_message = tk.Entry(input_frame, bg=LIGHTER_GRAY, fg=WHITE, font=('Arial', 10))
entry_message.pack(side=tk.LEFT, fill=tk.X, expand=True)
send_button = tk.Button(input_frame, text="Send", bg=BLUE, fg=WHITE, command=lambda: send_broadcast())
send_button.pack(side=tk.RIGHT, padx=(5,0))

# button frame below the input area for additional options
button_frame = tk.Frame(chat_frame, bg=DARK_GRAY)
button_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
btn_broadcast = tk.Button(button_frame, text="Send Broadcast", bg=BLUE, fg=WHITE, command=send_broadcast)
btn_broadcast.pack(side=tk.LEFT, padx=2)
btn_private = tk.Button(button_frame, text="Send Private", bg=BLUE, fg=WHITE, command=lambda: send_private())
btn_private.pack(side=tk.LEFT, padx=2)

# Start threads for receiving messages and friend requests
threading.Thread(target=receive_messages, daemon=True).start()
threading.Thread(target=friend_request_listener, daemon=True).start()

root.mainloop()
