import socket

HOST = "127.0.0.1"
PORT = 5000

ENDER = (HOST, PORT)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
    try:
        c.settimeout(.1)
        c.connect(ENDER)

        while True:
            mensagem = str(input("Digite algo: ")).encode("utf-8")
            c.sendall(mensagem)

            if mensagem.decode("utf-8") == "/exit":
                break

        resposta = c.recv(4096)
        print(f"Bytes recebidos({len(resposta)} bytes): {repr(resposta)}")
        print(f"Mensagem recebida({len(resposta.decode("utf-8"))} bytes): {resposta.decode("utf-8")}")

    except ConnectionError as e:
        print(f"Erro de conexão: {e}")