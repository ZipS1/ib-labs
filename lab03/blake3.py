def blake3(data: bytes) -> bytes:
    """
    Упрощенная версия BLAKE3 (только для одного 1K блока).
    Реальный BLAKE3 использует дерево Меркла и параллелизм.
    """
    # Константы
    IV = [
        0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
        0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19
    ]

    # Инициализация состояния (16 слов)
    state = IV.copy() + [0] * 8  # Добавляем 8 нулевых слов

    # Упрощение: работаем с одним блоком
    chunk = data.ljust(1024, b'\x00')

    def compress(chunk, counter=0, flags=0):
        # Перемешивание данных (16 слов по 32 бита)
        msg = [int.from_bytes(chunk[i*4:(i+1)*4], 'little') for i in range(16)]

        # Инициализация состояния
        state = IV.copy() + [0] * 8

        # Добавление сообщения в состояние
        for i in range(16):
            state[i] ^= msg[i]

        # 7 раундов перемешивания
        for _ in range(7):
            # Смешивание столбцов
            for i in range(4):
                a, b, c, d = i, i + 4, i + 8, i + 12
                state[a], state[b], state[c], state[d] = (
                    state[a] ^ state[b],
                    state[c] ^ state[d],
                    (state[a] + state[b]) & 0xFFFFFFFF,
                    (state[c] + state[d]) & 0xFFFFFFFF
                )

            # Смешивание диагоналей
            for i in range(4):
                a, b, c, d = i, (i + 1) % 4 + 4, (i + 2) % 4 + 8, (i + 3) % 4 + 12
                state[a], state[b], state[c], state[d] = (
                    state[a] ^ state[b],
                    state[c] ^ state[d],
                    (state[a] + state[b]) & 0xFFFFFFFF,
                    (state[c] + state[d]) & 0xFFFFFFFF
                )

        # Финализация
        return [state[i] ^ IV[i] for i in range(8)]

    # Вычисление хэша
    hash_words = compress(chunk)
    return b''.join(word.to_bytes(4, 'little') for word in hash_words)

# Пример использования
data = b"Hello, World!"
print("BLAKE3 hash:", blake3(data).hex())
