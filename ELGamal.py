from dmath.dmath import *
from dstring.dstring import *


def ElGamal(p, alpha, a, k, x):
    print("Value of p: ", p)
    print("Value of alpha: ", alpha)
    print("Value of a: ", a)
    print("Value of k: ", k)

    # Calc beta.
    beta = mu(alpha, a, p)
    # Show public key: K' = (p, alpha, beta)
    # Hidden private ket: K" = a.

    def encode(plaintext):
        return mu(alpha, k, p), (plaintext * mu(beta, k, p)) % p

    def decode(y1, y2):
        return (y2 * invModulo(mu(y1, a, p), p)[0]) % p

    def calc_a_if_k_shown(plaintext, k, y1, y2):
        return ((plaintext - (k * y2) % (p - 1) + (p - 1)) * invModulo(y1, p - 1)[0]) % (p - 1)

    plaintext = string2int(x, p)
    y1, y2 = encode(plaintext)

    print("Value of beta: ", beta)
    print("Cipher Text: ", y1, y2)

    print('....')
    actual_plaintext = decode(y1, y2)
    print("Actual Plaintext: ", actual_plaintext)
    print("Actual String: ", int2string(actual_plaintext))
    print("Expected Plaintext: ", plaintext)
    print("Expected String: ", int2string(plaintext))
    print('....')
    print("Calc a if know k and plain: ", calc_a_if_k_shown(plaintext, k, y1, y2))
    print("Expected of a: ", a)
    assert actual_plaintext == plaintext


ElGamal(10089886811898868001, 2, 1234567890123456789, 9876543210987654321, "HOCHIMINH")
