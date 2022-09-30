import socket
from config import (SERVER_HOST,
                    ADDRESS,
                    ENCODE_DECODE_FORMAT,
                    MESSAGE_LENGTH,
                    PORT,
                    DISCONNECT_MESSAGE)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)


def send(msg):
	message = msg.encode(ENCODE_DECODE_FORMAT)
	msg_length = len(message)
	send_length = str(msg_length).encode(ENCODE_DECODE_FORMAT)
	send_length += b' ' * (MESSAGE_LENGTH - len(send_length))
	client.send(send_length)
	client.send(message)
	print(client.recv(MESSAGE_LENGTH).decode(ENCODE_DECODE_FORMAT))


send("Hello World!")
input()
send("Hello Everyone!")
input()
send("Hello Tim!")

send(DISCONNECT_MESSAGE)
