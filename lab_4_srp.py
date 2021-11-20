from math import gcd
import random
import hashlib


def fast_pow(base, exp, mod):
    if exp == 0:
        return 1
    if exp & 1 == 0:
        r = fast_pow(base, exp // 2, mod)
        return (r * r) % mod
    else:
        return (base % mod * fast_pow(base, exp - 1, mod)) % mod


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


def root(modulo: int) -> int:
    required_set = set(num for num in range(
        1, modulo) if gcd(num, modulo) == 1)
    for g in range(1, modulo):
        actual_set = set(pow(g, powers) %
                         modulo for powers in range(1, modulo))
        if required_set == actual_set:
            return g


def hashval(val: str) -> int:
    return int(hashlib.sha256(val.encode('utf-8')).hexdigest(), 16)


def SRP(password: str) -> int:
    N = 1
    q = 1
    g = 1
    while not is_prime(N):
        q = get_prime(4)
        N = 2*q + 1
        g = root(N)

    salt = random.getrandbits(3)

    secret_key = hashval(str(salt) + password)
    server_verifier = fast_pow(g, secret_key, N)

    a = random.randint(2, 100)
    A = fast_pow(g, a, N)
    if A != 0:
        b = random.randint(2, 100)
        k = 3
        B = (k * server_verifier + fast_pow(g, b, N)) % N
        if B != 0:
            u = hashval(hex(A + B))
            if u != 0:
                client_session_key = fast_pow(
                    (B - k * fast_pow(g, secret_key, N)), (a + u * secret_key),  N)
                client_encode_key = hashval(hex(client_session_key))

                server_session_key = fast_pow(
                    (A * (fast_pow(server_verifier, u, N))), b, N)
                server_encode_key = hashval(hex(server_session_key))

                if client_encode_key == server_encode_key:
                    print("Ключ сессии на сервере: \t", server_session_key)
                    print("Ключ кодирования на сервере: \t", server_encode_key)
                    print("Ключ сессии на клиенте: \t", client_session_key)
                    print("Ключ кодирования на клиенте: \t", client_encode_key)
                    return server_encode_key


print(SRP('123243'))
