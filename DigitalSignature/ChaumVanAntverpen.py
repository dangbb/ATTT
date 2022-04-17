from dmath.dmath import *
from dstring.dstring import *

class AntverpenSigner:
    def __init__(self, p, a, alpha):
        self.p = p
        self.q = (p - 1) // 2
        self.a = a
        self.alpha = alpha
        self.beta = mu(self.alpha, self.a, self.p)

        print("Khóa bí mật:")
        print("a = {}".format(self.a))
        print("Khóa công khai:")
        print("p = {}, alpha = {}, beta = alpha^a mod p = {}".format(self.p, self.alpha, self.beta))

    def sign(self, x):
        signature = mu(x, self.a, self.p)
        print("A ký chữ ký = x^a mod p = {}^{} mod {} = {}".format(
            x, self.a, self.p, signature
        ))
        return signature

    def getPublicKey(self):
        return self.p, self.alpha, self.beta

    def Publictest(self, e1, e2, y):
        c = (mu(y, e1, self.p) * mu(self.beta, e2, self.p)) % self.p
        return c

    def PrivateTest(self, c):
        d = mu(c, invModulo(self.a, self.q)[0], self.p)
        return d

    def PublicCheck(self, x, e1, e2):
        rightSide = (mu(x, e1, self.p) * mu(self.alpha, e2, self.p)) % self.p
        return rightSide

    def checkDeny(self, e1, e2, f1, f2, d, D):
        left = mu(d * mu(self.alpha, self.p - 1 - e2, self.p), f1, self.p)
        right = mu(D * mu(self.alpha, self.p - 1 - f2, self.p), e1, self.p)

        if left == right:
            print("y là chữ ký giả")
        else:
            print("y không là chứ ký giả")


class AntverpenChecker:
    def __init__(self):
        pass

    def checkSignature(self, x, y, e1, e2, signer: AntverpenSigner):
        print("########### CHECK SIGNATURE #############")
        print("Bước 1.")
        p, alpha, beta = signer.getPublicKey()
        print("Giá trị khóa công khai từ A: p={}, alpha={}, beta={}".format(p, alpha, beta))

        print("Giá trị của bản rõ và chữ ký: x = {}, y = {}".format(x, y))
        print("B chọn ngẫu nhiên hai số e1 = {}, e2 = {}".format(e1, e2))

        c = (mu(y, e1, p) * mu(beta, e2, p)) % p
        print("Giá trị của c = y^(e1).beta^(e2) mod p= {}^{}.{}^{} mod {}= {}".format(
            y, e1, beta, e2, p, c
        ))

        print("Bước 2.")
        d = signer.PrivateTest(c)
        print("A gửi lại cho B giá trị d = ", d)

        print("Bước 3.")
        rightSide = (mu(x, e1, p) * mu(alpha, e2, p)) % p
        print("Giá trị của vế trái = x^e1 * alpha^e2 % p = {}^{}.{}^{} mod {} = {}".format(
            x, e1, alpha, e2, p, rightSide
        ))
        if d == rightSide:
            print("d == vế phải. Chữ ký hợp lệ ({} == {})".format(d, rightSide))
        else:
            print("d != vế phải. Chữ ký không hợp lệ ({} != {})".format(d, rightSide))

    def checkDeny(self, x, y, e1, e2, f1, f2, signer: AntverpenSigner):
        print("########### CHECK DENY #############")
        print("Bước 1.")
        p, alpha, beta = signer.getPublicKey()
        print("Giá trị khóa công khai từ A: p={}, alpha={}, beta={}".format(p, alpha, beta))

        print("Giá trị của bản rõ và chữ ký: x = {}, y = {}".format(x, y))
        print("B chọn ngẫu nhiên hai số e1 = {}, e2 = {}".format(e1, e2))

        c = (mu(y, e1, p) * mu(beta, e2, p)) % p
        print("Giá trị của c = y^(e1).beta^(e2) mod p= {}^{}.{}^{} mod {}= {}".format(
            y, e1, beta, e2, p, c
        ))

        print("Bước 2.")
        d = signer.PrivateTest(c)
        print("A gửi lại cho B giá trị d = ", d)

        print("Bước 3.")
        rightSide = (mu(x, e1, p) * mu(alpha, e2, p)) % p
        print("Giá trị của vế trái = x^e1 * alpha^e2 % p = {}^{}.{}^{} mod {} = {}".format(
            x, e1, alpha, e2, p, rightSide
        ))
        if d != rightSide:
            print("Giá trị của d khác giá trị của vế phải. ({} != {})".format(d, rightSide))
            print("Bước 4. Chọn f1={}, f2={}".format(f1, f2))

            C = (mu(y, f1, p) * mu(beta, f2, p)) % p
            print("Giá trị của C = y^(f1).beta^(f2) mod p= {}^{}.{}^{} mod {}= {}".format(
                y, f1, beta, f2, p, C
            ))

            print("Bước 5.")
            D = signer.PrivateTest(C)
            print("A tính và gửi lại cho B giá trị D = ", D)

            print("Bước 6.")
            rightSide = (mu(x, f1, p) * mu(alpha, f2, p)) % p
            print("Giá trị của vế phải = x^f1 . alpha^f2 mod p = {}^{} . {}^{} mod {} = {}".format(
                x, f1, alpha, f2, p, rightSide
            ))

            if D != rightSide:
                print("Giá trị của D khác vế phải ({} != {})".format(D, rightSide))

                leftSide = mu(d * mu(alpha, p - 1 -e2, p), f1, p)
                rightSide3 = mu(D * mu(alpha, p - 1 -f2, p), e1, p)

                print("Bước 7.")
                print("Giá trị của vế trái = (d.alpha^(-e2))^f1 = ({}.{}^{})^{} = {}".format(
                    d, alpha, -e2, f1, leftSide
                ))
                print("Giá trị của vế phải = (D.alpha^(-f2))^e1 = ({}.{}^{})^{} = ".format(
                    D, alpha, -f2, e1, p
                ), end="")
                print(rightSide3)

                if leftSide == rightSide3:
                    print("Giá trị vế trái và vế phải bằng nhau ({} == {}). Chữ ký là giả.".format(
                        leftSide, rightSide3
                    ))
            else:
                print("???")
        else:
            print("???")

if __name__ == "__main__":
    print("----- STATE 1 ------------")
    x = string2int('DU')
    print(x)

    signer = AntverpenSigner(p=1511, a=912, alpha=9)
    ## TODO: tìm nhóm con cấp q
    checker = AntverpenChecker()

    signature = signer.sign(x)

    checker.checkSignature(x, signature, 33, 37, signer)

    y = signature
    checker.checkDeny(x, y, e1=23, e2=145, f1=15, f2=22, signer=signer)

    print("----- STATE 2 ------------")
    x = string2int('DA')
    print(x)

    signer = AntverpenSigner(p=1559, a=337, alpha=10)
    ## TODO: tìm nhóm con cấp q
    checker = AntverpenChecker()

    signature = signer.sign(x)

    checker.checkSignature(x, signature, 41, 211, signer)

    y = signature
    checker.checkDeny(x, y, e1=41, e2=211, f1=25, f2=119, signer=signer)