import json
import random
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

def gerar_dicionarios(num_dicionarios, min_digitos, max_digitos):
    caracteres = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789áàãâéèêíìîóòõôúùûçÁÀÃÂÉÈÊÍÌÎÓÒÕÔÚÙÛÇ!@#$%&*()-_+=/.,?;: "
    caracteres = caracteres + ' '

    dicionarios = []

    for i in range(num_dicionarios):
        num_digitos = random.randint(min_digitos, max_digitos)
        dicionario = {}

        caracteres_embaralhados = random.sample(caracteres, len(caracteres))

        for j in range(len(caracteres_embaralhados)):
            valor_binario = bin(j)[2:].zfill(num_digitos)

            while valor_binario in dicionario.values():
                j = (j + 1) % len(caracteres_embaralhados)
                valor_binario = bin(j)[2:].zfill(num_digitos)

            dicionario[caracteres_embaralhados[j]] = valor_binario

        dicionarios.append(dicionario)

    nome_arquivo_dicionario = input("Digite o nome para salvar o arquivo do dicionário: ")
    nome_arquivo_dicionario_completo = f"{nome_arquivo_dicionario}.json"

    try:
        with open(nome_arquivo_dicionario_completo, 'w') as arquivo_dicionario:
            json.dump(dicionarios, arquivo_dicionario)
        print("Dicionários criados e salvos com sucesso.")
    except IOError:
        print("Erro ao salvar os dicionários.")
        return []

    return dicionarios