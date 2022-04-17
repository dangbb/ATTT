from dmath.dmath import *
from dstring.dstring import *


class ChaumvanHash:
    def __init__(self, p, alpha, beta):
        self.p = p
        self.alpha = alpha
        self.beta = beta

    def encode(self, x1, x2):
        return (mu(self.alpha, x1, self.p) * mu(self.beta, x2, self.p)) % self.p

class ExtentHash:
    def __init__(self):
        pass