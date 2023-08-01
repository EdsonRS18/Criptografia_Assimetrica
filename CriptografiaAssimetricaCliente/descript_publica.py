import json
import shutil
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
def verificar_assinatura(path_to_encrypted_dicionario, path_to_public_key):
    try:
        with open(path_to_public_key, "rb") as public_key_file:
            public_key = serialization.load_pem_public_key(
                public_key_file.read(),
                backend=default_backend()
            )

        signature = None
        encrypted_dicionario_lines = []
        with open(path_to_encrypted_dicionario, "r") as encrypted_file:
            for line in encrypted_file:
                if line.strip().startswith("Signature:"):
                    signature = line.strip().split("Signature:", 1)[1].strip()
                else:
                    encrypted_dicionario_lines.append(line)

        if signature is None:
            print("Assinatura não encontrada no arquivo.")
            return

        encrypted_dicionario = json.loads("".join(encrypted_dicionario_lines))
        signature = bytes.fromhex(signature)

        encrypted_data = json.dumps(encrypted_dicionario).encode('utf-8')
        try:
            public_key.verify(
                signature,
                encrypted_data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            print("Assinatura verificada com sucesso.")
            # Remover a assinatura verificada do arquivo e restaurar a versão anterior
            shutil.move(path_to_encrypted_dicionario, path_to_encrypted_dicionario + ".bak")
            with open(path_to_encrypted_dicionario, "w") as encrypted_file:
                encrypted_file.write("".join(encrypted_dicionario_lines))
        except:
            print("Assinatura inválida ou erro na verificação.")
            # Restaurar o conteúdo original do arquivo, caso a verificação falhe
            with open(path_to_encrypted_dicionario, "w") as encrypted_file:
                encrypted_file.write("".join(encrypted_dicionario_lines))
    except IOError:
        print("Erro ao carregar a chave pública.")