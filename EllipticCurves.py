from dmath.dmath import *

import warnings


class ellipticCurves:
    def __init__(self, a, b, p, debug=False):
        """
        Initialize for Elliptic Curve.
        :param a:
        :param b:
        :param p: Must be prime
        :param debug: True to enable Debug, False otherwise
        """
        self.a = (a + p) % p
        self.b = (b + p) % p
        self.p = p
        self.DEBUG = debug

        if (4 * mu(self.a, 3, self.p) + 27 * mu(self.b, 2, self.p)) % self.p == 0:
            raise Exception('Invalid value for a and b. Condition of 4a^3 + 27b^2 is not satisfied.')

    def isInCurve(self, point):
        """
        Check if point in curve
        :param point:
        :return:
        """
        if mu(point[1], 2, self.p) == ((mu(point[0], 3, self.p) + (self.a * point[0]) % self.p + self.b) % self.p):
            return True
        return False

    def findAllPoint(self):
        """
        Find all point in curve.
        Only work fast when p if small
        :return:
        """
        quadratic_residue_dict = {}
        for i in range(0, self.p):
            value = mu(i, 2, self.p)
            if value not in quadratic_residue_dict.keys():
                quadratic_residue_dict[value] = [i]
            else:
                quadratic_residue_dict[value].append(i)
        ans = []
        for x in range(0, self.p):
            leftSide = (mu(x, 3, self.p) + self.a * x + self.b) % self.p
            if leftSide in quadratic_residue_dict.keys():
                for y in quadratic_residue_dict[leftSide]:
                    print(x, y)
                    ans.append((x, y))
        print("Number of point (include O): ", len(ans) + 1)
        print("All quadratic residue mode {}".format(self.p), sorted(quadratic_residue_dict.keys()))

    def add(self, p1, p2):
        """
        Add to point in curve.
        There no guarantee that a sum must be a point in curve.
        :param p1:
        :param p2:
        :return:
        """
        x1 = p1[0]
        y1 = p1[1]

        x2 = p2[0]
        y2 = p2[1]

        if x1 != x2:
            l = ((y2 - y1) * invModulo((x2 - x1 + self.p) % self.p, self.p)[0]) % self.p
            nu = (y1 - (l * x1) % self.p + self.p) % self.p
        elif x1 == x2 and y1 == (-y2 + self.p) % self.p:
            raise Exception('P are inverse of Q. No result found.')
        else:
            l = ((3 * mu(x1, 2, self.p) + self.a) * invModulo((2 * y1) % self.p, self.p)[0]) % self.p
            nu = (y1 - (l * x1) % self.p + self.p) % self.p
        x3 = (mu(l, 2, self.p) - x1 - x2 + 2 * self.p) % self.p
        y3 = ((l * ((x1 - x3 + self.p) % self.p)) % self.p - y1 + self.p) % self.p

        if not self.isInCurve((x3, y3)):
            warnings.warn("Point {},{} is not in curve".format(x3, y3))

        return x3, y3

    def mul(self, p, k):
        """
        Point multiplicative. Calculate k * P
        :param p: point in curve
        :param k: Interger
        :return:
        """
        cur = 1
        sum = p
        while cur < k:
            cur += 1

            sum = self.add(sum, p)
        return sum

    def mulFaster(self, p, k):
        """
        Point multiplicative, but only costs log(k)
        :param p: point in curve
        :param k: Interger
        :return:
        """
        if k == 1:
            return p
        cur = self.mulFaster(p, k // 2)
        cur = self.add(cur, cur)
        if k % 2 == 1:
            cur = self.add(cur, p)
        return cur

    def neg(self, p):
        """
        Find negative of p
        :param p:
        :return:
        """
        return p[0], self.p - p[1]

    def findS(self, root, point):
        """
        Find an number s so that root * s = point
        :param root:
        :param point:
        :return:
        """
        print("Find s so that s * root == point.")
        s = 1
        sum = root
        while sum != point:
            s = s + 1
            sum = self.add(sum, root)
        return s

    def ElGamal_encode(self, plaintext_point, k, P, B):
        """
        ElGamal encoder
        :param plaintext_point:
        :param k:
        :param P:
        :param B:
        :return:
        """
        return self.mulFaster(P, k), self.add(plaintext_point, self.mulFaster(B, k))

    def ElGamal_decode(self, s, M1, M2):
        """
        ElGamal decoder
        :param s:
        :param M1:
        :param M2:
        :return:
        """
        return self.add(M2, self.neg(self.mulFaster(M1, s)))

    def ElGamal_encode_and_decode(self, plaintext_point, s, P, k):
        """
        ElGamal Cryptosystem on Elliptic curve
        :param plaintext_point:
        :param s:
        :param P:
        :param k:
        :return:
        """
        B = self.mulFaster(P, s)

        print("Start ElGamal encode")
        print("Plaintext point: ", plaintext_point)
        print("B Private key: ", s)
        print("B Value: ", B)
        print("Root point P: ", P)
        print("A private key: ", k)

        M1, M2 = self.ElGamal_encode(plaintext_point, k, P, B)

        print("Encoded Value: ", M1, M2)
        print("Encode Complete!")

        print("Start decode")
        M = self.ElGamal_decode(s, M1, M2)
        print("Decoded Value: ", M)
        print("Decoded ElGamal Complete!")

    def Massey_Omura(self, n, M, mA, mB):
        """
        Massey Omura cryptosystem
        :param n: Number of points in Elliptic Curve
        :param M: Plaintext message
        :param mA: private key from A
        :param mB: private key from B
        :return:
        """

        assert gcd(mA, n) == 1, "Invalid value of mA. gcd(mA, n) != 1"
        assert gcd(mB, n) == 1, "Invalid value of mB. gcd(mB, n) != 1"

        M1 = self.mulFaster(M, mA)
        M2 = self.mulFaster(M1, mB)
        M3 = self.mulFaster(M2, invModulo(mA, n)[0])
        M4 = self.mulFaster(M3, invModulo(mB, n)[0])

        print("Value of M1: ", M1)
        print("Value of M2: ", M2)
        print("Value of M3: ", M3)
        print("Value of M4: ", M4)
        print("Check if value of M4 is identical to M:", M4 == M)


try:
    # curve = ellipticCurves(1, 1, 14734520141266665763, False)

    # curve.ElGamal_encode_and_decode((3683630035316666441, 5525445052974999660), 947, (72, 611), 97742)
    curve = ellipticCurves(1, 1, 223, False)
    # curve.findAllPoint()

    curve.Massey_Omura(244, (3, 37), 179, 7)

    # print(curve.isInCurve((217, 606)))

except Exception as e:
    print(e)
