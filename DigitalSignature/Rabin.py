from dmath.dmath import *
from dstring.dstring import *

class Rabin:
    def __init__(self, p, q):
        # private
        self.p = p
        self.q = q

        assert p % 4 == 3
        assert q % 4 == 3

        self.d = (p * q - p - q + 5) / 8

        # public
        self.n = p * q

    def encode(self, x):
        sig = mu(x, self.d, self.n)
        return sig

    def decode(self, x, y):
        if x == (y * y) % self.n:
            print("Giá trị trùng nhau ({} == {}). Chữ ký là hợp lệ.")
        else:
            print("Giá trị không trùng nhau ({} != {}). Chứ ký là không hợp lệ.")

class RabinExtent:
    def __init__(self, p, q):
        # private
        self.p = p
        self.q = q

        assert p % 8 == 3
        assert q % 8 == 7

        self.d = (p * q - p - q + 5) / 8

        print("Khóa kín: p={}, q={}, d={}".format(p, q, self.d))

        # public
        self.n = p * q
        print("Khóa công khai: n={}".format(self.n))
        print("Giá trị của x phải nhỏ hơn: ", (self.n - 6) // 16)

    def encode(self, x, J):
        """

        :param x:
        :param J: Jacobi symbol (m / n)
        http://math.fau.edu/richman/jacobi.htm#:~:text=The%20Jacobi%20symbol%2C%20(m%2F,0%2Fn)%20%3D%200.
        :return:
        """
        m = (16 * x + 6) % self.n

        print("Giá trị của m: ", m)

        if J == 1:
            s = mu(m, self.d, self.n)
        else:
            s = mu(m // 2, self.d, self.n)

        return s

    def decode(self, s):
        m_ = mu(s, 2, self.n)

        print(m_)

        m = 0
        if m_ % 8 == 6:
            m = m_
        elif m_ % 8 == 3:
            m = (2 * m_) % self.n
        elif m_ % 8 == 7:
            m = (self.n - m_ + self.n) % self.n
        elif m_ % 8 == 2:
            m = (2 * (self.n - m_ + self.n)) % self.n

        print(m)

        if m % 16 != 6:
            print("Chữ ký sai, bị bác bỏ do m % 16 != 6")
        else:
            x = ((m - 6) * invModulo(16, self.n)[0]) % self.n
            print("Xác nhận s là chứ kỹ trên văn bản x.")
            print("Giá trị của x là ", x)

if __name__ == "__main__":
    system = RabinExtent(p=19, q=31)
    signature = system.encode(12, 1)
    print("Chữ ký: ", signature)
    system.decode(signature)
