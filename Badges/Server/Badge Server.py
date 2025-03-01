import socket
import threading

SERVER_IP = '192.168.52.244'
SERVER_PORT = 65432  # For teachers sending images
STUDENT_PORT = 65433  # For students receiving images

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(5)

student_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
student_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
student_socket.bind((SERVER_IP, STUDENT_PORT))
student_socket.listen(5)

print(f"Server running on {SERVER_IP}:{SERVER_PORT} (Teachers) and {SERVER_IP}:{STUDENT_PORT} (Students)")

students = {}

def handle_teacher(client_socket):
    try:
        student_initials = client_socket.recv(50).decode().strip()
        print(f"📩 Received badge request for: {student_initials}")

        # ✅ Receive the full image
        image_data = b""
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            image_data += data

        print(f"✅ Received {len(image_data)} bytes of image data for {student_initials}")

        # ✅ Ensure student is still connected
        if student_initials in students:
            student_conn = students[student_initials]

            if isinstance(student_conn, socket.socket):
                try:
                    print(f"📤 Sending {len(image_data)} bytes to {student_initials}")
                    student_conn.sendall(image_data)  # Send image
                    print(f"✅ Badge successfully sent to {student_initials}")

                except Exception as e:
                    print(f"❌ Error sending to {student_initials}: {e}")

            else:
                print(f"❌ Error: {student_initials} does not have a valid socket!")

        else:
            print(f"❌ Student {student_initials} not connected")

    except Exception as e:
        print(f"❌ Error handling teacher connection: {e}")

    finally:
        client_socket.close()  # ✅ Ensure teacher connection is closed




def handle_student(client_socket, addr):
    try:
        student_name = client_socket.recv(1024).decode().strip()
        students[student_name] = client_socket  # Store socket reference
        print(f"🟢 Student {student_name} connected and ready to receive badges.")

        while True:
            try:
                data = client_socket.recv(1)  # Small receive check to keep alive
                if not data:
                    break  # Exit if client disconnects
            except:
                break

    except Exception as e:
        print(f"❌ Error handling student connection: {e}")

    finally:
        print(f"🔴 Student {student_name} disconnected.")
        del students[student_name]  # Remove disconnected student
        client_socket.close()



def accept_teachers():
    while True:
        client, addr = server_socket.accept()
        threading.Thread(target=handle_teacher, args=(client,)).start()

def accept_students():
    while True:
        student, addr = student_socket.accept()
        threading.Thread(target=handle_student, args=(student, addr)).start()

threading.Thread(target=accept_teachers, daemon=True).start()
threading.Thread(target=accept_students, daemon=True).start()

while True:
    pass
