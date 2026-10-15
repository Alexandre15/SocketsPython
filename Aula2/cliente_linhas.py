import socket
from rich import print

HOST = "127.0.0.1"
PORT = 5000
MAX_LIN = 8192

def receberl(sock, buffer):
    while b"\n" not in buffer:
        dados = sock.recv(4096)

        if not dados:
            raise ConnectionError("[x] Servidor encerrou a conexão antes da resposta completa.")
        buffer.extend(dados)
        if len(buffer) > MAX_LIN and b"\n" not in buffer:
            raise ValueError("[!] Resposta excedeu o limite.")

    fim = buffer.index(b"\n")
    linha = bytes(buffer[:fim])
    del buffer[:fim + 1]

    if len(linha) > MAX_LIN:
        raise ValueError("[!] Resposta excedeu o limite.")
    return linha

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
    c.settimeout(5)
    c.connect((HOST, PORT))

    buffer = bytearray()

    print("Digite mensagens para o servidor.")
    print("Digite /sair para encerrar.")

    while True:
        texto = input("> ")

        if texto == "/sair":
            break

        mensagem = (texto + "\n").encode("utf-8")
        c.sendall(mensagem)

        resposta = receberl(c, buffer)
        print(resposta.decode("utf-8"))