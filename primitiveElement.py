from dmath.dmath import *
import math
import tqdm


def precondition(x):
    if x > 2 and x % 2 == 0:
        return 0
    if x > 3 and x % 3 == 0:
        return 0
    if x > 5 and x % 5 == 0:
        return 0
    if x > 7 and x % 7 == 0:
        return 0
    if x > 11 and x % 11 == 0:
        return 0
    if x > 13 and x % 13 == 0:
        return 0
    if x > 17 and x % 17 == 0:
        return 0
    if x > 19 and x % 19 == 0:
        return 0
    return 1


def testPrimitive(r, limit = -1):
    # for i in range(2, int(math.sqrt(r)) + 1):
    #     if r % i == 0:
    #         print("r is not a prime !")
    #         return

    i = 2
    index = []
    while i <= int(math.sqrt(r)):
        if i % 1000000000 == 0:
            print(i)
        index = [i for i in range(2, int(math.sqrt(r)) + 1) if precondition(i)]
        if precondition(i):
            index.append(i)
        i += 1

    for alpha in range(2, r):
        isOK = True
        for _, i in tqdm.tqdm(enumerate(index)):
            if (r - 1) % i == 0:
                if mu(alpha, (r - 1) / i, r) == 1:
                    isOK = False
                    break
        if isOK:
            limit -= 1
            print(alpha)

            if limit == 0:
                break


def testPrimitive2(r, limit = -1):
    index = [2, (r - 1) // 2]
    for alpha in range(2, r):
        isOK = True
        for i in index:
            if (r - 1) % i == 0:
                if mu(alpha, (r - 1) // i, r) == 1:
                    isOK = False
                    break
        if isOK:
            limit -= 1
            print(alpha)

            if limit == 0:
                break

# TODO: kiểm tra tính nguyên thủy bằng tìm ước.

testPrimitive2(29072553456409183479268752003825253455672839222789445223234915115682921921621182714164684048719891059149763352939888629001652768286998932224000980861127751097886364432307005283784155195197202827350411, 1)