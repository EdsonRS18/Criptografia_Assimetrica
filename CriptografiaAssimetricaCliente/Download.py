# Função para baixar o arquivo pelo socket
def baixar_arquivo(sock, nome_arquivo):
    sock.sendall(b'DOWNLOAD')
    sock.sendall(nome_arquivo.encode())

    resposta = sock.recv(1024).decode()
    if resposta == 'FILE_FOUND':
        tamanho_arquivo = int(sock.recv(1024).decode())
        with open(nome_arquivo, 'wb') as arquivo:
            tamanho_restante = tamanho_arquivo
            tamanho_buffer = 4 * 1024
            while tamanho_restante > 0:
                dados = sock.recv(min(tamanho_buffer, tamanho_restante))
                arquivo.write(dados)
                tamanho_restante -= len(dados)

        print("Arquivo baixado com sucesso.")
    elif resposta == 'FILE_NOT_FOUND':
        print("Arquivo não encontrado no servidor.")
    else:
        print("Erro durante o download do arquivo.")