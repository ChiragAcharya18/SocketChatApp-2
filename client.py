import sqlite3
import socket
import threading
import pickle
import time
from getpass import getpass
import stdiomask
import sys
import os
from argon2 import PasswordHasher
from aess import encrypt, decrypt
import key


c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Trying to connect with server...")
try:
    c.connect(('localhost', 9999))
    print("Connection Established")
except:
    print("Something went wrong\nDisconnecting...")
    sys.exit()
key = key.key()
print("\n\t\tWelcome!\t\t")
h = input("Login[L] or Signup[S]: ")

def login():
    paes = encrypt(password, username)
    ld = pickle.dumps([username, paes])
    c.send("login".encode('utf-8'))
    c.send(ld)
    ack = c.recv(1024).decode('utf-8')
    if ack == "allok":
        print("\nLogin Successfull")
        if username == "admin":
            print(f"NOTE: \n1. Quit: {username.lower()}exitchat\n2. Your Password is Argon2 Hashed\n3. Server Shutdown Command: cmd server shutdown\n4. Kick: cmd kick username\n")
        else:
            print(f"NOTE: \n1. Quit: {username.lower()}exitchat\n2. Your Password is Argon2 Hashed\n")
        thrd()
    elif ack == "null":
        print("Invalid Username or Password!")
        sys.exit()
    elif ack == "loggedin":
        print(f"{username} already Logged in!")
        time.sleep(1)
        print("Do not try to login into somebody else's profile!")
        sys.exit()
    else:
        print("Something went wrong at Log In! Rerun the system")
        sys.exit()

def shutdown():
    print("Admin ran server shutdown")
    print("Server will shutdown in 10secs")
    time.sleep(4)
    print("Exiting...")
    os._exit(0)



def signup():
    arg = PasswordHasher()
    phash = arg.hash(password)
    ld = pickle.dumps([username, phash])
    c.send("signup".encode('utf-8'))
    c.send(ld)
    ack = c.recv(1024).decode('utf-8')
    if ack == "allok":
        print("Signup Successfull")
    elif ack == "exist":
        print("Username already taken!")
    else:
        print("Something went wrong at Sign up! Rerun the system")
        sys.exit()


def kickout():
    print("Admin kicked you out! Bye..")
    time.sleep(4)
    os._exit(0)

def recieve():
    while True:
        try:
            message = c.recv(1024).decode('utf-8')
            #message = decrypt(message, key)
            if message == "ssd":
                shutdown()
            elif f"[admin]: kick {username}" == message:
                kickout()
            elif f"[admin]: kick" == message[0:13]:
                t = message.split(" ")[-1]
                print(f"Admin Kicked out {t}")
            elif f"{username} joined the chat" in message:
                print(f"{username} joined the chat")
            elif "allok" not in message:
                print(f"{message}")
        except Exception as E:
            print("An error occurred: Exception: ", E)
            c.close()
            break


def write():
    while True:
        message = f"[{username}]: {input('')}"
        if f"[{username}]: {username.lower()}exitchat" == message:
            #c.send(f"{username}: Exiting... Bye!".encode('utf-8'))
            print("Please wait! Exiting...")
            time.sleep(1)
            os._exit(0)

        #message = encrypt(message, key)
        c.send(message.encode('utf-8'))




def thrd():
    tr = threading.Thread(target=recieve)
    tr.start()

    tw = threading.Thread(target=write)
    tw.start()


if h == 'L' or h == 'l' or h == " " or h == "":
    print("LOGIN")
    username = input("Enter your username: ")
    try:
        print(2/0)  #stdiomask doesnt work in pycham so put this exception purposely! If executing in cmd remove/comment this exception!
        password = stdiomask.getpass(prompt='Enter your password: ', mask='*')
    except:
        password = input("Enter your password: ")
    login()
elif h == "S" or h == "s" or h == "  ":
    print("SIGNUP")
    username = input("Enter a username: ")
    try:
        print(2/0)
        password = stdiomask.getpass(prompt='Enter Password: ', mask='*')
        p1 = stdiomask.getpass(prompt='Re-enter Password: ', mask='*')
    except:
        password = input("Enter a Password: ")
        if len(password) < 4:
            print("Password too small!")
            sys.exit()
        p1 = input("Re-enter a Password: ")

    if password == p1:
        signup()
    else:
        print("Enter password correctly! ")
        sys.exit()
else:
    print("Invalid Input")
