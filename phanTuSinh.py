from dmath.dmath import *

def timPhanTuSinh(p):
    q = (p - 1) // 2

    for i in range(2, p):
        if mu(i, q, p) == 1:
            print(i)

timPhanTuSinh(1559)