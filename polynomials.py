import copy


def checks(method):
    def wrapper(self, other):
        if not isinstance(other, Polynomials):
            raise TypeError(f"Argument must be of type {Polynomials.__name__}")
        elif self.modulus != other.modulus:
            raise IncompatibleModuliError(self.modulus, other.modulus)
        else:
            return method(self, other)
    return wrapper


def extended_euclidean_algorithm(modulus, element):
    quotient, remainder, y = 0, 0, 0
    dividend, divisor, y_2, y_1 = modulus, element, 0, 1
    while divisor != 0:
        quotient, remainder = dividend // divisor, dividend % divisor
        dividend, divisor = divisor, remainder
        y = y_2 - quotient*y_1
        y_2, y_1 = y_1, y
    return dividend, y_2 % modulus


class IncompatibleModuliError(Exception):
    def __init__(self, mod_1, mod_2):
        super().__init__(f"Cannot add polynomials with different moduli: {mod_1} and {mod_2}")
        self.mod_1 = mod_1
        self.mod_2 = mod_2


class Polynomials:
    def __init__(self, modulus: int, list_poly: list):
        if not isinstance(list_poly, list) or not all(isinstance(elem, int) for elem in list_poly):
            raise TypeError("Coefficients must be a list of integers.")
        if not isinstance(modulus, int):
            raise TypeError("Modulus must be an integer.")
        if modulus <= 0:
            raise ValueError("Modulus must be a positive integer.")

        self.modulus = modulus
        self.cooeffs = [elem % modulus for elem in list_poly]
        self.degree = len(self.cooeffs) - 1
        while self.cooeffs[-1] == 0 and self.degree != 0:
            self.cooeffs.pop()
            self.degree -= 1

    @checks
    def __add__(self, other):
        len_1, len_2 = len(self.cooeffs), len(other.cooeffs)
        max_len = max(len_1, len_2)
        result = [0]*max_len
        for i in range(max_len):
            if i > len_1 - 1:
                result[i] = other.cooeffs[i] % self.modulus
            elif i > len_2 - 1:
                result[i] = self.cooeffs[i] % self.modulus
            else:
                result[i] = (self.cooeffs[i] + other.cooeffs[i]) % self.modulus
        return Polynomials(self.modulus, result)

    def __sub__(self, other):
        opposite_poly = Polynomials(other.modulus, [-elem for elem in other.cooeffs])
        return self + opposite_poly

    @checks
    def __mul__(self, other):
        deg_poly_1, deg_poly_2 = self.degree, other.degree
        result = [0]*(deg_poly_1 + deg_poly_2 + 1)
        for i in range(deg_poly_1 + deg_poly_2 + 1):
            for j in range(i + 1):
                if not j > deg_poly_1 and not i - j > deg_poly_2:
                    result[i] += self.cooeffs[j]*other.cooeffs[i-j]
            result[i] = result[i] % self.modulus
        return Polynomials(self.modulus, result)

    @checks
    def __divmod__(self, other):
        dividend, divisor = copy.copy(self.cooeffs), copy.copy(other.cooeffs)
        if self.degree < other.degree:
            return Polynomials(self.modulus, [0]), Polynomials(self.modulus, dividend)
        else:
            quotient = [0]*(self.degree - other.degree + 1)
            for i in range(len(quotient)):
                senior_cooeff = ((extended_euclidean_algorithm(self.modulus, divisor[-1])[1] * dividend[-1])
                                 % self.modulus)
                subtrahend_poly = copy.copy(divisor)
                for j in range(len(subtrahend_poly)):
                    subtrahend_poly[j] = (subtrahend_poly[j] * senior_cooeff) % self.modulus
                subtrahend_poly = [0]*(len(dividend) - len(divisor)) + subtrahend_poly
                for j in range(len(dividend)):
                    dividend[j] = (dividend[j] - subtrahend_poly[j]) % self.modulus
                if len(dividend) != 1:
                    dividend.pop()
                quotient[-1 - i] = senior_cooeff
            return Polynomials(self.modulus, quotient), Polynomials(self.modulus, dividend)

    @checks
    def __eq__(self, other):
        bool_value = True if self.cooeffs == other.cooeffs else False
        return bool_value

    def __ne__(self, other):
        return not self == other

    def __floordiv__(self, other):
        return divmod(self, other)[0]

    def __mod__(self, other):
        return divmod(self, other)[1]

    def __repr__(self):
        return f"(Polynom({self.cooeffs}), modulus: {self.modulus})"
