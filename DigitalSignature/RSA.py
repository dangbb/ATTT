from dmath.dmath import *
from dstring.dstring import *

class RsaSender():
    def __init__(self, p, q, a, h_x = lambda x: x):
        self.n = p * q
        self.phi = (p - 1) * (q - 1)
        self.a = a
        if gcd(self.a, self.phi) > 1:
            raise Exception("a not coprime with phi")
        else:
            self.b = invModulo(a, self.phi)[0]
        self.h_x = h_x

        print("Khóa công khai của người gửi: b={}, n={}".format(self.b, self.n))

    def encode(self, x, receiver):
        print("Giá trị của bản rõ: ", x)
        ciphertext = receiver.encode(x)
        signature = mu(self.h_x(x), self.a, self.n)
        print("Giá trị của chữ kí được mã hóa bởi người gửi: {}^{} mod {} = {}".format(self.h_x(x), self.a, self.n, signature))

        return ciphertext, signature

    def decode(self, signature):
        decode_signature = mu(signature, self.b, self.n)
        print("Chữ kí sau khi giải mã bởi khóa công khai của người gửi: {}^{} mod {} = {}".format(signature, self.b, self.n, decode_signature))
        return decode_signature


class RsaReceiver():
    def __init__(self, p, q, a):
        self.n = p * q
        self.phi = (p - 1) * (q - 1)
        self.a = a
        if gcd(self.a, self.phi) > 1:
            raise Exception("a not coprime with phi")
        else:
            self.b = invModulo(a, self.phi)[0]

        print("Khóa công khai của người nhận: b={}, n={}".format(self.b, self.n))

    def encode(self, plaintext):
        ciphertext = mu(plaintext, self.b, self.n)
        print("Giá trị bản rõ được mã hóa bởi khóa công khai từ người nhận: {}^{} mod {} = {}".format(plaintext, self.b, self.n, ciphertext))
        return ciphertext

    def decode(self, message, sender):
        print("Giá trị của tin nhắn được mã hóa: ", message)
        plaintext = mu(message[0], self.a, self.n)
        signature = message[1]

        print("Bản rõ thông tin tìm được: {}^{} mod {} = {}".format(message[0], self.a, self.n, plaintext))
        decode_signature = sender.decode(signature)

        if decode_signature == plaintext:
            print("Bản rõ và chữ kí trùng nhau ({} == {})".format(plaintext, decode_signature))
        else:
            print("Bản rõ và chữ kí không trùng nhau ({} != {})".format(plaintext, decode_signature))

        return plaintext


class RsaSignature():
    def __init__(self, sender, receiver):
        self.sender = sender
        self.receiver = receiver

    def messaging(self, x):
        encoded_message = self.sender.encode(x, self.receiver)

        print("------------------------------------------------")

        plaintext = self.receiver.decode(encoded_message, self.sender)

        print("------------------------------------------------")

        if plaintext == x:
            print("Giá trị giải mã của bản rõ bằng thông tin từ người gửi, {} == {}".format(plaintext, x))
        else:
            print("Giá trị giải mã của bản rõ khác thông tin từ người gửi, {} != {}".format(plaintext, x))

        print("Xâu sau khi giải mã: ", int2string(plaintext))



if __name__ == "__main__":
    sender = RsaSender(
        2074722246773485207821695222107608587480996474721117292752992589912196684750549658310084416732550077,
        2367495770217142995264827948666809233066409497699870112003149352380375124855230068487109373226251983,
        1814159566819970307982681716822107016038920170504391457462563485198126916735167260215619523429714031
    )
    receiver = RsaReceiver(
        5371393606024775251256550436773565977406724269152942136415762782810562554131599074907426010737503501,
        6513516734600035718300327211250928237178281758494417357560086828416863929270451437126021949850746381,
        5628290459057877291809182450381238927697314822133923421169378062922140081498734424133112032854812293
    )
    system = RsaSignature(sender, receiver)

    decode_str = string2int("CAUEMTIMDUOCNGUOITINHNHUTOIDAYEUEM",
                            5371393606024775251256550436773565977406724269152942136415762782810562554131599074907426010737503501 * 6513516734600035718300327211250928237178281758494417357560086828416863929270451437126021949850746381)
    system.messaging(decode_str)



