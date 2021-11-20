#!/usr/bin/env python

import random
import math


class User(object):
    def __init__(self, name, bitlen):
        self.name = name
        self.public_alice = get_prime(bitlen)
        self.public_bob = get_prime(bitlen)
        self.private_key = get_prime(bitlen)
        self.full_key = None

    def generate_partial_key(self):
        result = self.public_alice ** self.private_key % self.public_bob
        print(
            f"Сгенерировать частичный ключ {self.name}\t{result} =",
            self.public_alice, "^", self.private_key, "mod", self.public_bob
        )

        return result

    def generate_full_key(self, partial_key_r):
        self.full_key = partial_key_r ** self.private_key % self.public_bob

        print(
            f"Сгенерировать полный ключ {self.name}\t{self.full_key} =",
            partial_key_r, "^", self.private_key, "mod", self.public_bob
        )

    def encode(self, message):
        return "".join([chr(ord(c) ^ self.full_key) for c in message])


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


def exchange_private(alice, bob, eve: User):
    alice.public_bob = bob.public_bob
    bob.public_alice = alice.public_alice
    eve.public_alice = alice.public_alice


def generate_full(alice, bob, eve: User):
    a_partial = alice.generate_partial_key()
    b_partial = bob.generate_partial_key()
    e_partial = eve.generate_partial_key()

    alice.generate_full_key(b_partial)
    bob.generate_full_key(a_partial)
    eve.generate_full_key(a_partial)


message = "Приеду завтра в полдень, Артемов Максим"
bitlen = int(math.log2(max([ord(c) for c in message])))

alice = User("Алиса", bitlen)
bob = User("Боб", bitlen)
eve = User("Ева", bitlen)

print(
    f"Алиса ключи\t публичный {alice.public_alice}, \tприватный {alice.private_key}")
print(f"Боб ключ\t публичный {bob.public_bob}, \tприватный {bob.private_key}")

exchange_private(alice, bob, eve)

print("Обмен публичными ключами")
generate_full(alice, bob, eve)
b_encrypted = bob.encode(message)
print("Зашифровка сообщения\n\t", b_encrypted)

desc_message = alice.encode(b_encrypted)
print("Расшифровка сообщения\n\t", desc_message)

desc_message = eve.encode(b_encrypted)
print("Расшифровка сообщения\n\t", desc_message)
