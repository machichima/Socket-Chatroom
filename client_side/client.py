# Python program to implement client side of chat room.
import socket
import select
import sys
import tqdm
import cv2
from IPython.display import Image
import os
import numpy as np




SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096
key = [1, 3, 4, 6, 7]




server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:
	print ("Correct usage: script, IP address, port number")
	exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.connect((IP_address, Port))

def message2binary(message):
	if type(message) == str:
		result= ''.join([ format(ord(i), "08b") for i in message ])
	
	elif type(message) == bytes or type(message) == np.ndarray:
		result= [ format(i, "08b") for i in message ]
	
	elif type(message) == int or type(message) == np.uint8:
		result=format(message, "08b")

	else:
		raise TypeError("Input type is not supported")
	
	return result  

def encode_data(img, key):
	data=input("Enter the data to be Encoded:")    
	if (len(data) == 0): 
		raise ValueError('Data is empty')
  
	filename = "stegano_final.png"#input("Enter the name of the New Image after Encoding(with extension):")
	
	no_bytes=(img.shape[0] * img.shape[1] * 3) // 8
	
	print("Maximum bytes to encode:", no_bytes)
	
	if(len(data)>no_bytes):
		raise ValueError("Error encountered Insufficient bytes, Need Bigger Image or give Less Data !!")
	
	# Using the below as delimeter
	data +='*****'    
	
	data_binary=message2binary(data)
	# print(data_binary)
	data_len=len(data_binary)
	
	# print("The Length of Binary data",data_len)
	
	data_index = 0
	key_index = 0
	
	for i in img:
		for pixel in i:
			
			r, g, b = message2binary(pixel)
			# print(r)
			# print(g)
			# print(b)
			#   print(pixel)
			if data_index < data_len:
				# hiding the data into LSB(Least Significant Bit) of Red Pixel
		#               print("Original Binary",r)
				# print("The old pixel",pixel[0])
				insert_place = key[key_index]
				pixel[0] = int(r[:insert_place] + data_binary[data_index] + r[insert_place+1:], 2) #changing to binary after overwrriting the LSB bit of Red Pixel
		#               print("Changed binary",r[:-1] + data_binary[data_index])
				
				data_index += 1
				key_index += 1
				if(key_index >= len(key)):
					key_index = 0
				#list1.append(pixel[0])

			if data_index < data_len:
				# hiding the data into LSB of Green Pixel
				insert_place = key[key_index]
				pixel[1] = int(g[:insert_place] + data_binary[data_index] + g[insert_place+1:], 2) #changing to binary after overwrriting the LSB bit of Green Pixel
				data_index += 1
				key_index += 1
				if(key_index >= len(key)):
					key_index = 0
				#list1.append(pixel[1])

			if data_index < data_len:
				# hiding the data into LSB of  Blue Pixel
				insert_place = key[key_index]
				pixel[2] = int(b[:insert_place] + data_binary[data_index] + b[insert_place+1:], 2) #changing to binary after overwrriting the LSB bit of Blue pixel
				data_index += 1
				key_index += 1
				if(key_index >= len(key)):
					key_index = 0
				#list1.append(pixel[2])

				# if data is encoded, just breaking out of the Loop
			if data_index >= data_len:
				break

		 
  
	cv2.imwrite(filename,img)
	
	print("Encoded the data successfully and the image is successfully saved as ",filename)
def decode_data(img, key):
    key_index = 0
    binary_data = ""
    for i in img:
      for pixel in i:
        
        #   print(pixel)
        r, g, b = message2binary(pixel) 
        binary_data += r[key[key_index]]  #Extracting Encoded data from the LSB bit of Red Pixel as we have stored in LSB bit of every pixel.
        key_index += 1
        if(key_index >= len(key)):
            key_index = 0
        binary_data += g[key[key_index]]  #Extracting Encoded data from the LSB bit of Green Pixel
        key_index += 1
        if(key_index >= len(key)):
            key_index = 0
        binary_data += b[key[key_index]]  #Extracting Encoded data from LSB bit of Blue Pixel
        key_index += 1
        if(key_index >= len(key)):
            key_index = 0

    # splitting by 8-bits
    all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]

    # Converting the bits to Characters
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-5:] == "*****": #Checking if we have reached the delimeter which is "*****"
            break

    
    print("The Encoded data was :--",decoded_data[:-5])
def send_file(filename, s):
	# get the file size
	print('In send file')
	filesize = os.path.getsize(filename)
	# create the client socket


	# send the filename and filesize
	s.send(f"{filename}{SEPARATOR}{filesize}".encode())

	# start sending the file
	# progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
	# with open('test.txt') as f:
	#     lines = f.readlines()
	#     for l in lines:
	#         print(l)

	f= open(filename, 'rb')
	while True:
		# read the bytes from the file
		# print(f)
	 
		bytes_read = f.read(BUFFER_SIZE)
		# print('\nbytes:', bytes_read)
		# print('type of byte:',type(bytes_read))
		if not bytes_read:
		#     # file transmitting is done
		#     s.sendall(f"=====".encode())
		#     print('Done')
			break
		# we use sendall to assure transimission in 
		# busy networks
		s.sendall(bytes_read)
		# update the progress bar
		# progress.update(len(bytes_read))

def receiveImage(received, connection):
	filename, filesize = received.split(SEPARATOR)
	# progress = tqdm.tqdm(range(int(filesize)), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
	with open(filename, "wb") as f:
		index =0
		while True:
			# print(index)
			if index == 72:
				# print('Breaking recv')
				# nothing is received
				# file transmitting is done
				break
			# read 1024 bytes from the socket (receive)
			bytes_read = connection.recv(BUFFER_SIZE)
			# print(bytes_read)
			if not bytes_read:    
				# nothing is received
				# file transmitting is done
				break
		
			# write to the file the bytes we just received
			f.write(bytes_read)
			index+=1
			# update the progress bar
			# progress.update(len(bytes_read))
def sendImage(server):
	image=cv2.imread("test.jpeg")   # import image
	encode_data(image, key)
	send_file('stegano_final.png',server)

toBreak = False

while True:

	if toBreak == True:
		break
	# maintains a list of possible input streams
	sockets_list = [sys.stdin, server]

	""" There are two possible input situations. Either the
	user wants to give manual input to send to other people,
	or the server is sending a message to be printed on the
	screen. Select returns from sockets_list, the stream that
	is reader for input. So for example, if the server wants
	to send a message, then the if condition will hold true
	below.If the user wants to send a message, the else
	condition will evaluate as true"""
	read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])
	for socks in read_sockets:
		print('-')
		if socks == server:
			message = str(socks.recv(BUFFER_SIZE), "utf-8")
			# print(message)
			if  SEPARATOR in message:
				filename, filesize = message.split(SEPARATOR)
				print('Recieving Image')
				receiveImage(message, socks)
			else :
				print (message)
		else:
			message = sys.stdin.readline()
			if 'quit' in message: 
				print('quited')
				toBreak = True
				break
			elif 'send image' in message:
				print('sending image')
				sendImage(server)

				break
			elif 'decode image' in message:
				image1=cv2.imread("stegano_final.png")
				print('decoding image')
				decode_data(image1, key)
				break


			server.send(str.encode(message))
			sys.stdout.write("<You>")
			sys.stdout.write(message)
			sys.stdout.flush()

server.close()

