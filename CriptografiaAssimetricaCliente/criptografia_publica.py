import json
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

def criptografar_dicionario(dicionarios, path_to_public_key):
    try:
        with open(path_to_public_key, "rb") as public_key_file:
            public_key = serialization.load_pem_public_key(
                public_key_file.read(),
                backend=default_backend()
            )

        encrypted_dicionarios = []
        for dicionario in dicionarios:
            encrypted_dicionario = {}
            for chave, valor in dicionario.items():
                chave_bytes = chave.encode("utf-8")
                valor_bytes = valor.encode("utf-8")
                encrypted_chave = public_key.encrypt(
                    chave_bytes,
                    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
                )
                encrypted_valor = public_key.encrypt(
                    valor_bytes,
                    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
                )
                encrypted_dicionario[encrypted_chave.hex()] = encrypted_valor.hex()

            encrypted_dicionarios.append(encrypted_dicionario)

        return encrypted_dicionarios
    except IOError:
        print("Erro ao carregar a chave pública.")
        return []