import hashlib
import json

def generate_hashes(passwords, hash_algorithms):
    rainbow_table = {}
    for password in passwords:
        rainbow_table[password] = {}
        for algo in hash_algorithms:
            hasher = hashlib.new(algo)
            hasher.update(password.encode('utf-8'))
            rainbow_table[password][algo] = hasher.hexdigest()
    return rainbow_table

def save_rainbow_table(rainbow_table, filename="rainbow_table.json"):
    with open(filename, "w") as file:
        json.dump(rainbow_table, file, indent=4)

def load_rainbow_table(filename="rainbow_table.json"):
    with open(filename, "r") as file:
        return json.load(file)

def find_password(hash_value, filename="rainbow_table.json"):
    rainbow_table = load_rainbow_table(filename)
    for password, hashes in rainbow_table.items():
        if any(hash_value == hash for hash in hashes.values()):
            return password
    return None

def main():
    passwords = ["password123", "helloWorld", "admin", "qwerty", "letmein", "welcome", "123456", "monkey", "football", "iloveyou"]
    hash_algorithms = ["md5", "sha1", "sha256"]
    rainbow_table = generate_hashes(passwords, hash_algorithms)
    save_rainbow_table(rainbow_table)
    print("Радужная таблица успешно создана и сохранена.")

    # Пример поиска пароля по хэшу
    test_hash = input("Введите хэш для поиска: ")
    result = find_password(test_hash)
    if result:
        print(f"Найден пароль: {result}")
    else:
        print("Пароль не найден в таблице.")

if __name__ == "__main__":
    main()
