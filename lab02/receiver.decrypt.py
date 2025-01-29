# decrypt.py
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.backends import default_backend

def decrypt_file():
    # Загрузка закрытого ключа
    with open("private_key.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None,
            backend=default_backend()
        )

    # Чтение зашифрованного файла
    with open("encrypted.txt", "rb") as f:
        key_len = int.from_bytes(f.read(4), "big")
        encrypted_aes_key = f.read(key_len)
        iv = f.read(16)
        ciphertext = f.read()

    # Дешифровка AES-ключа
    aes_key = private_key.decrypt(
        encrypted_aes_key,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Дешифровка данных
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    # Удаление padding
    unpadder = sym_padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    # Сохранение результата
    with open("decrypted.txt", "wb") as f:
        f.write(plaintext)

if __name__ == "__main__":
    decrypt_file()
