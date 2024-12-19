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
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def gcd(a: int, b: int) -> int:
    """Находит наибольший общий делитель двух чисел a и b."""
    while b:
        a, b = b, a % b
    return a


def multiplicative_inverse(e: int, phi: int) -> int:
    """Находит мультипликативную обратную величину для e по модулю phi."""
    for d in range(1, phi):
        if (e * d) % phi == 1:
            return d
    raise ValueError("Обратная величина не найдена.")


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

    d = multiplicative_inverse(e, phi)

    return ((e, n), (d, n))


def encrypt(pk: tp.Tuple[int, int], plaintext: str) -> tp.List[int]:
    """Шифрует сообщение с использованием открытого ключа."""
    key, n = pk
    cipher = [(ord(char) ** key) % n for char in plaintext]
    return cipher


def decrypt(pk: tp.Tuple[int, int], ciphertext: tp.List[int]) -> str:
    """Дешифрует зашифрованное сообщение с использованием закрытого ключа."""
    key, n = pk
    plain = [chr((char ** key) % n) for char in ciphertext]
    return "".join(plain)


if __name__ == "__main__":
    print("RSA Encrypter/ Decrypter")

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

    message = input("Enter a message to encrypt with your private key: ")
    encrypted_msg = encrypt(private, message)
    print("Your encrypted message is:")
    print(" ".join(map(lambda x: str(x), encrypted_msg)))

    print("Decrypting message with public key", public, ". . .")
    print("Your message is:")
    print(decrypt(public, encrypted_msg))
