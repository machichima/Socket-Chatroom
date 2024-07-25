# Python program to implement server side of chat room.
import socket
import select
import sys
from _thread import *
#import tqdm
#from global_variable import *


SERVER_HOST = "134.209.42.176"
SERVER_PORT = 5002

BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

"""The first argument AF_INET is the address domain of the
socket. This is used when we have an Internet Domain with
any two hosts The second argument is the type of socket.
SOCK_STREAM means that data or characters are read in
a continuous flow."""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# # checks whether sufficient arguments have been provided
# if len(sys.argv) != 3:
# 	print ("Correct usage: script, IP address, port number")
# 	exit()

# # takes the first argument from command prompt as IP address
# IP_address = str(sys.argv[1])

# # takes second argument from command prompt as port number
# Port = int(sys.argv[2])

"""
binds the server to an entered IP address and at the
specified port number.
The client must be aware of these parameters
"""
server.bind((SERVER_HOST, SERVER_PORT))

"""
listens for 100 active connections. This number can be
increased as per convenience.
"""
server.listen(100)

list_of_clients = []

def clientthread(conn, addr):

	# sends a message to the client whose user object is conn
	conn.send(str.encode("Welcome to this chatroom!"))

	while True:
		
			try:
				received = conn.recv(BUFFER_SIZE).decode()

				if  SEPARATOR in received:
					print("<" + addr[0] + ">  sending" + received)
					filename, filesize = received.split(SEPARATOR)
					broadcast(f"{filename}{SEPARATOR}{filesize}".encode(), conn, True)
					receiveImage(received, conn)
				elif received:
					message = received

					"""prints the message and address of the
					user who just sent the message on the server
					terminal"""
					print ("<" + addr[0] + "> " + message)

					# Calls broadcast function to send message to all
					message_to_send = "<" + addr[0] + "> " + message
					broadcast(message_to_send, conn, False)

				else:
					"""message may have no content if the connection
					is broken, in this case we remove the connection"""
					remove(conn)

			except:
				continue

"""Using the below function, we broadcast the message to all
clients who's object is not the same as the one sending
the message """
def broadcast(message, connection, isImage):
	print('Broadcasting', message)
	for clients in list_of_clients:
		if isImage:
			if clients!=connection:
				try:
					clients.send(message)
				except(error):
					clients.close()
					print('error in broadcasting ', error)
					# if the link is broken, we remove the client
					remove(clients)
		else:
			if clients!=connection:
				try:
					clients.send(str.encode(message))
				except(error):
					clients.close()
					print('error in broadcasting ', error)



					# if the link is broken, we remove the client
					remove(clients)

"""The following function simply removes the object
from the list that was created at the beginning of
the program"""
def remove(connection):
	if connection in list_of_clients:
		list_of_clients.remove(connection)

def broadcastImage(filename, filesize, s):
	# with open('test.txt') as f:
	#     lines = f.readlines()
	#     for l in lines:
	#         print(l)
	print('In broadcasting Image')
	f= open(filename, 'rb')
	while True:
		# read the bytes from the file
	 
		bytes_read = f.read(BUFFER_SIZE)
		# print('\nbytes:', bytes_read)
		# print('type of byte:',type(bytes_read))
		if not bytes_read:
			# file transmitting is done
			# time.sleep(5)
			# s.send(f"=====".encode())
			print('Done')
			break
		# we use sendall to assure transimission in 
		# busy networks
		s.sendall(bytes_read)
		# update the progress bar


def receiveImage(received, connection):
	filename, filesize = received.split(SEPARATOR)
	print('Receiving')
	
	# progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
	with open(filename, "wb") as f:
		index = 0
		while True:
			print(index)
			if index == 200:
				# print('break')  
				break
			bytes_read = connection.recv(BUFFER_SIZE)
			# print(index)

			# if bytes_read.decode() == '=====':    
			# 	# nothing is received
			# 	# file transmitting is done
			# 	print('while break')
			# 	time.sleep(1)
				# broadcast('Done', connection, False)
			if not bytes_read:  
				print('break')  
				break
		
			
			f.write(bytes_read)
			index +=1
		print('ended')
	for clients in list_of_clients:
		if clients!=connection:
			broadcastImage(filename, filesize, clients)
			# for clients in list_of_clients:
			# 	if clients!=connection:
			# 		try:
			# 			clients.sendall(bytes_read)
			# 		except(error):
			# 			print('Error in sending Image:', error)
			# 			clients.close()

			# 			# if the link is broken, we remove the client
			# 			remove(clients)


while True:

	"""Accepts a connection request and stores two parameters,
	conn which is a socket object for that user, and addr
	which contains the IP address of the client that just
	connected"""
	conn, addr = server.accept()

	"""Maintains a list of clients for ease of broadcasting
	a message to all available people in the chatroom"""
	list_of_clients.append(conn)

	# prints the address of the user that just connected
	print (addr[0] + " connected")

	# creates and individual thread for every user
	# that connects
	start_new_thread(clientthread,(conn,addr))	

conn.close()
server.close()

