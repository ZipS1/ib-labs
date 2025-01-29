# encrypt.py
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.backends import default_backend
import os

def encrypt_file():
    # Загрузка открытого ключа
    with open("public_key.pem", "rb") as f:
        public_key = serialization.load_pem_public_key(f.read(), backend=default_backend())

    # Генерация AES-ключа и IV
    aes_key = os.urandom(32)  # AES-256
    iv = os.urandom(16)       # 128-битный IV

    # Шифрование данных
    with open("text.txt", "rb") as f:
        plaintext = f.read()

    # Добавление padding
    padder = sym_padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()

    # Шифрование AES
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    # Шифрование AES-ключа RSA
    encrypted_aes_key = public_key.encrypt(
        aes_key,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Сохранение в файл
    with open("encrypted.txt", "wb") as f:
        f.write(len(encrypted_aes_key).to_bytes(4, "big"))
        f.write(encrypted_aes_key)
        f.write(iv)
        f.write(ciphertext)

if __name__ == "__main__":
    encrypt_file()
