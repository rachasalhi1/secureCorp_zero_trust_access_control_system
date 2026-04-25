# crypto_rsa.py

import json

import random

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def mod_inverse(e, phi):
    for d in range(1, phi):
        if (e * d) % phi == 1:
            return d
    return None


def generate_keys():
    p = 61
    q = 53

    n = p * q
    phi = (p - 1) * (q - 1)

    e = 17
    while gcd(e, phi) != 1:
        e += 2

    d = mod_inverse(e, phi)

    return {
        "public_key": (e, n),
        "private_key": (d, n)
    }

keys = generate_keys()
PUBLIC_KEY = keys["public_key"]
PRIVATE_KEY = keys["private_key"]




def encrypt(message, key):
    e, n = key
    return [pow(ord(char), e, n) for char in message]


def decrypt(cipher, key):
    d, n = key
    return ''.join([chr(pow(char, d, n)) for char in cipher])





