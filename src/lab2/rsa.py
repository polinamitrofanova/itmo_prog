"""
Модуль для реализации алгоритма шифрования RSA.

Этот модуль содержит функции для генерации ключей, шифрования и
дешифрования сообщений с использованием алгоритма RSA.
"""
import random
import typing as tp


def is_prime(n: int) -> bool:
    """Проверяет, является ли число n простым."""
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def gcd(a: int, b: int) -> int:
    """Находит наибольший общий делитель двух чисел a и b."""
    while b:
        a, b = b, a % b
    return a


def multiplicative_inverse(a: int, b: int) -> tuple[int, int, int]:
    """
    Расширенный алгоритм Евклида для нахождения НОД и коэффициентов x и y,
    такие что a * x + b * y = gcd(a, b).
    """
    if a == 0:
        return b, 0, 1

    gcd, x1, y1 = multiplicative_inverse(b % a, a)

    x = y1 - (b // a) * x1
    y = x1

    return gcd, x, y


def generate_keypair(p: int, q: int) -> tp.Tuple[tp.Tuple[int, int], tp.Tuple[int, int]]:
    """Генерирует пару ключей на основе простых чисел p и q."""
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("Both numbers must be prime.")
    elif p == q:
        raise ValueError("p and q cannot be equal")

    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)


    _, d, _ = multiplicative_inverse(e, phi)

    return ((e, n), (d, n))


def encrypt(pk: tp.Tuple[int, int], plaintext: str) -> list[int]:
    """Шифрует сообщение с использованием открытого ключа."""
    e, n = pk
    # Используем pow() с модулем для повышения производительности
    cipher = [pow(ord(char), e, n) for char in plaintext]
    return cipher


def decrypt(pk: tp.Tuple[int, int], ciphertext: list[int]) -> str:
    """Дешифрует зашифрованное сообщение с использованием закрытого ключа."""
    d, n = pk  # Используем закрытый ключ
    # Используем pow() для дешифровки с модулем
    plain = [chr(pow(char, d, n)) for char in ciphertext]
    return "".join(plain)


if __name__ == "__main__":
    print("RSA Encrypter/Decrypter")

    while True:
        try:
            p = int(input("Enter a prime number (17, 19, 23, etc): "))
            if not is_prime(p):
                print(f"{p} is not a prime number. Please try again.")
                continue

            q = int(input("Enter another prime number (Not one you entered above): "))
            if not is_prime(q):
                print(f"{q} is not a prime number. Please try again.")
                continue

            if p == q:
                print("p and q cannot be equal. Please try again.")
                continue

            break

        except ValueError:
            print("Invalid input. Please enter valid prime numbers.")

    print("Generating your public/private keypairs now . . .")
    public, private = generate_keypair(p, q)
    print("Your public key is", public)
    print("and your private key is", private)

    message = input("Enter a message to encrypt with your public key: ")  # Используем открытый ключ
    encrypted_msg = encrypt(public, message)
    print("Your encrypted message is:")
    print(" ".join(map(str, encrypted_msg)))

    print("Decrypting message with private key", private, ". . .")
    decrypted_msg = decrypt(private, encrypted_msg)
    print("Your message is:")
    print(decrypted_msg)
