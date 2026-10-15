import socket
from time import sleep

HOST = "127.0.0.1"
PORT = 5001

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)

    print((f"Servidor escutando em {HOST}:{PORT}"))

    conexao, endereco = s.accept()

    with conexao:
        print(f"Cliente conectado: IP:[{endereco[0]}] PORTA:[{endereco[1]}]")

        while True:
            dados = conexao.recv(4096)

            if not dados:
                print("Cliente encerrou a conexão.")
                break

            print(f"Recebidos {len(dados)} bytes: {dados!r}")

            conexao.sendall(dados)
    print("Conexão encerrada.")