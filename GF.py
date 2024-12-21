from polynomials import Polynomials, extended_euclidean_algorithm
import copy


class GaloisDifferentModuleError(Exception):
    def __init__(self, mod_1, mod_2):
        super().__init__(f"Cannot set primitive polynom with module: {mod_2} while GF module is {mod_1}")
        self.mod_1 = mod_1
        self.mod_2 = mod_2


class GaloisFormingElementError(Exception):
    def __init__(self):
        super().__init__("This element isn't forming, or you didn't use find_forming_elements method")


class GF:
    def __init__(self, modulus: int, primitive_poly: Polynomials):
        self.modulus = modulus
        if isinstance(primitive_poly, Polynomials):
            if primitive_poly.modulus == self.modulus:
                # TODO: попытаться каким-то образом определять является ли данный многочлен простым,
                #  например полный перебор
                self.primitive_poly = primitive_poly
            else:
                raise GaloisDifferentModuleError(self.modulus, primitive_poly.modulus)
        else:
            raise TypeError(f"Primitive poly must be type of Polynomials")
        self.num_of_degrees = primitive_poly.degree
        self.field_elements = list()
        for number in range(0, self.modulus**self.num_of_degrees):
            poly_list = list()
            current_value = number
            while current_value >= self.modulus:
                current_value, remainder = divmod(current_value, self.modulus)
                poly_list.append(remainder)
            poly_list.append(current_value)
            self.field_elements.append(Polynomials(self.modulus, poly_list))
        self.forming_elements = None

    def addition_of_polynomials(self, poly_1, poly_2):
        return (poly_1 + poly_2) % self.primitive_poly

    def subtraction_of_polynomials(self, poly_1, poly_2):
        return (poly_1 - poly_2) % self.primitive_poly

    def multiplication_of_polynomials(self, poly_1, poly_2):
        return (poly_1 * poly_2) % self.primitive_poly

    def find_forming_elements(self):
        if not self.forming_elements:
            self.forming_elements = list()
            for i in range(self.modulus, self.modulus**self.num_of_degrees):
                current_poly = copy.deepcopy(self.field_elements[i])
                list_of_polynomials = list([Polynomials(self.modulus, [1])])
                while current_poly != list_of_polynomials[0]:
                    list_of_polynomials.append(current_poly)
                    current_poly = self.multiplication_of_polynomials(current_poly, self.field_elements[i])
                if len(list_of_polynomials) == self.modulus**self.num_of_degrees - 1:
                    self.forming_elements.append(self.field_elements[i])
                    for j in range(2, len(list_of_polynomials)):
                        if extended_euclidean_algorithm(self.modulus**self.num_of_degrees-1, j)[0] == 1:
                            self.forming_elements.append(list_of_polynomials[j])
                    break

    def print_multiplicative_group_gf_by_element(self, poly):
        if poly in self.forming_elements:
            current_poly = copy.deepcopy(poly)
            identity = Polynomials(self.modulus, [1])
            idx = 0
            print(f"X^{idx} =", identity)
            while current_poly != identity:
                idx += 1
                print(f"X^{idx} =", current_poly)
                current_poly = self.multiplication_of_polynomials(current_poly, poly)
        else:
            raise GaloisFormingElementError

    def find_reverse_element(self, poly):
        divisor = poly % self.primitive_poly
        dividend = self.primitive_poly
        y_2, y_1 = Polynomials(self.modulus, [0]), Polynomials(self.modulus, [1])
        while divisor != Polynomials(self.modulus, [0]):
            quotient, remainder = dividend // divisor, dividend % divisor
            dividend, divisor = divisor, remainder
            y = y_2 - quotient * y_1
            y_2, y_1 = y_1, y
        return (self.multiplication_of_polynomials
                (Polynomials(self.modulus, [extended_euclidean_algorithm(self.modulus, dividend.cooeffs[0])[1]]), y_2))

    def show_forming_elements(self):
        for elem in self.forming_elements:
            print(elem)

    def show_field_elements(self):
        for elem in self.field_elements:
            print(elem)
