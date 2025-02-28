import socket
import threading
from better_profanity import profanity
from datetime import datetime, time

# Global dictionaries
clients = {}
client_names = {}
friend_requests = {}
friends = {}
lock = threading.Lock()
profanity.load_censor_words()
SERVER_IP = '0.0.0.0'
SERVER_PORT = 65432
STUDENT_PORT = 65433
lesson_intervals = [
    (time(8, 45), time(9, 40)),
    (time(10, 55), time(11, 50)),
    (time(13, 40), time(14, 35)),
]

def is_lesson_time(current_time):
    for start, end in lesson_intervals:
        if start <= current_time < end:
            return True
    return False

def broadcast_message(message):
    """Send a message to all connected clients except the sender."""
    with lock:
        for code, (conn, addr) in clients.items():
            try:
                conn.sendall(message.encode())
            except Exception as e:
                print(f"Broadcast error to {code}: {e}")

def handle_client(conn, addr):
    friend_code = None
    try:
        # Registration
        data = conn.recv(1024).decode()
        if data.startswith("REGISTER:"):
            parts = data.split(":", 2)
            if len(parts) < 3:
                conn.sendall("SERVER: Invalid registration format.".encode())
                conn.close()
                return
            friend_code = parts[1].strip()
            username = parts[2].strip()
            with lock:
                clients[friend_code] = (conn, addr)
                client_names[friend_code] = username
                print(f"Registered {username} with code {friend_code} from {addr}")
                conn.sendall(f"SERVER: Welcome, {username}! Your friend code is {friend_code}".encode())
        else:
            conn.close()
            return

        # Main loop
        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode()
            print(profanity.censor(f"From {addr} ({friend_code}): {message}"))

            if message.startswith("BROADCAST:"):
                _, text = message.split(":", 1)
                full_message = f"{client_names[friend_code]} (Broadcast): {text}"
                now = datetime.now().time()
                if is_lesson_time(now):
                    broadcast_message("SERVER: Lesson time! All chats are now off until lessons end.")
                else:
                    broadcast_message(full_message)
            elif message.startswith("PRIVATE:"):
                parts = message.split(":", 3)  # Split into 4 parts
                if len(parts) < 4:
                    conn.sendall("SERVER: Incorrect private message format.".encode())
                    continue
                _, sender_code, target_code, text = parts
                sender_code = sender_code.strip()
                target_code = target_code.strip()
                with lock:
                    if target_code in clients:
                        target_conn, _ = clients[target_code]
                        send_text = profanity.censor(f"PRIVATE:{sender_code}:{target_code}:{text}")
                        notext = "SERVER: Lesson time! All chats are now off until lessons end."
                        try:
                            now = datetime.now().time()
                            now = time(6,45)
                            if is_lesson_time(now):
                                target_conn.sendall(notext.encode())
                            else:
                                target_conn.sendall(send_text.encode())
                            print(f"Sent private message from {client_names[sender_code]} to {client_names[target_code]}")
                        except Exception as e:
                            print("Error sending private message:", e)
                            conn.sendall("SERVER: Failed to deliver private message.".encode())
                    else:
                        conn.sendall("SERVER: User not found.".encode())
            elif message.startswith("FRIEND_REQUEST:"):
                parts = message.split(":", 2)
                if len(parts) < 3:
                    conn.sendall("SERVER: Invalid friend request format.".encode())
                    continue
                _, sender_code, target_code = parts
                sender_code = sender_code.strip()
                target_code = target_code.strip()
                with lock:
                    if target_code in clients:
                        target_conn, _ = clients[target_code]
                        friend_req_message = f"FRIEND_REQUEST:{sender_code}:{client_names[sender_code]}"
                        try:
                            target_conn.sendall(friend_req_message.encode())
                            print(f"Sent friend request from {sender_code} to {target_code}")
                            if target_code not in friend_requests:
                                friend_requests[target_code] = set()
                            friend_requests[target_code].add(sender_code)
                            conn.sendall(f"SERVER: Friend request sent to {client_names[target_code]}".encode())
                        except Exception as e:
                            print(f"Error sending friend request: {e}")
                            conn.sendall("SERVER: Failed to send friend request.".encode())
                    else:
                        conn.sendall("SERVER: Friend code not found.".encode())
            elif message.startswith("FRIEND_ACCEPT:"):
                parts = message.split(":", 2)
                if len(parts) < 3:
                    conn.sendall("SERVER: Invalid friend accept format.".encode())
                    continue
                _, accepter_code, requester_code = parts
                accepter_code = accepter_code.strip()
                requester_code = requester_code.strip()
                print(f"{accepter_code} is trying to accept friend request from {requester_code}")
                with lock:
                    if accepter_code in friend_requests and requester_code in friend_requests[accepter_code]:
                        if requester_code in clients:
                            requester_conn, _ = clients[requester_code]
                            accept_message = f"ACCEPTED_FRIEND:{accepter_code}:{client_names[accepter_code]}"
                            try:
                                requester_conn.sendall(accept_message.encode())
                                conn.sendall(f"SERVER: You are now friends with {client_names[requester_code]}".encode())
                                print(f"Friend request accepted: {accepter_code} and {requester_code} are now friends")
                                if accepter_code not in friends:
                                    friends[accepter_code] = set()
                                if requester_code not in friends:
                                    friends[requester_code] = set()
                                friends[accepter_code].add(requester_code)
                                friends[requester_code].add(accepter_code)
                                friend_requests[accepter_code].remove(requester_code)
                                if not friend_requests[accepter_code]:
                                    del friend_requests[accepter_code]
                            except Exception as e:
                                print(f"Error sending friend acceptance: {e}")
                                conn.sendall("SERVER: Failed to send acceptance.".encode())
                        else:
                            conn.sendall("SERVER: User not found.".encode())
                    else:
                        conn.sendall("SERVER: No pending friend request from this user.".encode())
            else:
                conn.sendall("SERVER: Unknown command.".encode())
    except Exception as e:
        print(f"Error with client {addr}: {e}")
    finally:
        with lock:
            if friend_code and friend_code in clients:
                print(f"Client {client_names[friend_code]} ({friend_code}) disconnected.")
                del clients[friend_code]
                del client_names[friend_code]
                if friend_code in friend_requests:
                    del friend_requests[friend_code]
                for user_code, friend_list in friends.items():
                    if friend_code in friend_list:
                        friend_list.remove(friend_code)
                if friend_code in friends:
                    del friends[friend_code]
                conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_IP, SERVER_PORT))
    server.listen()
    print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")
    while True:
        try:
            conn, addr = server.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
        except Exception as e:
            print("Error accepting connection:", e)
            break

if __name__ == '__main__':
    start_server()
