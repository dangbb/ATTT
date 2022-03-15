from dmath.dmath import *


def chineseRemainer(r, m):
    M = 1
    for mi in m:
        M = M * mi
    Mi = []
    y = []
    for mi in m:
        Mi.append(M // mi)
        y.append(invModulo(Mi[-1], mi)[0])

    x = 0
    for i in range(len(r)):
        x += r[i] * Mi[i] * y[i]
    print("Result: ", x)

    print("Testing...")
    for i in range(len(r)):
        print("\t Expected r: ", r[i], " mod ", m[i], " Got ", x % m[i], end=" ")
        if x % m[i] == r[i]:
            print("TRUE")
        else:
            print("FALSE")


chineseRemainer([3, 7], [7, 13])