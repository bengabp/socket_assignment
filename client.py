import socket
from config import ENCODE_DECODE_FORMAT,MESSAGE_LENGTH,PORT

FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.184.25"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
	message = msg.encode(ENCODE_DECODE_FORMAT)
	msg_length = len(message)
	send_length = str(msg_length).encode(ENCODE_DECODE_FORMAT)
	send_length += b' ' * (MESSAGE_LENGTH - len(send_length))
	client.send(send_length)
	client.send(message)
	print(client.recv(2048).decode(ENCODE_DECODE_FORMAT))


send("Hello World!")
input()
send("Hello Everyone!")
input()
send("Hello Tim!")

send(DISCONNECT_MESSAGE)
