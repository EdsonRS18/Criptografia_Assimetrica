import base64
import json
import shutil
import socket
import random
import itertools
from cript_privada import assinar_dicionario
from descript_publica import verificar_assinatura

from menu import exibir_menu
from Gerar_chaves import gerar_chaves_arquivos #1
from Simetrica import criptografar_mensagem, descriptografar_mensagem, exibir_dicionarios #2,3,4
from Download import baixar_arquivo #5
from Upload import enviar_arquivo #6
from Carregar_dicionario import carregar_dicionarios_arquivo # 7
from Gerar_dicionario import gerar_dicionarios #8
from criptografia_publica import criptografar_dicionario # 9
from Descriptografar_privada import  descriptografar_dicionarios #9
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


#C:/Users/edson/OneDrive/Documentos/CriptografiaAssimetricaCliente/edson_chave_publica.pem
#C:/Users/edson/OneDrive/Documentos/CriptografiaAssimetricaCliente/edson_chave_privada.pem
#C:/Users/edson/OneDrive/Documentos/CriptografiaAssimetricaCliente/a.json

#C:/Users/edson/OneDrive/Documentos/CriptografiaAssimetricaCliente/nathan_chave_privada.pem
#C:/Users/edson/OneDrive/Documentos/CriptografiaAssimetricaCliente/nathan_chave_publica.pem





# Função para criar dicionários de criptografia e salvá-los com o nome fornecido pelo usuário





def main():
    exibir_menu()  # Exibir o menu assim que o programa começar

    dicionarios = []
    dicionarios_iter = None

    host = '192.168.0.101'  # Substitua isso pelo endereço IP ou nome do servidor
    port = 5000

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))

        while True:
            exibir_menu()
 

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                # Exemplo de uso da função
                nome_cliente = input("Digite o nome do cliente: ")
                gerar_chaves_arquivos(nome_cliente)

            elif opcao == "2":
                if dicionarios:
                    mensagem = input("Digite a mensagem que você deseja criptografar: ")
                    mensagem_criptografada = criptografar_mensagem(mensagem, dicionarios)
                    print("Mensagem criptografada:", mensagem_criptografada)
                else:
                    print("Nenhum dicionário encontrado. Crie os dicionários primeiro.")

            elif opcao == "3":
                if dicionarios:
                    mensagem_criptografada = input("Digite a mensagem criptografada recebida: ")
                    mensagem_original = descriptografar_mensagem(mensagem_criptografada, dicionarios)
                    print("Mensagem original:", mensagem_original)
                else:
                    print("Nenhum dicionário encontrado. Crie os dicionários primeiro.")

            elif opcao == "4":
                if dicionarios:
                    exibir_dicionarios(dicionarios)
                else:
                    print("Nenhum dicionário encontrado. Crie os dicionários primeiro.")

            elif opcao == "5":
                
                    nome_arquivo = input("Digite o nome do arquivo para baixar: ")
                    baixar_arquivo(sock, nome_arquivo)
                
            elif opcao == "6":
                    caminho_arquivo = input("Digite o caminho do arquivo para upload: ")
                    enviar_arquivo(sock, caminho_arquivo)

            elif opcao == "7":  # Nova opção para carregar dicionário do arquivo
                nome_arquivo = input("Digite o nome do arquivo do dicionário para carregar: ")
                dicionarios = carregar_dicionarios_arquivo(nome_arquivo)
                dicionarios_iter = itertools.cycle(dicionarios)

            elif opcao == "8":
                
                num_dicionarios = int(input("Digite o número de dicionários que você deseja criar: "))
                min_digitos = int(input("Digite o número mínimo de dígitos para cada dicionário: "))
                max_digitos = int(input("Digite o número máximo de dígitos para cada dicionário: "))
                dicionarios = gerar_dicionarios(num_dicionarios, min_digitos, max_digitos)
                dicionarios_iter = itertools.cycle(dicionarios)
            
            elif opcao == "9":
                nome_arquivo_dicionario_completo = input("Digite o caminho do arquivo do dicionário: ")
                path_to_public_key = input("Digite o caminho do arquivo da chave pública: ")

                try:
                    with open(nome_arquivo_dicionario_completo, 'r') as arquivo_dicionario:
                        dicionarios = json.load(arquivo_dicionario)

                    encrypted_dicionarios = criptografar_dicionario(dicionarios, path_to_public_key)

                    with open(nome_arquivo_dicionario_completo, 'w') as arquivo_dicionario:
                        json.dump(encrypted_dicionarios, arquivo_dicionario)

                except IOError:
                    print("Erro ao carregar ou salvar o arquivo do dicionário.")
   

            elif opcao == "10":
                # Example usage:
                path_to_encrypted_dicionarios = input("Digite o caminho do arquivo dos dicionários criptografados: ")
                path_to_private_key = input("Digite o caminho do arquivo da chave privada: ")

                descriptografar_dicionarios(path_to_encrypted_dicionarios, path_to_private_key)

            elif opcao == "11":

                path_to_encrypted_dicionario = input("Digite o caminho para o arquivo com o dicionário criptografado: ")
                path_to_private_key = input("Digite o caminho para a chave privada: ")

                with open(path_to_encrypted_dicionario, 'r') as encrypted_file:
                    encrypted_dicionario = json.load(encrypted_file)

                assinar_dicionario(encrypted_dicionario, path_to_private_key, path_to_encrypted_dicionario)
                
            elif opcao == "12":
                path_to_encrypted_dicionario = input("Digite o caminho para o arquivo com o dicionário criptografado: ")
                path_to_public_key = input("Digite o caminho para a chave pública: ")

                verificar_assinatura(path_to_encrypted_dicionario, path_to_public_key)

            elif opcao == "0":
                break
            else:
                print("Opção inválida. Tente novamente.")

    
            

    except Exception as e:
        print("Erro:", e)
    finally:
        sock.close()


if __name__ == "__main__":
    main()