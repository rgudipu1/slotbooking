#!/usr/bin/env python3

import os
import socket
import ssl
import sys
a=sys.argv
a1=a[1]
a2=int(a[2])
HOST = a1
PORT = a2
def sftp_client():
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock = context.wrap_socket(sock, server_hostname=HOST)
    sock.connect((HOST, PORT))
    print('Connected to the sftp server')
    authenticated = False
    while not authenticated:
        username = input('Username: ')
        password = input('Password: ')
        sock.sendall(username.encode())
        sock.sendall(password.encode())
        response = sock.recv(1024).decode().strip()
        if response == 'correct ID and password':
            authenticated = True
        else:
            print('Invalid Login Details, please try again')
    print('Logged in to the appoint scheduler')

    while True:
        print('Main Menu')
        print('1. Book a slot for demo')
        print('2. Drop existing slot')
        print('3. view your slot details')
        print('4. Exit')
        print('\n')
        command = input('choose from above option: ')
        sock.sendall(command.encode())
        if command=='1':
            status=sock.recv(1024).decode()
            if status=='0':
                print('\nYour slot is already booked.\nPlease use modify option to modify your slot\n')
            else:
                print('\nbook your slot')
                bs=sock.recv(1024).decode()
                print(bs)
                sd=input('select an option from above slots : ')
                sock.sendall(sd.encode())
                prasad=int(sd)
                if(prasad<10):
                    print('slot booked successfully\n')
        elif command=='2':
            result31=sock.recv(1024).decode()
            print('\n')
            print(result31)
            print('\n')
        elif command=='3':
            result3=sock.recv(1024).decode()
            print('\n')
            print(result3)
            print('\n')
        elif command=='4':
            sock.close()
            break
        else:
            print('Invalid command')
            print('\n')


sftp_client()