from EllipticCurves import *
from dstring.dstring import *

class EllipticSender:
    def __init__(self, a, b, p, A, q, hash, mA):
        self.curve = ellipticCurves(a, b, p)
        self.p = p
        self.A = A
        self.d = 7
        self.B = self.curve.mulFaster(self.A, self.d)
        self.q = self.curve.findAllPoint()

        self.hash = lambda x : hash(x)

        self.k = 10
        self.invK = invModulo(self.k, q)[0]

        self.mA = mA
        self.invmA = invModulo(self.mA, self.q)[0]

        print("Khóa công khai của người gửi:")
        print("E: y^2 = x^3 + {} * x + {} mod {}".format(a, b, p))
        print("A = {}".format(self.A))
        print("B = {}.{} = {}".format(self.d, self.A, self.B))
        print("Số bậc của đường cong: q = {}".format(self.q))

        print("Khóa bí mật của người gửi: ")
        print("d = {}".format(self.d))
        print("mA = {}".format(self.mA))

        print("HỆ CHỮ KÝ SỐ KIỂU ĐỨC TRÊN ĐƯỜNG CONG ELLIPTIC")
        print("Khóa công khai từ người gửi:")
        self.Q = self.curve.mulFaster(self.A, invModulo(self.d, self.q)[0])
        print("Khóa công khai của người gửi:")
        print("E: y^2 = x^3 + {} * x + {} mod {}".format(a, b, p))
        print("A = {}".format(self.A))
        print("Q = ({}^-1 mod {}) * {} = {}".format(self.d, self.q, self.A, self.Q))
        print("Số bậc của đường cong: q = {}".format(self.q))
        print("Khóa riêng của người gửi:")
        print("Giá trị của d = {}".format(self.d))

    def encodeElgamal(self, message, receiver):
        kA = self.curve.mulFaster(self.A, self.k)
        r = kA[0] % self.q
        s = ((self.hash(message[0]) + self.d * r) * self.invK) % self.q
        print("Giá trị của kA = {}.{} = {}".format(self.k, self.A, kA))
        print("Giá trị của r: {} mod {} = {}".format(kA[0], self.q, r))
        print("Giá trị của x = {}".format(self.hash(message[0])))
        print("Giá trị của k^-1 = {}".format(self.invK))
        print("Giá trị của s: ({} + {} * {}) * {}^-1 mod {} = {}".format(message[0], self.d, r, self.invK, self.q, s))

        M1, M2 = receiver.encodeElgamal(message)

        print("Người gửi gửi tập tin cho người nhận: {}, {}".format((M1, M2), (r, s)))

        return M1, M2, r, s

    def decodeElgamal(self, message, r, s):
        hash = self.hash(message)
        print("Giá trị của x = {}".format(message, self.hash(message)))
        w = invModulo(s, self.q)[0]
        print("Giá trị của w = {}^-1 mod {} = {}".format(s, self.q, w))

        u1 = (w * hash) % self.q
        print("Giá trị của u1 = {} * {} mod {} = {}".format(w, hash, self.q, u1))
        u2 = (w * r) % self.q
        print("Giá trị của u2 = {} * {} mod {} = {}".format(w, r, self.q, u2))
        P = self.curve.add(
            self.curve.mulFaster(self.A, u1),
            self.curve.mulFaster(self.B, u2)
        )
        print("Giá trị của P = {}.{} + {}.{} = {}".format(u1, self.A, u2, self.B, P))
        print("Kiểm tra chữ ký có đúng hay không: P[0] có bằng r hay không")
        if P[0] == r:
            print("{} == {}, giá trị chữ kí là hợp lệ".format(P[0], r))
        else:
            print("{} != {}. Giá trị chữ kí là không hợp lệ".format(P[0], r))

    def encodeOmura(self, M):
        res = self.curve.mulFaster(M, self.mA)
        print("Người gửi mã hóa bằng khóa bí mật: M1 = {}.{} = {}".format(self.mA, M, res))
        return res

    def decodeOmura(self, M):
        res = self.curve.mulFaster(M, self.invmA)
        print("Người gửi giải mã bằng khóa bí mật: M3 = {}.{} = {}".format(self.invmA, M, res))
        return res

    def encodeSignature(self, message):
        print("Xây dựng chữ ký dựa trên bản rõ: M = {}".format(message))
        kA = self.curve.mulFaster(self.A, self.k)
        print("Giá trị k được chọn: {}".format(self.k))
        print("Giá trị của kG = {}.{} = {}".format(self.k, self.A, kA))

        x1 = kA[0]
        if x1 == 0:
            print("KHÔNG ĐƯỢC! x1 == 0")
        r = x1 % self.q
        print("Giá trị của r = kA[0] mod n = {} mod {}".format(x1, self.q))

        h = message
        s = ((self.k * r - h + self.q) * self.d) % self.q
        print("Giá trị của s = (kr - h) * d mod n = ({}.{} - {}) * {} mod {} = {}".format(self.k, r, h, self.d, self.q, s))

        if s == 0:
            print("KHÔNG ĐƯỢC! s == 0")
        print("Giá trị của chữ ký được mã hóa tương ứng với M = {} là (r, s) = {}".format(message, (r, s)))
        return r, s


    def decodeSignature(self, message, r, s):
        w = invModulo(r, self.q)[0]
        print("Giá trị của w = r^-1 % n = {}^-1 mod {} = {}".format(r, self.q, w))
        h = message
        print("Giá trị của h = {}".format(message))

        u1 = (h * w) % self.q
        u2 = (s * w) % self.q
        print("Giá trị của u1 = hw % n = {}.{} mod {} = {}".format(h, w, self.q, u1))
        print("Giá trị của u2 = sư % n = {}.{} mod {} = {}".format(s, w, self.q, u2))

        T = self.curve.add(self.curve.mulFaster(self.A, u1), self.curve.mulFaster(self.Q, u2))
        print("Tính giá trị điểm T = u1.g + u2.Q = {}.{} + {}.{} = {}".format(u1, self.A, u2, self.Q, T))
        v = T[0]
        print("Giá trị của v = T[0] = {}".format(v))

        if v == r:
            print("Giá trị v == r ({} == {}). Chữ ký là hợp lệ".format(v, r))
        else:
            print("Giá trị v != r ({} != {}). Chữ ký là không hợp lệ".format(v, r))



class EllipticReceiver:
    def __init__(self, a, b, p, A, q, hash, mB):
        self.curve = ellipticCurves(a, b, p)
        self.p = p
        self.A = A
        self.s = 7
        self.B = self.curve.mulFaster(self.A, self.s)
        self.q = self.curve.findAllPoint()

        self.hash = lambda x : hash(x)

        self.k = 10
        self.invK = invModulo(self.k, q)[0]

        self.mB = mB
        self.invmB = invModulo(self.mB, self.q)[0]

        print("Khóa công khai của người nhận:")
        print("E: y^2 = x^3 + {} * x + {} mod {}".format(a, b, p))
        print("A = {}".format(self.A))
        print("B = {}.{} = {}".format(self.s, self.A, self.B))
        print("Số bậc của đường cong: q = {}".format(self.q))

        print("Khóa bí mật của người nhận: ")
        print("s = {}".format(self.s))
        print("mB = {}".format(self.mB))

    def encodeElgamal(self, message):
        M1 = self.curve.mulFaster(self.A, self.k)
        M2 = self.curve.add(message, self.curve.mulFaster(self.B, self.k))

        print("Mã hóa tin nhắn")
        print("Tính giá trị của M1 = {}.{} = {}".format(self.k, self.A, M1))
        print("Tính giá trị của M2 = {} + {}.{} = {}".format(message, self.k, self.B, M2))

        return M1, M2

    def decodeElgamal(self, M1, M2, r, s, sender):
        message = self.curve.add(M2, self.curve.neg(self.curve.mulFaster(M1, self.s)))
        print("Giải mã bản rõ: M = {} - {}.{} = {}".format(M2, M1, self.s, message))

        sender.decodeElgamal(message[0], r, s)
        print("Giá trị của tin nhắn sau khi giải mã: ", message)
        return message

    def decodeOmuraSignature(self, message, r, s, sender):
        sender.decodeElgamal(message[0], r, s)
        return message

    def encodeOmura(self, M):
        res = self.curve.mulFaster(M, self.mB)
        print("Người nhận mã hóa bằng khóa bí mật: M2 = {}.{} = {}".format(self.mB, M, res))
        return res

    def decodeOmura(self, M):
        res = self.curve.mulFaster(M, self.invmB)
        print("Người nhận giải mã bằng khóa bí mật: M4 = {}.{} = {}".format(self.invmB, M, res))
        return res


class EllipticSystem:
    def __init__(self, sender, receiver):
        self.sender = sender
        self.receiver = receiver

    def sendMessageElGamal(self, message):
        print("** Tiến hành gửi mã **")
        print("Bản rõ từ người gửi: ", message)
        m1, m2, r, s = self.sender.encodeElgamal(message, self.receiver)
        print("** Người nhận tiến hành giải mã chữ ký **")
        self.receiver.decodeElgamal(m1, m2, r, s, self.sender)

    def sendMessageMassey(self, message):
        print("** Tiến hành gửi mã **")
        print("Bản rõ từ người gửi: ", message)
        _, _, r, s = self.sender.encodeElgamal(message, self.receiver)
        print("** Người gửi mã hóa bản rõ, gửi cho người nhận **")
        M1 = self.sender.encodeOmura(message)
        print("** Người nhận mã hóa thêm gửi lại mã cho người gửi **")
        M2 = self.receiver.encodeOmura(M1)
        print("** Người gửi giải mã một phần, gửi cho người nhận **")
        M3 = self.sender.decodeOmura(M2)
        print("** Người nhận nhận được mã và giải mã bằng khóa kín **")
        M4 = self.receiver.decodeOmura(M3)
        print("** Kiểm tra chữ ký **")
        self.receiver.decodeOmuraSignature(M4, r, s, self.sender)
        print("Kiểm thử giá trị của chữ ký có đúng hay không: ")
        if message == M4:
            print("Tin nhắn được truyền đi chính xác, {} == {}".format(message, M4))
        else:
            print("Tin nhắn không được truyền đi chính xác, {} != {}".format(message, M4))

    def GermanSignature(self, message):
        print("Người gửi tính chữ ký và gửi cho người nhận:")
        r, s = self.sender.encodeSignature(message)
        print("Người nhận nhận được tin nhắn là thực hiện kiểm tra chữ ký:")
        self.sender.decodeSignature(message, r, s)



if __name__ == "__main__":
    sender = EllipticSender(10, 17, 127,  (68, 13), 131, lambda x:x, 19)
    receiver = EllipticReceiver(10, 17, 127,  (68, 13), 131, lambda x:x, 22)
    system = EllipticSystem(sender=sender, receiver=receiver)

    system.GermanSignature(25)