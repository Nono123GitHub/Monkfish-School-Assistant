import socket
from PIL import Image
from io import BytesIO

SERVER_IP = "127.0.0.1"
SERVER_PORT = 65432
STUDENT_PORT = 65433
clients = {}

def handle_client(conn, addr):
    try:
        data = conn.recv(1024)
        message_data = b""
        
        while data:
            message_data += data
            data = conn.recv(1024)
            
        if message_data.startswith(b"REGISTER:"):
            initials = message_data[9:].decode('utf-8').strip()
            clients[initials] = addr[0]
        elif b":" in message_data:
            target_initials, image_data = message_data.split(b":", 1)
            target_initials = target_initials.decode('utf-8')
            
            if target_initials in clients:
                target_ip = clients[target_initials]
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((target_ip, STUDENT_PORT))
                    s.sendall(image_data)
    except:
        pass
    finally:
        conn.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((SERVER_IP, SERVER_PORT))
        s.listen(5)
        print("Server started, waiting for connections...")
        while True:
            conn, addr = s.accept()
            handle_client(conn, addr)

if __name__ == "__main__":
    start_server()