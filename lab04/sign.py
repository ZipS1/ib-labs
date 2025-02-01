import random
import hashlib

# Параметры эллиптической кривой secp256k1
P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
A = 0
B = 7
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# Функции эллиптической кривой
def inverse_mod(k, p):
    return pow(k, -1, p)

def add_points(P1, P2):
    if P1 is None:
        return P2
    if P2 is None:
        return P1

    x1, y1 = P1
    x2, y2 = P2

    if x1 == x2 and y1 != y2:
        return None

    if x1 == x2:
        m = (3 * x1 * x1 + A) * inverse_mod(2 * y1, P) % P
    else:
        m = (y2 - y1) * inverse_mod(x2 - x1, P) % P

    x3 = (m * m - x1 - x2) % P
    y3 = (m * (x1 - x3) - y1) % P

    return x3, y3

def multiply_point(k, point):
    result = None
    temp = point

    while k:
        if k & 1:
            result = add_points(result, temp)
        temp = add_points(temp, temp)
        k >>= 1

    return result

# Чтение сообщения из файла
with open("message.txt", "r") as f:
    message = f.read().strip()

# Генерация ключей
private_key = random.randint(1, N-1)
public_key = multiply_point(private_key, (Gx, Gy))

# Сохранение ключей в разные файлы
with open("private_key.txt", "w") as f:
    f.write(f"{private_key}\n")

with open("public_key.txt", "w") as f:
    f.write(f"{public_key[0]},{public_key[1]}\n")

# Создание подписи
message_hash = int(hashlib.sha256(message.encode()).hexdigest(), 16)

k = random.randint(1, N-1)
R, _ = multiply_point(k, (Gx, Gy))
r = R % N
s = (inverse_mod(k, N) * (message_hash + r * private_key)) % N

# Сохранение подписи
with open("signature.txt", "w") as f:
    f.write(f"{message}\n{r},{s}\n")

print("Сгенерированы приватный и публичный ключи, подписано сообщение.")
