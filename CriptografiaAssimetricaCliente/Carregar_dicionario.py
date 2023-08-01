import json

# Função para carregar dicionários de criptografia de um arquivo
def carregar_dicionarios_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, 'r') as arquivo:
            dicionarios_serializados = json.load(arquivo)

        dicionarios = []
        for dicionario_serializado in dicionarios_serializados:
            dicionario = {}
            for chave, valor in dicionario_serializado.items():
                dicionario[chave] = valor
            dicionarios.append(dicionario)

        print("Dicionários carregados com sucesso.")
        return dicionarios
    except IOError:
        print("Erro ao carregar os dicionários.")
        return []