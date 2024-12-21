from GF import GF
from polynomials import Polynomials


class CypherKeyError(Exception):
    def __init_(self, poly):
        super().__init__(f"The first key should not equal to {poly}")


def from_string_to_list_of_polys(input_str: str):
    str_repr_polys = [list(bin(ord(elem)).lstrip("0b")[::-1]) for elem in input_str]
    return [[int(char) for char in elem] for elem in str_repr_polys]


def from_list_of_polys_to_string(input_list: list):
    list_bin_repr = [chr(int("".join(list(reversed([str(cooeff) for cooeff in elem]))), 2)) for elem in input_list]
    return "".join(list_bin_repr)


def encryption(key: list, plaintext: str):
    if key[0] != Polynomials(2, [0]):
        gf_2 = GF(2, Polynomials(2, [1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1]))
        list_of_polys_cooeffs = [Polynomials(2, cooeffs) for cooeffs in from_string_to_list_of_polys(plaintext)]
        list_of_encrypted_chars = [gf_2.addition_of_polynomials(gf_2.multiplication_of_polynomials(poly, key[0]),
                                                                key[1]).cooeffs for poly in list_of_polys_cooeffs]
        return from_list_of_polys_to_string(list_of_encrypted_chars)
    else:
        raise KeyError(key[0])


def decryption(key: list, cypher_text: str):
    gf_2 = GF(2, Polynomials(2, [1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1]))
    list_of_polys_cooeffs = [Polynomials(2, cooeffs) for cooeffs in from_string_to_list_of_polys(cypher_text)]
    reverse_value_of_key = gf_2.find_reverse_element(key[0])
    list_of_decrypted_chars = [gf_2.multiplication_of_polynomials(
        gf_2.subtraction_of_polynomials(poly, key[1]), reverse_value_of_key).cooeffs for poly in list_of_polys_cooeffs]
    return from_list_of_polys_to_string(list_of_decrypted_chars)
