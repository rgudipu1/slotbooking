#!/usr/bin/env python3


import os
import socket
import ssl
import sys
from datetime import datetime
a=sys.argv
a1=int(a[1])
def sftp_server(certfile, keyfile):
    port = a1
    passwords = {}
    with open("../password") as f:
        for line in f:
            username, password = line.strip().split(' ')
            passwords[username] = password

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostbyname(socket.gethostname()), port))
    s.listen()

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=certfile, keyfile=keyfile)
    print("server working")
    while True:
        try:
            conn,addr = s.accept()
            conn=context.wrap_socket(conn, server_side=True)
            print(f'Connected by {addr}')
        except KeyboardInterrupt:
            print('connection ended')
            break
        log = False
        while not log:
            username = conn.recv(1024).decode().strip()
            password = conn.recv(1024).decode().strip()
            if username in passwords and passwords[username] == password:
                conn.sendall(b'correct ID and password\n')
                log = True
            else:
                conn.sendall(b'incorrect ID and password\n')

        while True:
            d = conn.recv(1024).decode()
            if d=='1':
                m=0
                with open("../history.txt") as f:
                    for line in f:
                        split_line = line.strip().split()
                        if len(split_line) > 0:
                            na = split_line[0]
                            if (username == na):
                                conn.sendall(b'0')
                                m=1
                    if m==0:
                        conn.sendall(b'1')
                        k=''
                        q=1
                        with open("../slotdetails.txt") as z:
                            for line in z:
                                split_line = line.strip().split()
                                if len(split_line) > 0:
                                    na = split_line[1]
                                    w=str(q)
                                    ma=split_line[0]
                                    ma=w+'.'+ma
                                    if(na=='0'):
                                        k=k+ma+'\n'
                                        q=q+1
                        conn.sendall(k.encode())
                        sd=conn.recv(1024).decode()
                        r=1
                        uv=''
                        with open("../slotdetails.txt",'r+') as z:
                            lines = z.readlines()
                            for i in range(len(lines)):
                                n,count = lines[i].strip().split()
                                if count=='0':
                                    j=str(r)
                                    if(sd==j):
                                        uv=uv+n
                                        count = int(count) + 1
                                        lines[i] = n + ' ' + str(count) + '\n'
                                        break
                                    r=r+1
                            z.seek(0)
                            z.writelines(lines)
                        with open('../history.txt', 'a') as f:
                                now = datetime.now()
                                timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
                                f.write(username + ' ' + timestamp + ' '+n+'\n')
            elif d=='3':
                a=0
                with open('../history.txt') as f:
                    for line in f:
                        v_name,datess,timess,sl= line.strip().split()
                        if (v_name==username):
                            tosend=username+" slot details: "+sl+"\n"+"Your slot booked on: "+datess+" "+timess
                            conn.sendall(tosend.encode())
                            a=1
                            break
                    if a==0:
                        conn.sendall(b'You have not booked slot')
            elif d=='2':
                ff=0
                vaa=''
                with open('../history.txt', "r") as file:
                    lines = file.readlines()
                with open('../history.txt', "w") as file:
                    for line in lines:
                        if username not in line:
                            file.write(line)
                        else:
                            ff=1
                            conn.sendall(b'dropped successfully')
                            words=line.split()
                            vaa=words[3]
                if ff==0:
                    conn.sendall(b'You have not booked slot')
                else:
                    with open("../slotdetails.txt",'r+') as z:
                            lines = z.readlines()
                            for i in range(len(lines)):
                                n,count = lines[i].strip().split()
                                if count=='1':
                                    if(n==vaa):
                                        count = int(count) - 1
                                        lines[i] = n + ' ' + str(count) + '\n'
                                        break
                            z.seek(0)
                            z.writelines(lines)
            elif d=='4':
                break
            else:
                z=1


sftp_server("cert.pem", "key.pem")