"""
TASK TWO : CLIENT-SERVER SET INTERSECTION
"""

# Importing all necessary modules
import socket
import threading
import random

# Importing constant variables declared in config file
from config import (SERVER_HOST,
                    ENCODE_DECODE_FORMAT,
                    PORT,
                    ADDRESS,
                    MESSAGE_LENGTH,
                    DISCONNECT_MESSAGE)

# Creating a socket object (server) and binding it to the connection characteristics
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)


# Define function to handle clients separately in another thread
def handle_client(conn, addr):
	print(f"New connection from {addr}")
	conn.send("Please could you send a set of 25 numbers between 1 and 100?".encode(ENCODE_DECODE_FORMAT))
	connected = True
	while connected:
		msg_length = conn.recv(MESSAGE_LENGTH).decode(ENCODE_DECODE_FORMAT)  # Decode the message
		if msg_length:
			msg_length = int(msg_length)
			msg = conn.recv(msg_length).decode(ENCODE_DECODE_FORMAT)
			print(f"[CLIENT {addr[0]}] {msg}")
			if msg == DISCONNECT_MESSAGE: # check for disconnect message to disconnect client cleanly
				print(f"[DISCONNECT] {addr[0]} has disconnected, bye!")
				connected = False

			try: # Error handler for handling errors that may be due to network
				real_object = eval(msg)
				# check if client has sent a set object
				if type(real_object) is set:
					# Server will now generate its own set of numbers
					server_set = set()
					client_set: set = real_object
					while len(server_set) < len(client_set):
						server_set.add(random.randint(1, 100))
					common_values = client_set.intersection(server_set)
					conn.send(f"Common values are {common_values}".encode(ENCODE_DECODE_FORMAT))
				else:
					conn.send("Hey you sent me an invalid type !".encode(ENCODE_DECODE_FORMAT))
			except Exception as err:
				conn.send("Got an error, but I handled it anyways".encode(ENCODE_DECODE_FORMAT))
	conn.close()


# Listening for client connections and handling them

server.listen()
print(f"[RUNNING] Server is listening on {SERVER_HOST}")
while True:
	conn, addr = server.accept()

	# Assign function to handle client in new separate thread
	thread = threading.Thread(target=handle_client, args=(conn, addr))
	thread.start()
