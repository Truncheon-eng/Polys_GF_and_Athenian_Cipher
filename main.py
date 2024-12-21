from cypher import encryption, decryption
from polynomials import Polynomials


def from_key_to_polys(key_list: list):
    res = list()
    for i in range(len(key_list)):
        res.append(Polynomials(2, [int(elem) for elem in key_list[i].strip(" []").split(", ")]))
    return res


if __name__ == '__main__':
    mode = input("Введите 0 для зашифрования, 1 для расшифрования: ")
    if mode == "0":
        input_str = input("Введите значение для зашифрования: ")
        key = [input("Введите значение a: "), input("Введите значение b: ")]
        print(encryption(from_key_to_polys(key), input_str))
    elif mode == "1":
        input_str = input("Введите значение для расшифрования: ")
        key = [input("Введите значение a: "), input("Введите значение b: ")]
        print(decryption(from_key_to_polys(key), input_str))
    else:
        print("Было введено неверное значение")
