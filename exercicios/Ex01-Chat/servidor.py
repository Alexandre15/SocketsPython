import socket

ENDER = ("127.0.0.1", 5000)

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(ENDER)
    s.listen()
    while True:
        con, end = s.accept()
        while True:
            print(f"{end[0]}: {con.recv(4096).decode('utf-8')}")

if __name__ == "__main__":
    main()