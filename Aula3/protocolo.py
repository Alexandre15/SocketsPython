import socket
import struct

CABECALHO = struct.Struct("!I")
MAX_FRAME = 1_048_576

def receberEx(sock, qtd, perm=False):
    """Recebe exatamente N bytes ou identifica uma conexão incompleta."""
    dados = bytearray()

    while len(dados) < qtd:
        bloco = sock.recv(qtd - len(dados))

        if not bloco:
            if perm and not dados:
                return None
            raise ConnectionError("[!] Conexão encerrada antes de completar os dados.")

        dados.extend(bloco)
    return bytes(dados)

def enviarF(sock: socket.socket, payload):
    """Recebe um cabeçalho e exatamente o tamanho de conteúdo informado."""
    if len(payload) > MAX_FRAME:
        raise ValueError("[!] Mensagem acima do tamanho permitido.")

    cabecalho = CABECALHO.pack(len(payload))
    sock.sendall(cabecalho + payload)

def receberF(sock: socket.socket):
    """Recebe um cabeçalho e exatamente o tamanho de conteúdo informado."""
    cabecalho = receberEx(sock, CABECALHO.size, True)

    if cabecalho is None:
        return None

    (tamanho,) = CABECALHO.unpack(cabecalho)

    if tamanho > MAX_FRAME:
        raise ValueError("[!] Servidor ou cliente anunciou tamanho excessivo.")
    return receberEx(sock, tamanho)