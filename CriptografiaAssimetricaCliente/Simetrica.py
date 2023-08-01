# Função para criptografar uma mensagem usando os dicionários de criptografia
import itertools


def criptografar_mensagem(mensagem, dicionarios):
    mensagem_criptografada = ""
    iterador_dicionarios = itertools.cycle(dicionarios)
    espaco = None

    for letra in mensagem:
        if letra == ' ':
            if espaco is None:
                dicionario = next(iterador_dicionarios)
                espaco = dicionario.get(' ')
                if espaco is None:
                    espaco = dicionario[next(iter(dicionario))]
            mensagem_criptografada += espaco
        else:
            dicionario = next(iterador_dicionarios)
            if letra in dicionario:
                mensagem_criptografada += dicionario[letra]

    return mensagem_criptografada


# Função para descriptografar uma mensagem usando os dicionários de criptografia
def descriptografar_mensagem(mensagem_criptografada, dicionarios):
    mensagem_original = ""
    iterador_dicionarios = itertools.cycle(dicionarios)
    espaco = None

    while mensagem_criptografada:
        dicionario = next(iterador_dicionarios)
        num_bits = len(dicionario[next(iter(dicionario))])

        if mensagem_criptografada[:num_bits] == espaco:
            mensagem_original += ' '
            mensagem_criptografada = mensagem_criptografada[num_bits:]
        else:
            for letra, valor_binario in dicionario.items():
                if mensagem_criptografada[:num_bits] == valor_binario:
                    mensagem_original += letra
                    mensagem_criptografada = mensagem_criptografada[num_bits:]
                    break

    return mensagem_original


    # Função para exibir os dicionários de criptografia
def exibir_dicionarios(dicionarios):
        for i, dicionario in enumerate(dicionarios):
            print(f"Dicionário {i+1}:")
            for chave, valor in dicionario.items():
                print(f"{chave}: {valor}")
            print()
