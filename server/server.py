#!/usr/bin/env python3

from socket import socket, AF_INET, SOCK_STREAM, gethostbyname, gethostname
from ssl import create_default_context, Purpose
from json import load, dump
from datetime import datetime
from argparse import ArgumentParser

def load_passwords_from_json(filename):
    with open(filename, 'r') as f:
        data = load(f)
        return data

def save_passwords_to_json(filename, passwords):
    with open(filename, 'w') as f:
        dump(passwords, f)

def load_slot_details_from_json(filename):
    with open(filename, 'r') as f:
        data = load(f)
        return data

def save_slot_details_to_json(filename, slot_details):
    with open(filename, 'w') as f:
        dump(slot_details, f)

def load_history_from_json(filename):
    with open(filename, 'r') as f:
        data = load(f)
        return data

def save_history_to_json(filename, history):
    with open(filename, 'w') as f:
        dump(history, f)


def book_my_slot_server(port):
    user_credentials = load_passwords_from_json("../password.json")
    slot_details = load_slot_details_from_json("../slotdetails.json")
    booking_history = load_history_from_json("../history.json")

    sock_connection = socket(AF_INET, SOCK_STREAM)
    sock_connection.bind((gethostbyname(gethostname()), port))
    sock_connection.listen()

    context = create_default_context(Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile = "cert.pem", keyfile="key.pem")
    print("BookMySlot server running")
    while True:
        try:
            conn, addr = sock_connection.accept()
            conn = context.wrap_socket(conn, server_side=True)
            print(f'Client connected from {addr}')
        except KeyboardInterrupt:
            print('Connection closed')
            break

        logged_in = False
        while not logged_in:
            username = conn.recv(1024).decode().strip()
            password = conn.recv(1024).decode().strip()
            if username in user_credentials and user_credentials[username] == password:
                conn.sendall(b'correct ID and password\n')
                logged_in = True
            else:
                conn.sendall(b'incorrect ID and password\n')

        while True:
            received_data = conn.recv(1024).decode()
            if received_data == '1':
                user_found = False
                for history_entry in booking_history:
                    if history_entry["username"] == username:
                        conn.sendall(b'0')
                        user_found = True
                        break

                if not user_found:
                    conn.sendall(b'1')
                    available_slots = ''
                    slot_counter = 1
                    for slot_entry in slot_details:
                        if slot_entry["slot_status"] == 0:
                            slot_date = slot_entry["slot_date"]
                            formatted_slot = f"{slot_counter}.{slot_date}"
                            available_slots += formatted_slot + '\n'
                            slot_counter += 1
                    conn.sendall(available_slots.encode())

                    selected_slot = conn.recv(1024).decode()
                    slot_counter = 1
                    for slot_entry in slot_details:
                        if slot_entry["slot_status"] == 0:
                            selected_slot_index = str(slot_counter)
                            if selected_slot == selected_slot_index:
                                slot_entry["slot_status"] = 1
                                slot_entry["booked_by"] = username
                                slot_entry["booked_at"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                save_slot_details_to_json("../slotdetails.json", slot_details)
                                booking_history.append({"username": username, "booked_at": slot_entry["booked_at"], "slot_date": slot_entry["slot_date"]})
                                save_history_to_json("../history.json", booking_history)
                                break
                            slot_counter += 1

            elif received_data == '3':
                slot_booked = False
                for history_entry in booking_history:
                    if history_entry["username"] == username and "slot_date" in history_entry:
                        slot_details_msg = f"{username} slot details: {history_entry['slot_date']}\nYour slot booked on: {history_entry['booked_at']}"
                        conn.sendall(slot_details_msg.encode())
                        slot_booked = True
                        break
    
                if not slot_booked:
                    conn.sendall(b'You have not booked a slot')

            elif received_data == '2':
                slot_found = False
                slot_date_to_drop = ''
                for history_entry in booking_history:
                    if history_entry["username"] == username and "slot_date" in history_entry:
                        slot_found = True
                        conn.sendall(b'dropped successfully')
                        slot_date_to_drop = history_entry["slot_date"]
                        break
                
                if not slot_found:
                    conn.sendall(b'You have not booked a slot')
                else:
                    for slot_entry in slot_details:
                        if slot_entry["slot_date"] == slot_date_to_drop:
                            slot_entry["slot_status"] = 0
                            slot_entry["booked_by"] = ""
                            slot_entry["booked_at"] = ""
                            save_slot_details_to_json("../slotdetails.json", slot_details)
                            booking_history = [entry for entry in booking_history if entry["username"] != username]
                            save_history_to_json("../history.json", booking_history)
                            break


            elif received_data == '4':
                break
            else:
                z = 1

    sock_connection.close()


def main():
    parser = ArgumentParser(description="Initialize a socket connection with a Admin-specified port.")
    parser.add_argument("--port", type=int, help="Specify the PORT number.")
    args = parser.parse_args()
    print(f"Using port: {args.port}")
    book_my_slot_server(args.port)

if __name__ == "__main__":
    main()
