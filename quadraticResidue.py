from dmath.dmath import *


def findAllQuadraticResidual(p):
    """

    :param p: Must be an odd prime
    :return: Print list of quadratic residual
    """

    for i in range(1, p):
        if mu(i, (p-1) // 2, p) == 1:
            print(i)


def checkAllResidual(p):
    """

    :param p: A prime
    :return: print all value and it square modulo p
    """

    for i in range(1, p):
        print(i, mu(i, 2, p))


findAllQuadraticResidual(23)
