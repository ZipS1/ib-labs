def keccak(data: bytes, digest_size: int = 32) -> bytes:
    """
    Упрощенная версия Keccak (SHA-3) с исправленной обработкой блоков.
    """
    # Параметры
    ROUNDS = 12  # В оригинале 24 раунда, сокращено для демонстрации
    BLOCK_SIZE = 136  # 1088 бит для SHA3-256

    # Инициализация состояния (5x5 матрица 64-битных слов)
    state = [[0] * 5 for _ in range(5)]

    # Дополнение данных: pad10*1
    pad_length = (-len(data) - 1) % BLOCK_SIZE
    padded = data + b'\x01' + b'\x00' * pad_length + b'\x80'

    # Функция перестановки (permutation)
    def permute(state):
        for _ in range(ROUNDS):
            # Theta
            C = [state[x][0] ^ state[x][1] ^ state[x][2] ^ state[x][3] ^ state[x][4] for x in range(5)]
            D = [C[(x-1)%5] ^ ((C[(x+1)%5] << 1) | (C[(x+1)%5] >> 63)) for x in range(5)]
            state = [[state[x][y] ^ D[x] for y in range(5)] for x in range(5)]

            # Rho и Pi (упрощенная версия)
            rotations = [
                [0, 36, 3, 41, 18],
                [1, 44, 10, 45, 2],
                [62, 6, 43, 15, 61],
                [28, 55, 25, 21, 56],
                [27, 20, 39, 8, 14]
            ]
            new_state = [[0]*5 for _ in range(5)]
            for x in range(5):
                for y in range(5):
                    new_state[y][(2*x + 3*y) % 5] = (
                        (state[x][y] << rotations[x][y]) |
                        (state[x][y] >> (64 - rotations[x][y]))
                    ) & 0xFFFFFFFFFFFFFFFF
            state = new_state

            # Chi
            for x in range(5):
                row = state[x].copy()
                for y in range(5):
                    state[x][y] = row[y] ^ ((~row[(y+1)%5]) & row[(y+2)%5])

            # Iota (добавление константы)
            state[0][0] ^= 0x0000000000000001
        return state

    # Поглощение (absorb) данных
    for i in range(0, len(padded), BLOCK_SIZE):
        block = padded[i:i+BLOCK_SIZE]
        # Преобразование блока в 64-битные слова
        words = [int.from_bytes(block[j:j+8], 'little') for j in range(0, len(block), 8)]
        # Заполнение состояния
        for idx in range(len(words)):
            x = idx % 5
            y = idx // 5
            state[x][y] ^= words[idx]
        state = permute(state)

    # Выжимание (squeeze) хэша
    hash_bytes = bytearray()
    while len(hash_bytes) < digest_size:
        for y in range(5):
            for x in range(5):
                hash_bytes.extend(state[x][y].to_bytes(8, 'little'))
        state = permute(state)

    return bytes(hash_bytes[:digest_size])

# Пример использования
data = b"Hello, World!"
print("Keccak (SHA-3) hash:", keccak(data).hex())
