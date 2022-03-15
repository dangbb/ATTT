from dmath.dmath import *
from dstring.dstring import *


def rsa_encode(plain, e, mod):
    if isinstance(plain, str):
        plain = string2int(plain, mod)
        print("String to int: ", plain)
    cipher = mu(plain, e, mod)
    print("Encoded value: ", cipher)
    cipher_str = int2string(cipher)
    print("Encoded string: ", cipher_str)
    return cipher


def rsa_decode(cipher, d, mod):
    plain = mu(cipher, d, mod)
    print("Decoded value: ", plain)
    msg = int2string(plain)
    print("Decoded string: ", msg)
    return msg


def rsaE2E(plain, p, q, e):
    n = p * q
    print("Value of n: ", n)
    if gcd(e, (p-1)*(q-1)) != 1:
        print("value of e is invalid!!")
        return
    d, _ = invModulo(e, (p-1)*(q-1))
    print("Value of d: ", d)

    cipher = rsa_encode(plain, e, n)
    rsa_decode(cipher, d, n)


if __name__ == "__main__":
    rsaE2E("NGOHAIFANG",
           22953686867719691230002707821868552601124472329079,
           30762542250301270692051460539586166927291732754961,
           48112959837082048697)