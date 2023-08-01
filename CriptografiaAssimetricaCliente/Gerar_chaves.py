from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

# Função para gerar chaves pública e privada para o Cliente B e salvá-las em arquivos

def gerar_chaves_arquivos(nome_cliente):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    public_key = private_key.public_key()

    # Serializa as chaves para formato PEM
    pem_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    pem_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Salva as chaves em arquivos com o nome do cliente
    with open(f"{nome_cliente}_chave_privada.pem", "wb") as f:
        f.write(pem_private)

    with open(f"{nome_cliente}_chave_publica.pem", "wb") as f:
        f.write(pem_public)

    print("Chaves pública e privada geradas e salvas com sucesso.")

    
