import socket
from rich import print

HOST = "127.0.0.1"
PORT = 5000
MAX_LIN = 1024

def atenderc(con, end):
    buffer = bytearray()

    print(f"[green][!] Cliente conectado:[/] [blue]{end[0]}:{end[1]}[/]")

    with con:
        while True:
            dados = con.recv(4096)

            if not dados:
                if buffer:
                    print("[red][x] Conexão encerrada com mensagem incompleta.")
                break

            buffer.extend(dados)

            while True:
                try:
                    fim = buffer.index(b"\n")
                except ValueError:
                    if len(buffer) > MAX_LIN:
                        print("[yellow][!] Mensagem excedeu o limite.")
                        return
                    break
                
                mensagem_bytes = bytes(buffer[:fim])
                del buffer[:fim + 1]

                if len(mensagem_bytes) > MAX_LIN:
                    print("[yellow][!] Mensagem excedeu o limite.")
                    return

                try:
                    mensagem = mensagem_bytes.decode("utf-8")
                except UnicodeDecodeError:
                    con.sendall("[red][x] ERRO: [blue]UTF-8[/] inválido!\n".encode("utf-8"))
                    continue
                print(f"[!] Recebido: {mensagem!r}")

                resposta = f"[?] ECO: {mensagem}\n"
                con.sendall(resposta.encode("utf-8"))
    print(f"Cliente desconectado: {end}")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)

    print(f"[*] Escutando em {HOST}:{PORT}")
    
    conexao, endereco = s.accept()
    atenderc(conexao, endereco)