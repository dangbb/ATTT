def string2int(s, mod=-1):
    s = str.upper(s)
    res = 0
    for c in s:
        res = res * 26 + ord(c) - ord('A')
        if mod != -1:
            res = res % mod
    return res


def int2string(v):
    res = ""
    while v > 0:
        res = chr(v % 26 + ord('A')) + res
        v = v // 26
    return res


# print(string2int("DU"))