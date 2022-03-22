def mu(base, top, mode):
    if top == 0:
        return 1
    if top == 1:
        return base % mode
    x = mu(base, top // 2, mode)
    x = (x * x) % mode

    if top % 2 == 0:
        return x
    else:
        return (x * base) % mode


def gcd(x, y):
    c = x % y
    while True:
        c = x % y
        x = y
        y = c
        if c == 0:
            break
    return x


def gcdExtend(xe, ye, xmod, ymod, e, mod, modulo, gcdd):
    d = mod // e 
    r = mod - e * d
    
    newxe = (xmod - (xe * d) % modulo + modulo) % modulo
    newye = (ymod - (ye * d) % modulo + modulo) % modulo

    if r == gcdd:
        return newxe, newye

    return gcdExtend(newxe, newye, xe, ye, r, e, modulo, gcdd)


def invModulo(e, mod):
    if e == 1:
        return 1, 0
    x1, x2 = gcdExtend(1, 0, 0, 1, e, mod, mod, gcd(e, mod))
    assert x1 * e - ((x1 * e) // mod) * mod == 1, "Inverse Module, result is not inverse."
    return x1, x2
