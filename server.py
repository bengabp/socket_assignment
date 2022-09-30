import socket
import threading

from config import ENCODE_DECODE_FORMAT, PORT, MESSAGE_LENGTH

SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
	print(f"[NEW CONNECTION] {addr} connected.")

	connected = True
	while connected:
		msg_length = conn.recv(MESSAGE_LENGTH).decode(ENCODE_DECODE_FORMAT)
		if msg_length:
			msg_length = int(msg_length)
			msg = conn.recv(msg_length).decode(ENCODE_DECODE_FORMAT)
			if msg == DISCONNECT_MESSAGE:
				connected = False

			print(f"[{addr}] {msg}")
			conn.send("Msg received".encode(ENCODE_DECODE_FORMAT))

	conn.close()


def start():
	server.listen()
	print(f"[LISTENING] Server is listening on {SERVER}")
	while True:
		conn, addr = server.accept()
		thread = threading.Thread(target=handle_client, args=(conn, addr))
		thread.start()
		print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] server is starting...")
start()
server.close()
