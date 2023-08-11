#!/usr/bin/env python3

from socket import socket, AF_INET, SOCK_STREAM
from ssl import create_default_context, CERT_NONE
from argparse import ArgumentParser

def book_my_slot_client(HOST, PORT):
    context = create_default_context()
    context.check_hostname = False
    context.verify_mode = CERT_NONE

    sock_connection = socket(AF_INET, SOCK_STREAM)
    sock_connection = context.wrap_socket(sock_connection, server_hostname=HOST)
    sock_connection.connect((HOST, PORT))
    
    print('Connected to the BookMySlot server')
    logged_in = False
    while not logged_in:
        username = input('Username: ')
        password = input('Password: ')
        sock_connection.sendall(username.encode())
        sock_connection.sendall(password.encode())
        
        authentication_response = sock_connection.recv(1024).decode().strip()
        if authentication_response == 'correct ID and password':
            logged_in = True
        else:
            print('Invalid Login Details, please try again')
    print('Successfully logged in to the appointment scheduler.')

    while True:
        print('Main Menu')
        print('1. Book a slot for demo')
        print('2. Drop existing slot')
        print('3. view your slot details')
        print('4. Exit')
        print('\n')
        
        user_choice = input('choose from above option: ')
        if user_choice=='1':
            user_choice='bookslot'
        elif user_choice=='2':
            user_choice='dropslot'
        elif user_choice=='3':
            user_choice='viewslot'
        else:
            user_choice='exit'
        sock_connection.sendall(user_choice.encode())
        if user_choice=='bookslot':
            slot_status = sock_connection.recv(1024).decode()
            if slot_status == '0':
                print('\nYour slot is already booked.\nPlease use modify option to re-schedule your slot\n')
            else:
                print('\nbook your slot')
                available_slots = sock_connection.recv(1024).decode()
                print(available_slots)
                selected_slot = input('select an option from above slots : ')
                sock_connection.sendall(selected_slot.encode())
                selected_slot_index = int(selected_slot)
                if(selected_slot_index < 10):
                    print('Slot booked successfully\n')

        elif user_choice=='dropslot':
            drop_result = sock_connection.recv(1024).decode()
            print('\n')
            print(drop_result)
            print('\n')
        elif user_choice=='viewslot':
            slot_details_result = sock_connection.recv(1024).decode()
            print('\n')
            print(slot_details_result)
            print('\n')
        
        elif user_choice =='exit':
            sock_connection.close()
            break
        else:
            print('Invalid command')
            print('\n')


def main():
    parser = ArgumentParser(description="Initialize a socket connection with a Admin-specified HOST and PORT.")
    
    parser.add_argument("--host", type=str, help="Specify the HOST address.")
    parser.add_argument("--port", type=int, help="Specify the port number.")

    args = parser.parse_args()
    # print(f"Using port: {args.host, args.port}")
    book_my_slot_client(args.host, args.port)

if __name__ == "__main__":
    main()
