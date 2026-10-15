import socket

from protocolo import enviarF, receberF

HOST = "127.0.0.1"
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)

    print(f"[*] Servidor escutando em {HOST}:{PORT}")

    while True:
        con, ender = s.accept()
        print(f"Cliente conectado: {ender[0]}:{ender[1]}")

        with con:
            try:
                while True:
                    payload = receberF(con)

                    if payload is None:
                        break
                    try:
                        mensagem = payload.decode("utf-8")
                    except UnicodeDecodeError:
                        enviarF(con, b"ERRO: texto UTF-8 invalido")
                        continue
                    print(f"[!] Recebido: {mensagem!r}")

                    resposta = f"ECO: {mensagem}".encode("utf-8")
                    enviarF(con, resposta)
            except (OSError, ValueError) as e:
                print(f"[x] Conexão encerrada com erro: {e}")