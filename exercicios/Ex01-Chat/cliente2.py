import socket

HOST = "127.0.0.1"
PORT = 5001

def main():
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((HOST, PORT))

    while True:

        msg = str(input("Digite: "))
        print(msg)
        if msg == "/exit":
            break
        c.sendall((msg + "\n").encode("utf-8"))

if __name__ == "__main__":
    main()