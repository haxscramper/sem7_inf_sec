#!/usr/bin/env python

import random, math

def is_prime(n: int) -> bool:
    if n > 1:
        for i in range(2, int(n/2)+1):
            if (n % i) == 0:
                return False

        else:
            return True

def get_prime(n: int) -> int:
    while True:
        range_start = int("1" + "0" * (n), 2)
        range_end = int("1" + "1" * (n), 2)
        number = random.randint(range_start, range_end)
        if is_prime(number):
            return number

def RSA(p, q: int):
    n = p * q
    z = (p - 1) * (q - 1)
    e = 0
    for i in range(2, z):
        if math.gcd(i, z) == 1:
            e = i
            break
    d = 0
    for i in range(z):
        x = 1+(i*z)
        if x % e == 0:
            d = int(x / e)
            break
    return [e, n], [d, n]


def encrypt(message: str, key: int) -> list[int]:
    return [pow(ord(m), key[0]) % key[1] for m in message]

def decrypt(message: str, key: int) -> str:
    return "".join([chr(pow(m, key[0]) % key[1]) for m in message])

public_key, private_key = RSA(get_prime(8), get_prime(8))

print("Публичный ключ: ", public_key)
print('Приватный ключ: ', private_key)

msg = encrypt("Пересланное сообщение", public_key)
print("Зашифрованное: ", msg)
print("Расшифрованное: ", decrypt(msg, private_key))