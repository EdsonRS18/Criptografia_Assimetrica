import json
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

def descriptografar_dicionarios(path_to_encrypted_dicionarios, path_to_private_key):
    try:
        # Load the encrypted dictionaries from the provided file
        with open(path_to_encrypted_dicionarios, 'r') as encrypted_file:
            encrypted_dicionarios = json.load(encrypted_file)

        # Load the private key from the provided file
        with open(path_to_private_key, "rb") as private_key_file:
            private_key = serialization.load_pem_private_key(
                private_key_file.read(),
                password=None,
                backend=default_backend()
            )

        # Decrypt the dictionaries using the private key
        decrypted_dicionarios = []
        for encrypted_dicionario in encrypted_dicionarios:
            decrypted_dicionario = {}
            for encrypted_chave_hex, encrypted_valor_hex in encrypted_dicionario.items():
                encrypted_chave = bytes.fromhex(encrypted_chave_hex)
                encrypted_valor = bytes.fromhex(encrypted_valor_hex)
                decrypted_chave = private_key.decrypt(
                    encrypted_chave,
                    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
                )
                decrypted_valor = private_key.decrypt(
                    encrypted_valor,
                    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
                )
                decrypted_dicionario[decrypted_chave.decode("utf-8")] = decrypted_valor.decode("utf-8")

            decrypted_dicionarios.append(decrypted_dicionario)

        # Overwrite the encrypted dictionaries file with the decrypted content
        with open(path_to_encrypted_dicionarios, 'w') as encrypted_file:
            json.dump(decrypted_dicionarios, encrypted_file)

        print("Dicionários descriptografados e salvos com sucesso no arquivo:", path_to_encrypted_dicionarios)
        return decrypted_dicionarios

    except IOError:
        print("Erro ao carregar a chave privada ou descriptografar os dicionários.")
        return []