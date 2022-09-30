"""
TASK THREE: CLIENT-SERVER PROTOCOL
"""

# Importing all necessary modules
import socket
import threading
import random
import os

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
	connected = True
	while connected:
		msg_length = conn.recv(MESSAGE_LENGTH).decode(ENCODE_DECODE_FORMAT)  # Decode the message
		if msg_length:
			msg_length = int(msg_length)
			msg = conn.recv(msg_length).decode(ENCODE_DECODE_FORMAT)
			print(f"[CLIENT {addr[0]}] {msg}")
			if msg == DISCONNECT_MESSAGE:  # check for disconnect message to disconnect client cleanly
				print(f"[DISCONNECT] {addr[0]} has disconnected, bye!")
				connected = False

			try:  # Error handler for handling errors that may be due to network

				# If it's a close message raise an error which server will handle
				if DISCONNECT_MESSAGE not in msg:
					if 'am' in msg:  # Check if query is a ==> Basic Hello
						name = msg.split("am", 1)[-1]
						conn.send(f"Hello {name}, Glad to meet you".encode(ENCODE_DECODE_FORMAT))
					elif 'search' in msg:  # Check if query is b ==> Search query
						search_keyword = msg.split('for')[-2].strip()
						print(search_keyword)
						results = []
						for file in os.listdir("files/"):
							if file.startswith(search_keyword):
								results.append(file)
						if not results:  # Send appropriate message if there are no matches
							result_string = "Nah nah.. didn't find any file that matches your query string"
						else:
							result_string = "Search results for '" + search_keyword + "'\n" + '\n'.join(results)

						conn.send(result_string.encode(ENCODE_DECODE_FORMAT))
					else:
						conn.send(
							"Sorry ,Invalid query: Must be either 'Hello, I am XYZ' or 'Can you search for XYZ for me? "
							"Rephrase and try again".encode(
								ENCODE_DECODE_FORMAT))
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
