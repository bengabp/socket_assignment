import socket
import threading

from config import (SERVER_HOST,
                    ENCODE_DECODE_FORMAT,
                    PORT,
					ADDRESS,
                    MESSAGE_LENGTH,
                    DISCONNECT_MESSAGE)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)


# Define function to handle clients separately in another thread
def handle_client(conn, addr):
	print(f"New connection from {addr}")
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
	print(f"[RUNNING] Server is listening on {SERVER_HOST}")
	while True:
		conn, addr = server.accept()
		thread = threading.Thread(target=handle_client, args=(conn, addr))
		thread.start()
		print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] server is starting...")
start()
server.close()
