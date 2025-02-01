import hashlib

# Параметры эллиптической кривой
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

# Загрузка ключей и подписи
with open("public_key.txt", "r") as f:
    x, y = map(int, f.readline().strip().split(","))
    public_key = (x, y)

with open("signature.txt", "r") as f:
    lines = f.readlines()
    message = lines[0].strip()
    r, s = map(int, lines[1].strip().split(","))

# Хэширование сообщения
message_hash = int(hashlib.sha256(message.encode()).hexdigest(), 16)

# Проверка подписи
w = inverse_mod(s, N)
u1 = (message_hash * w) % N
u2 = (r * w) % N
P1 = multiply_point(u1, (Gx, Gy))
P2 = multiply_point(u2, public_key)
X, _ = add_points(P1, P2)
v = X % N

if v == r:
    print("Подпись верна!")
else:
    print("Подпись недействительна.")
