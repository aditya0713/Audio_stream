import socket
import os
import sys
from _thread import *
import time
import pyaudio
import threading


def Produce(ServerSocket):
	global ThreadCount, quit, host, quit
	try:
		ServerSocket.bind((host, port))
	except socket.error as e:
		print(str(e))

	print('Waitiing for a Connection..')
	ServerSocket.listen(5)


	def threaded_client(connection):
		chunk = 1024  # Record in chunks of 1024 samples
		sample_format = pyaudio.paInt16  # 16 bits per sample
		channels = 2
		fs = 48000  # Record at 44100 samples per second
		seconds = 1

		p = pyaudio.PyAudio()  # Create an interface to PortAudio

		print('Recording')

		stream = p.open(format=sample_format,
				        channels=channels,
				        rate=fs,
				        frames_per_buffer=chunk,
				        input=True)

		while not quit:
			frames = []  # Initialize array to store frames

			for i in range(0, int(fs / chunk * seconds)):
				data = stream.read(chunk)
				frames.append(data)

			connection.sendall(b''.join(frames))
			print("Sent")
			#print(b''.join(frames))
			print(len(b''.join(frames)))
			#sys.exit(1)
		# Stop and close the stream 
		stream.stop_stream()
		stream.close()
		# Terminate the PortAudio interface
		p.terminate()
		print('Finished recording')
		
		connection.close()

	while not quit:
		Client, address = ServerSocket.accept()
		print('Connected to: ' + address[0] + ':' + str(address[1]))
		start_new_thread(threaded_client, (Client, ))
		ThreadCount += 1
		print('Thread Number: ' + str(ThreadCount))
	print("Producer Quiting")
#	ServerSocket.close()

def Driver(ServerSocket, produce):
	global quit
	while True:
		option = input(">>")
		if option == "q":
			quit = True
			break
	print("Quiting Driver")
	ServerSocket.close()
	#produce.kill()
	#print(produce.isAlive())
	
print("Changing")
#t = os.open('log', os.O_WRONLY)
#os.dup2(t, 1)
#os.dup2(t, 2)
print("test")
host = '192.168.0.100'
port = 1234
ThreadCount = 0
quit = False
ServerSocket = socket.socket()
produce = threading.Thread(target=Produce, args=(ServerSocket,))
driver = threading.Thread(target=Driver, args=(ServerSocket, produce))
produce.start()
driver.start()
#produce.join()
#driver.join()
#sys.stdout.close()
#stdout.close()
print("end")
