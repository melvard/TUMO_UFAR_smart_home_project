import threading

def password_insert():
    while True:
        key = input()
        print(key)

thread = threading.Thread(target=password_insert)
thread.start()