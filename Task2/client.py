"""
TASK TWO : CLIENT-SERVER SET INTERSECTION
"""
import socket
import random
from config import (SERVER_HOST,
                    ADDRESS,
                    ENCODE_DECODE_FORMAT,
                    MESSAGE_LENGTH,
                    PORT,
                    DISCONNECT_MESSAGE)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)


# This function will send message to server
def send(msg, arg=None):
	message = msg.encode(ENCODE_DECODE_FORMAT)  # Encode message in utf-8 format
	msg_length = len(message)  # Get the length of the message string
	send_length = str(msg_length).encode(ENCODE_DECODE_FORMAT)  # Encode the message
	send_length += b' ' * (MESSAGE_LENGTH - len(send_length))  # Pad message with spaces to reach length
	client.send(send_length)  # Server expects to know the length of message before actual message
	client.send(message)  # Send the message to the client
	received_message = client.recv(MESSAGE_LENGTH).decode(ENCODE_DECODE_FORMAT)  # Decode message to string
	print("[SERVER]", received_message)


random_set = set()
while len(random_set) < 25:
	random_set.add(random.randint(1, 100))


# Send message to server
send(str(random_set))

# Send corrupt package to server since it's not expecting this type
send("Hahaha lets see how strong you are!")

# Cleanly disconnect client from server
send(DISCONNECT_MESSAGE)
