import json
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

def assinar_dicionario(dicionario, path_to_private_key, path_to_encrypted_dicionario):
    try:
        with open(path_to_private_key, "rb") as private_key_file:
            private_key = serialization.load_pem_private_key(
                private_key_file.read(),
                password=None,
                backend=default_backend()
            )

        encrypted_data = json.dumps(dicionario).encode('utf-8')
        signature = private_key.sign(
            encrypted_data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        with open(path_to_encrypted_dicionario, "r+") as encrypted_file:
            # Posicionar o cursor no final do arquivo para adicionar a assinatura
            encrypted_file.seek(0, 2)
            encrypted_file.write("\n")
            encrypted_file.write("Signature:")
            encrypted_file.write(signature.hex())

        print("Assinatura gerada e adicionada ao arquivo:", path_to_encrypted_dicionario)

    except IOError:
        print("Erro ao carregar a chave privada.")
    except:
        print("Erro ao assinar o dicionário.")