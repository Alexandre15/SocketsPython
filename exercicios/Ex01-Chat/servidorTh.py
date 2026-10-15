
import socket
import threading

HOST = "127.0.0.1"
PORT = 5001

def atender_cliente(con, end):
    print(f"Cliente conectado: {end}")

    try:
        while True:
            dados = con.recv(4096)

            if not dados:
                break

            msg = dados.decode("utf-8").strip()
            print(f"{end[0]}: {msg}")

    finally:
        con.close()
        print(f"Cliente desconectado: {end}")

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()

    print(f"Servidor escutando na porta {PORT}")

    while True:
        con, end = s.accept()

        thread = threading.Thread(
            target=atender_cliente,
            args=(con, end)
        )
        thread.start()

if __name__ == "__main__":
    main()
