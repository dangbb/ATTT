from dmath.dmath import *
from dstring.dstring import *

class ElGamalSender():
    def __init__(self, p, a, alpha, k_encode, k_sign):
        """
        :param p:
        :param a:
        :param alpha: must be a primitive element of p.
        """
        self.p = p
        self.alpha = alpha
        self.beta = mu(self.alpha, a, self.p)
        self.a = a
        self.k_encode = k_encode
        self.k_sign = k_sign

        print("Khóa bí mật của người gửi:\na={}\nChọn k mã hóa là {}\nChọn k chữ kí là {}".format(self.a, self.k_encode, self.k_sign))
        print("Khóa công khai của người gửi: p={}, alpha={}, beta={}".format(self.p, self.alpha, self.beta))

    def encode(self, x, receiver):
        x = receiver.modulo(x)
        y1, y2 = receiver.encode(x, self.k_encode)

        signature_gamma = mu(self.alpha, self.k_sign, self.p)
        print("Giá trị chữ ký mã hóa gamma: gamma = {}^{} mod {} = {}".format(self.alpha, self.k_sign, self.p, signature_gamma))
        invK = invModulo(self.k_sign, self.p - 1)[0]
        print("Giá trị nghịch đảo của k kí = {}".format(invK))

        signature_sigma = ((x % (self.p - 1) - (self.a * signature_gamma) % (self.p - 1) + self.p - 1) * invK) % (self.p - 1)
        print("Giá trị chữ ký mã hóa sigma: sigma = ({} - {} * {}) * {} mod {} = {}".format(x, self.a, signature_gamma, invK, self.p - 1, signature_sigma))

        return y1, y2, signature_gamma, signature_sigma

    def decode(self, x, gamma, sigma):
        """
        Decode value of signature
        :param x:
        :param gamma:
        :param sigma:
        :return:
        """
        c1 = (mu(self.beta, gamma, self.p) * mu(gamma, sigma, self.p)) % self.p
        c2 = mu(self.alpha, x, self.p)
        print("Giải mã chữ kí bằng khóa công khai của người gửi:")
        print("c1 = {}^{} * {}^{} mod {} = {}".format(self.beta, gamma, gamma, sigma, self.p, c1))
        print("c2 = {}^{} mod {} = {}".format(self.alpha, x, self.p, c2))
        if c1 == c2:
            print("Giá trị của chữ ký được giải mã là đúng, {} == {}".format(c1, c2))
        else:
            print("Giá trị của chữ ký được giải mã là sai, {} != {}".format(c1, c2))


class ElGamalReceiver():
    def __init__(self, p, a, alpha):
        """

        :param p:
        :param a: must be a primitive element of p.
        :param alpha:
        """
        self.p = p
        self.alpha = alpha
        self.beta = mu(self.alpha, a, self.p)
        self.a = a

        print("Khóa bí mật của người nhận:\na={}".format(self.alpha))
        print("Khóa công khai của người nhận:\np={}\nalpha={}\nbeta={}".format(self.p, self.alpha, self.beta))

    def encode(self, x, k):
        y1 = mu(self.alpha, k, self.p)
        y2 = (x * mu(self.beta, k, self.p)) % self.p

        print("Mã hóa giá trị của bản rõ với k={}".format(k))
        print("y1 = {}^{} mod {} = {}".format(self.alpha, k, self.p, y1))
        print("y2 = {} * {}^{} mod {} = {}".format(x, self.beta, k, self.p, y2))
        return y1, y2

    def decode(self, y1, y2, gamma, sigma, sender):
        x = (y2 * invModulo(mu(y1, self.a, self.p), self.p)[0]) % self.p
        print("Giá trị bản rõ được giải mã: {}*({}^{})^-1 mod {} = {}".format(y2, y1, self.a, self.p, x))
        print("Xâu ký tự được giải mã: ", int2string(x))

        sender.decode(x, gamma, sigma)
        return x

    def modulo(self, x):
        return x % self.p


class ElGamalSystem():
    def __init__(self, sender, receiver):
        self.sender = sender
        self.receiver = receiver

    def messaging(self, message):
        print("Giá trị của bản rõ là: {}".format(message))
        print("-------------- Người gửi mã hóa tin nhắn và gửi giá trị y1, y2, gamma, sigma")
        y1, y2, gamma, sigma = self.sender.encode(message, self.receiver)
        print("Tin nhắn gửi cho người nhận: (y1, y2), (gamma, sigma) = ({}, {}), ({}, {})".format(y1, y2, gamma, sigma))
        print("-------------- Người nhận giải mã tin nhắn và kiểm tra chữ ký")
        return self.receiver.decode(y1, y2, gamma, sigma, self.sender)


if __name__ == "__main__":
    # sender = ElGamalSender(467, 127, 2, 213)
    # receiver = ElGamalReceiver(467, 127, 2, 213)
    # system = ElGamalSystem(sender, receiver)
    # system.messaging(100)

    print("Chiều gửi -------------------------------------------")
    sender = ElGamalSender(
        p=58021664585639791181184025950440248398226136069516938232493687505822471836536824298822733710342250697739996825938232641940670857624514103125986134050997697160127301547995788468137887651823707102007839,
        a=1010, alpha=2, k_encode=213, k_sign=213
    )
    receiver = ElGamalReceiver(
        p=29072553456409183479268752003825253455672839222789445223234915115682921921621182714164684048719891059149763352939888629001652768286998932224000980861127751097886364432307005283784155195197202827350411,
        a=1010,
        alpha=2
    )

    system = ElGamalSystem(sender, receiver)
    plaintext = string2int(
        "CAUEMTIMDUOCNGUOITINHNHUTOIDAYEUEM",
        29072553456409183479268752003825253455672839222789445223234915115682921921621182714164684048719891059149763352939888629001652768286998932224000980861127751097886364432307005283784155195197202827350411
    )
    decoded_text = system.messaging(plaintext)
    print("Xâu sau khi mã hóa: ", int2string(decoded_text))

    # print("Chiều nhận -------------------------------------------")
    # receiver = ElGamalReceiver(1409, 1010, 3)
    # sender = ElGamalSender(2179, 1010, 7, 912, 1009)
    #
    # system = ElGamalSystem(sender, receiver)
    # system.messaging(98)