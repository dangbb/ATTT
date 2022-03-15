from dmath.dmath import *
from dstring.dstring import *


def pollard(n, b):
    # p is a prime factor of n
    # q is a prime factor of p - 1

    # if all q smaller than b
    # then p - 1 | b!

    # a = 2^(b!) = 2^(p - 1) = 1 (mod p)
    a = 2
    for i in range(2, b + 1):
        a = mu(a, i, n)

    print("Value of a: ", a)

    # p | a - 1
    # p | n

    # => p = gcd(n, a - 1)
    p = gcd(n, a - 1)

    print (p)
    print (n // p)
    print (p * (n // p))


if __name__ == "__main__":
    pollard(15770708441, 180)