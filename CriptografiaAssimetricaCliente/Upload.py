import os


def enviar_arquivo(sock, caminho_arquivo):
    nome_arquivo = os.path.basename(caminho_arquivo)
    tamanho_arquivo = os.path.getsize(caminho_arquivo)

    with open(caminho_arquivo, 'rb') as arquivo:
        sock.sendall(b'UPLOAD')
        sock.sendall(nome_arquivo.encode())
        sock.sendall(str(tamanho_arquivo).encode())  # Enviar o tamanho do arquivo

        tamanho_buffer = 4 * 1024
        while True:
            dados = arquivo.read(tamanho_buffer)
            if not dados:
                break
            sock.sendall(dados)

    print("Arquivo enviado com sucesso.")