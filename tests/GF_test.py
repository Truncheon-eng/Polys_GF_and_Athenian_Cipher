from GF import GF
from polynomials import Polynomials

sep = "----------------------->"

gf = GF(3, Polynomials(3, [1, 1, 2]))
gf.find_forming_elements()
gf.show_forming_elements()
print(sep)
first_poly = Polynomials(3, [0, 1])
gf.print_multiplicative_group_gf_by_element(first_poly)
print(sep)
poly_1, poly_2 = Polynomials(3, [1, 1, 2]), Polynomials(3, [1, 1])
print(gf.addition_of_polynomials(poly_1, poly_2))
print(sep)
poly_3, poly_4 = Polynomials(3, [1, 2]), Polynomials(3, [2, 1])
print(gf.multiplication_of_polynomials(poly_3, poly_4))
print(sep)
gf.show_field_elements()
