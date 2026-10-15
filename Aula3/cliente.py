import socket

from protocolo import enviarF, receberF

HOST = "127.0.0.1"
PORT = 5000

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
        c.settimeout(5)
        c.connect((HOST, PORT))

        print("[-] Conectado. Digite /sair para terminar.")

        while True:
            texto = input("> ")
            if texto == "/sair":
                break

            payload = texto.encode("utf-8")
            enviarF(c, payload)
            resposta = receberF(c)
            if resposta is None:
                print("[!] O servidor encerrou a conexão.") # gittest
                break

            print(f"[SERVER] {resposta.decode("utf-8")}")
except (OSError, ValueError) as e:
    print(f"Erro de comunicação: {e}")
