import socket
from rich import print

HOST = "127.0.0.1"
PORT = 5000
MAX_LIN = 20

def receberl(sock, buffer):
    while b"\n" not in buffer:
        dados = sock.recv(4096)

        if not dados:
            raise ConnectionError("[x] Servidor encerrou a conexão antes da resposta completa.")
        buffer.extend(dados)
        if len(buffer) > MAX_LIN and b"\n" not in buffer:
            raise ValueError("[!] Resposta excedeu o limite.")

    fim = buffer.index(b"\n") # Verifica a condição e retorna a posição da primeira ocorrência
    linha = bytes(buffer[:fim])
    del buffer[:fim + 1] # Remove somente a 1° mensagem e o delimitador

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
        texto1 = input("T1> ")
        texto2 = input("T2> ")

        if texto1 == "/sair" or texto2 == "/sair":
            break

        mensagem1 = (texto1 + "\n").encode("utf-8")
        mensagem2 = (texto2 + "\n").encode("utf-8")
        c.sendall(mensagem1 + mensagem2)

        resposta1 = receberl(c, buffer)
        resposta2 = receberl(c, buffer)
        print(resposta1.decode("utf-8"))
        print(resposta2.decode("utf-8"))