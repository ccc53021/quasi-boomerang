import numpy


def get_ddt(sbox, n, m):
    table = numpy.zeros((2 ** n, 2 ** m))
    for a0 in range(2 ** n):
        for x in range(2 ** n):
            for b0 in range(2 ** m):
                y = x ^ a0
                sx = sbox[x]
                sy = sbox[y]
                if (sx ^ sy) == b0:
                    table[b0, a0] += 1

    for a0 in range(2 ** n):
        for b0 in range(2 ** m):
            table[b0, a0] = table[b0, a0] / (2 ** n)

    return table

def get_bct(sbox, n, m):
    sbox_inverse = [0] * (2 ** n)
    for i in range(2 ** n):
        sbox_inverse[sbox[i]] = i

    table = numpy.zeros((2 ** n, 2 ** m))
    # F(x) = S^-1(S(x)+lower_out)
    for upper_in in range(2 ** n):
        for lower_out in range(2 ** m):
                for x1 in range(2 ** n):
                    y1 = sbox[x1]
                    y3 = y1 ^ lower_out
                    x3 = sbox_inverse[y3]
                    y2 = sbox[x1 ^ upper_in]
                    y4 = y2 ^ lower_out
                    x4 = sbox_inverse[y4]
                    if (x3 ^ x4 == upper_in):
                           table[lower_out, upper_in] += 1

    for a0 in range(2 ** n):
        for b0 in range(2 ** m):
            table[b0, a0] = table[b0, a0] / (2 ** n)

    return table

def vector_inner_product(u, x, n):
    left = 0
    for i in range(n):
        left += ((u >> i) & 0x1) * ((x >> i) & 0x1)
    left = left % 2

    return left

def get_bct_matrices(sbox, n, m):
    def matrix_f1():
        table = numpy.zeros((2 ** (3 * n), 2 ** (3 * n)))
        for u0 in range(2 ** n):
            for u1 in range(2 ** n):
                for u2 in range(2 ** n):
                    for x0 in range(2 ** n):
                        for delta_1 in range(2 ** n):
                            for delta_2 in range(2 ** n):
                                input = (x0 << 2 * n) + (delta_1 << n) + delta_2
                                output = (u0 << 2 * n) + (u1 << n) + u2
                                if u1 != delta_1:
                                    continue
                                else:
                                    if (vector_inner_product(u0, x0, n) ^ vector_inner_product(u2, delta_2, n) == 0):
                                        table[input, output] = 1
                                    else:
                                        table[input, output] = -1

        return table

    # f2 : (y, lambda_1, lambda_2) -> (v0, v1, v2)
    def matrix_f2():
        table = numpy.zeros((2 ** (3 * n), 2 ** (3 * n)))
        for y0 in range(2 ** m):
            for lambda_1 in range(2 ** m):
                for lambda_2 in range(2 ** m):
                    for v0 in range(2 ** m):
                        for v1 in range(2 ** m):
                            for v2 in range(2 ** m):
                                input = (y0 << 2 * m) + (lambda_1 << m) + lambda_2
                                output = (v0 << 2 * m) + (v1 << m) + v2
                                if v2 != lambda_2:
                                    continue
                                else:
                                    if (vector_inner_product(v0, y0, m) ^ vector_inner_product(v1, lambda_1, n) == 0):
                                        table[input, output] = 1
                                    else:
                                        table[input, output] = -1

        return table

    def matrix_e(sbox):
        table = numpy.zeros((2 ** (3 * n), 2 ** (3 * m)))
        for x0 in range(2 ** n):
            for delta_1 in range(2 ** n):
                for delta_2 in range(2 ** n):
                    for y0 in range(2 ** m):
                        for lambda_1 in range(2 ** m):
                            for lambda_2 in range(2 ** m):
                                output = (x0 << 2 * n) + (delta_1 << n) + delta_2
                                input = (y0 << 2 * m) + (lambda_1 << m) + lambda_2
                                if (y0 == sbox[x0]) and (lambda_1 == sbox[x0] ^ sbox[x0 ^ delta_1]) and (
                                        lambda_2 == sbox[x0] ^ sbox[x0 ^ delta_2]) and (
                                        lambda_1 ^ lambda_2 == sbox[x0] ^ sbox[x0 ^ delta_1 ^ delta_2]):
                                    table[input, output] = 1

        return table

    def matrix_e1(sbox):
        table = numpy.zeros((2 ** (3 * n), 2 ** (3 * m)))
        for x in range(2 ** n):
            for u0 in range(2 ** n):
                for u1 in range(2 ** n):
                    for u2 in range(2 ** n):
                        for v0 in range(2 ** m):
                            for v1 in range(2 ** m):
                                for v2 in range(2 ** m):
                                    for delta_2 in range(2 ** n):
                                        output = (u0 << 2 * n) + (u1 << n) + u2
                                        input = (v0 << 2 * m) + (v1 << m) + v2
                                        delta_1 = u1
                                        lambda_2 = v2
                                        if (sbox[x] ^ sbox[x ^ delta_2] == lambda_2) and (
                                                sbox[x] ^ sbox[x ^ delta_1 ^ delta_2] == v2 ^ sbox[x] ^ sbox[x ^ u1]):
                                            if vector_inner_product(u0, x, n) ^ vector_inner_product(u2, delta_2,
                                                                                                     n) ^ vector_inner_product(
                                                    v0, sbox[x], m) ^ vector_inner_product(v1,
                                                                                           sbox[x] ^ sbox[x ^ delta_1],
                                                                                           m) == 0:
                                                table[input, output] += 1
                                            else:
                                                table[input, output] -= 1

        for input in range(2 ** (3 * n)):
            for output in range(2 ** (3 * m)):
                if table[input, output] != 0:
                    table[input, output] = table[input, output] / (2 ** (2 * n))

        return table

    # e1 = matrix_e1(sbox)
    f1 = matrix_f1()
    e = matrix_e(sbox)
    f2 = matrix_f2()
    f1_inverse = numpy.linalg.inv(f1)
    # f2_inverse = numpy.linalg.inv(f2)
    quasi_bct = numpy.dot(numpy.dot(f2, e), f1_inverse)

    return quasi_bct


def get_ddt_upper_matrices(sbox, n, m):
    # f1 : (x, delta_1, delta_2) -> (u0, u1, u2)
    def matrix_f1():
        table = numpy.zeros((2 ** (3 * n), 2 ** (3 * n)))
        for u0 in range(2 ** n):
            for u1 in range(2 ** n):
                for u2 in range(2 ** n):
                    for x0 in range(2 ** n):
                        for delta_1 in range(2 ** n):
                            for delta_2 in range(2 ** n):
                                input = (x0 << 2 * n) + (delta_1 << n) + delta_2
                                output = (u0 << 2 * n) + (u1 << n) + u2
                                if u1 != delta_1:
                                    continue
                                else:
                                    if (vector_inner_product(u0, x0, n) ^ vector_inner_product(u2, delta_2, n) == 0):
                                        table[input, output] = 1
                                    else:
                                        table[input, output] = -1

        return table

    # f2 : (y, lambda_1, lambda_2) -> (v0, v1, v2)
    def matrix_f2():
        table = numpy.zeros((2 ** (3 * n), 2 ** (3 * n)))
        for y0 in range(2 ** m):
            for lambda_1 in range(2 ** m):
                for lambda_2 in range(2 ** m):
                    for v0 in range(2 ** m):
                        for v1 in range(2 ** m):
                            for v2 in range(2 ** m):
                                input = (y0 << 2 * m) + (lambda_1 << m) + lambda_2
                                output = (v0 << 2 * m) + (v1 << m) + v2
                                if v1 != lambda_1:
                                    continue
                                else:
                                    if (vector_inner_product(v0, y0, m) ^ vector_inner_product(v2, lambda_2, n) == 0):
                                        table[input, output] = 1
                                    else:
                                        table[input, output] = -1

        return table

    def matrix_e(sbox):
        table = numpy.zeros((2 ** (3 * n), 2 ** (3 * m)))
        for x0 in range(2 ** n):
            for delta_1 in range(2 ** n):
                for delta_2 in range(2 ** n):
                    for y0 in range(2 ** m):
                        for lambda_1 in range(2 ** m):
                            for lambda_2 in range(2 ** m):
                                output = (x0 << 2 * n) + (delta_1 << n) + delta_2
                                input = (y0 << 2 * m) + (lambda_1 << m) + lambda_2
                                if (y0 == sbox[x0]) and (lambda_1 == sbox[x0] ^ sbox[x0 ^ delta_1]) and (
                                        lambda_2 == sbox[x0] ^ sbox[x0 ^ delta_2]) and (
                                        lambda_1 ^ lambda_2 == sbox[x0] ^ sbox[x0 ^ delta_1 ^ delta_2]):
                                    table[input, output] = 1

        return table

    def matrix_e1(sbox):
        table = numpy.zeros((2 ** (3 * n), 2 ** (3 * m)))
        for x in range(2 ** n):
            for u0 in range(2 ** n):
                for u1 in range(2 ** n):
                    for u2 in range(2 ** n):
                        for v0 in range(2 ** m):
                            for v1 in range(2 ** m):
                                for v2 in range(2 ** m):
                                    for delta_2 in range(2 ** n):
                                        output = (u0 << 2 * n) + (u1 << n) + u2
                                        input = (v0 << 2 * m) + (v1 << m) + v2
                                        delta_1 = u1
                                        lambda_1 = v1
                                        if (sbox[x] ^ sbox[x ^ delta_1] == lambda_1) and (
                                                sbox[x] ^ sbox[x ^ delta_1 ^ delta_2] == v1 ^ sbox[x] ^ sbox[x ^ delta_2]):
                                            if vector_inner_product(u0, x, n) ^ vector_inner_product(u2, delta_2,
                                                                                                     n) ^ vector_inner_product(
                                                    v0, sbox[x], m) ^ vector_inner_product(v2,
                                                                                           sbox[x] ^ sbox[x ^ delta_2],
                                                                                           m) == 0:
                                                table[input, output] += 1
                                            else:
                                                table[input, output] -= 1

        for input in range(2 ** (3 * n)):
            for output in range(2 ** (3 * m)):
                if table[input, output] != 0:
                    table[input, output] = table[input, output] / (2 ** (2 * n))

        return table

    # e1 = matrix_e1(sbox)
    f1 = matrix_f1()
    e = matrix_e(sbox)
    f2 = matrix_f2()
    f1_inverse = numpy.linalg.inv(f1)
    # f2_inverse = numpy.linalg.inv(f2)
    quasi_ddt = numpy.dot(numpy.dot(f2, e), f1_inverse)

    return quasi_ddt

def get_ddt_lower_matrices(sbox, n, m):
    # f1 : (x, delta_1, delta_2) -> (u0, u1, u2)
    def matrix_f1():
        table = numpy.zeros((2 ** (3 * n), 2 ** (3 * n)))
        for u0 in range(2 ** n):
            for u1 in range(2 ** n):
                for u2 in range(2 ** n):
                    for x0 in range(2 ** n):
                        for delta_1 in range(2 ** n):
                            for delta_2 in range(2 ** n):
                                input = (x0 << 2 * n) + (delta_1 << n) + delta_2
                                output = (u0 << 2 * n) + (u1 << n) + u2
                                if u2 != delta_2:
                                    continue
                                else:
                                    if (vector_inner_product(u0, x0, n) ^ vector_inner_product(u1, delta_1, n) == 0):
                                        table[input, output] = 1
                                    else:
                                        table[input, output] = -1

        return table

    # f2 : (y, lambda_1, lambda_2) -> (v0, v1, v2)
    def matrix_f2():
        table = numpy.zeros((2 ** (3 * n), 2 ** (3 * n)))
        for y0 in range(2 ** m):
            for lambda_1 in range(2 ** m):
                for lambda_2 in range(2 ** m):
                    for v0 in range(2 ** m):
                        for v1 in range(2 ** m):
                            for v2 in range(2 ** m):
                                input = (y0 << 2 * m) + (lambda_1 << m) + lambda_2
                                output = (v0 << 2 * m) + (v1 << m) + v2
                                if v2 != lambda_2:
                                    continue
                                else:
                                    if (vector_inner_product(v0, y0, m) ^ vector_inner_product(v1, lambda_1, n) == 0):
                                        table[input, output] = 1
                                    else:
                                        table[input, output] = -1

        return table

    def matrix_e(sbox):
        table = numpy.zeros((2 ** (3 * n), 2 ** (3 * m)))
        for x0 in range(2 ** n):
            for delta_1 in range(2 ** n):
                for delta_2 in range(2 ** n):
                    for y0 in range(2 ** m):
                        for lambda_1 in range(2 ** m):
                            for lambda_2 in range(2 ** m):
                                output = (x0 << 2 * n) + (delta_1 << n) + delta_2
                                input = (y0 << 2 * m) + (lambda_1 << m) + lambda_2
                                if (y0 == sbox[x0]) and (lambda_1 == sbox[x0] ^ sbox[x0 ^ delta_1]) and (
                                        lambda_2 == sbox[x0] ^ sbox[x0 ^ delta_2]) and (
                                        lambda_1 ^ lambda_2 == sbox[x0] ^ sbox[x0 ^ delta_1 ^ delta_2]):
                                    table[input, output] = 1

        return table

    def matrix_e1(sbox):
        table = numpy.zeros((2 ** (3 * n), 2 ** (3 * m)))
        for x in range(2 ** n):
            for u0 in range(2 ** n):
                for u1 in range(2 ** n):
                    for u2 in range(2 ** n):
                        for v0 in range(2 ** m):
                            for v1 in range(2 ** m):
                                for v2 in range(2 ** m):
                                    for delta_1 in range(2 ** n):
                                        output = (u0 << 2 * n) + (u1 << n) + u2
                                        input = (v0 << 2 * m) + (v1 << m) + v2
                                        delta_2 = u2
                                        lambda_2 = v2
                                        if (sbox[x] ^ sbox[x ^ delta_2] == lambda_2) and (
                                                sbox[x] ^ sbox[x ^ delta_1 ^ delta_2] == v2 ^ sbox[x] ^ sbox[x ^ delta_1]):
                                            if vector_inner_product(u0, x, n) ^ vector_inner_product(u1, delta_1,
                                                                                                     n) ^ vector_inner_product(
                                                    v0, sbox[x], m) ^ vector_inner_product(v1,
                                                                                           sbox[x] ^ sbox[x ^ delta_1],
                                                                                           m) == 0:
                                                table[input, output] += 1
                                            else:
                                                table[input, output] -= 1

        for input in range(2 ** (3 * n)):
            for output in range(2 ** (3 * m)):
                if table[input, output] != 0:
                    table[input, output] = table[input, output] / (2 ** (2 * n))

        return table

    # e1 = matrix_e1(sbox)
    f1 = matrix_f1()
    e = matrix_e(sbox)
    f2 = matrix_f2()
    f1_inverse = numpy.linalg.inv(f1)
    # f2_inverse = numpy.linalg.inv(f2)
    quasi_ddt = numpy.dot(numpy.dot(f2, e), f1_inverse)

    return quasi_ddt

def get_ddt_upper_matrices_2n_by_given_delta_1_and_lambda_1(sbox, n, m, delta_1, lambda_1):
    # f1 : (x, delta_1, delta_2) -> (u0, u1, u2)
    def matrix_f1():
        table = numpy.zeros((2 ** (2 * n), 2 ** (2 * n)))
        for u0 in range(2 ** n):
            for u2 in range(2 ** n):
                for x0 in range(2 ** n):
                    for delta_2 in range(2 ** n):
                        input = (x0 << n) + delta_2
                        output = (u0 << n) + u2
                        if (vector_inner_product(u0, x0, n) ^ vector_inner_product(u2, delta_2, n) == 0):
                            table[input, output] = 1
                        else:
                            table[input, output] = -1

        return table

    # f2 : (y, lambda_1, lambda_2) -> (v0, v1, v2)
    def matrix_f2():
        table = numpy.zeros((2 ** (2 * n), 2 ** (2 * n)))
        for y0 in range(2 ** m):
            for lambda_2 in range(2 ** m):
                for v0 in range(2 ** m):
                    for v2 in range(2 ** m):
                        input = (y0 << m) + lambda_2
                        output = (v0 << m) + v2
                        if (vector_inner_product(v0, y0, m) ^ vector_inner_product(v2, lambda_2, n) == 0):
                            table[input, output] = 1
                        else:
                            table[input, output] = -1

        return table

    def matrix_e(sbox):
        table = numpy.zeros((2 ** (2 * n), 2 ** (2 * m)))
        for x0 in range(2 ** n):
            for delta_2 in range(2 ** n):
                for y0 in range(2 ** m):
                    for lambda_2 in range(2 ** m):
                        output = (x0 << n) + delta_2
                        input = (y0 << m) + lambda_2
                        if (y0 == sbox[x0]) and (lambda_1 == sbox[x0] ^ sbox[x0 ^ delta_1]) and (
                                lambda_2 == sbox[x0] ^ sbox[x0 ^ delta_2]) and (
                                lambda_1 ^ lambda_2 == sbox[x0] ^ sbox[x0 ^ delta_1 ^ delta_2]):
                            table[input, output] = 1

        return table

    def matrix_e1(sbox):
        table = numpy.zeros((2 ** (2 * n), 2 ** (2 * m)))
        for x in range(2 ** n):
            for u0 in range(2 ** n):
                for u2 in range(2 ** n):
                    for v0 in range(2 ** m):
                        for v2 in range(2 ** m):
                            for delta_2 in range(2 ** n):
                                output = (u0 << n) + u2
                                input = (v0 << m) + v2
                                if (sbox[x] ^ sbox[x ^ delta_1] == lambda_1) and (
                                        sbox[x] ^ sbox[x ^ delta_1 ^ delta_2] == lambda_1 ^ sbox[x] ^ sbox[x ^ delta_2]):
                                    if vector_inner_product(u0, x, n) ^ vector_inner_product(u2, delta_2,
                                                                                             n) ^ vector_inner_product(
                                        v0, sbox[x], m) ^ vector_inner_product(v2,
                                                                               sbox[x] ^ sbox[x ^ delta_2],
                                                                               m) == 0:
                                        table[input, output] += 1
                                    else:
                                        table[input, output] -= 1

        for input in range(2 ** (2 * n)):
            for output in range(2 ** (2 * m)):
                if table[input, output] != 0:
                    table[input, output] = table[input, output] / (2 ** (2 * n))

        return table

    # e1 = matrix_e1(sbox)
    f1 = matrix_f1()
    e = matrix_e(sbox)
    f2 = matrix_f2()
    f1_inverse = numpy.linalg.inv(f1)
    # f2_inverse = numpy.linalg.inv(f2)
    quasi_ddt = numpy.dot(numpy.dot(f2, e), f1_inverse)

    return quasi_ddt

def get_bct_matrices_2n_by_given_delta_1_and_lambda_2(sbox, n, m, delta_1, lambda_2):
    def matrix_f1():
        table = numpy.zeros((2 ** (2 * n), 2 ** (2 * n)))
        for u0 in range(2 ** n):
            for u2 in range(2 ** n):
                for x0 in range(2 ** n):
                    for delta_2 in range(2 ** n):
                        input = (x0 << n) + delta_2
                        output = (u0 << n) + u2
                        if (vector_inner_product(u0, x0, n) ^ vector_inner_product(u2, delta_2, n) == 0):
                            table[input, output] = 1
                        else:
                            table[input, output] = -1
        return table

    # f2 : (y, lambda_1, lambda_2) -> (v0, v1, v2)
    def matrix_f2():
        table = numpy.zeros((2 ** (2 * n), 2 ** (2 * n)))
        for y0 in range(2 ** m):
            for lambda_1 in range(2 ** m):
                for v0 in range(2 ** m):
                    for v1 in range(2 ** m):
                        input = (y0 << m) + lambda_1
                        output = (v0 << m) + v1
                        if (vector_inner_product(v0, y0, m) ^ vector_inner_product(v1, lambda_1, n) == 0):
                            table[input, output] = 1
                        else:
                            table[input, output] = -1

        return table

    def matrix_e(sbox):
        table = numpy.zeros((2 ** (2 * n), 2 ** (2 * m)))
        for x0 in range(2 ** n):
            for delta_2 in range(2 ** n):
                for y0 in range(2 ** m):
                    for lambda_1 in range(2 ** m):
                        output = (x0 << n) + delta_2
                        input = (y0 << m) + lambda_1
                        if (y0 == sbox[x0]) and (lambda_1 == sbox[x0] ^ sbox[x0 ^ delta_1]) and (
                                lambda_2 == sbox[x0] ^ sbox[x0 ^ delta_2]) and (
                                lambda_1 ^ lambda_2 == sbox[x0] ^ sbox[x0 ^ delta_1 ^ delta_2]):
                            table[input, output] = 1

        return table

    def matrix_e1(sbox):
        table = numpy.zeros((2 ** (2 * n), 2 ** (2 * m)))
        for x in range(2 ** n):
            for u0 in range(2 ** n):
                for u2 in range(2 ** n):
                    for v0 in range(2 ** m):
                        for v1 in range(2 ** m):
                            for delta_2 in range(2 ** n):
                                output = (u0 << n) + u2
                                input = (v0 << m) + v1
                                if (sbox[x] ^ sbox[x ^ delta_2] == lambda_2) and (
                                        sbox[x] ^ sbox[x ^ delta_1 ^ delta_2] == lambda_2 ^ sbox[x] ^ sbox[x ^ delta_1]):
                                    if vector_inner_product(u0, x, n) ^ vector_inner_product(u2, delta_2,
                                                                                             n) ^ vector_inner_product(
                                        v0, sbox[x], m) ^ vector_inner_product(v1,
                                                                               sbox[x] ^ sbox[x ^ delta_1],
                                                                               m) == 0:
                                        table[input, output] += 1
                                    else:
                                        table[input, output] -= 1

        for input in range(2 ** (2 * n)):
            for output in range(2 ** (2 * m)):
                if table[input, output] != 0:
                    table[input, output] = table[input, output] / (2 ** (2 * n))

        return table

    # e1 = matrix_e1(sbox)
    f1 = matrix_f1()
    e = matrix_e(sbox)
    f2 = matrix_f2()
    f1_inverse = numpy.linalg.inv(f1)
    # f2_inverse = numpy.linalg.inv(f2)
    quasi_bct = numpy.dot(numpy.dot(f2, e), f1_inverse)

    return quasi_bct

def get_ddt_lower_matrices_2n_by_given_delta_2_and_lambda_2(sbox, n, m, delta_2, lambda_2):
    # f1 : (x, delta_1, delta_2) -> (u0, u1, u2)
    def matrix_f1():
        table = numpy.zeros((2 ** (2 * n), 2 ** (2 * n)))
        for u0 in range(2 ** n):
            for u1 in range(2 ** n):
                for x0 in range(2 ** n):
                    for delta_1 in range(2 ** n):
                        input = (x0 << n) + delta_1
                        output = (u0 << n) + u1
                        if (vector_inner_product(u0, x0, n) ^ vector_inner_product(u1, delta_1, n) == 0):
                            table[input, output] = 1
                        else:
                            table[input, output] = -1

        return table

    # f2 : (y, lambda_1, lambda_2) -> (v0, v1, v2)
    def matrix_f2():
        table = numpy.zeros((2 ** (2 * n), 2 ** (2 * n)))
        for y0 in range(2 ** m):
            for lambda_1 in range(2 ** m):
                for v0 in range(2 ** m):
                    for v1 in range(2 ** m):
                        input = (y0 << m) + lambda_1
                        output = (v0 << m) + v1
                        if (vector_inner_product(v0, y0, m) ^ vector_inner_product(v1, lambda_1, n) == 0):
                            table[input, output] = 1
                        else:
                            table[input, output] = -1

        return table

    def matrix_e(sbox):
        table = numpy.zeros((2 ** (2 * n), 2 ** (2 * m)))
        for x0 in range(2 ** n):
            for delta_1 in range(2 ** n):
                for y0 in range(2 ** m):
                    for lambda_1 in range(2 ** m):
                        output = (x0 << n) + delta_1
                        input = (y0 << m) + lambda_1
                        if (y0 == sbox[x0]) and (lambda_1 == sbox[x0] ^ sbox[x0 ^ delta_1]) and (
                                lambda_2 == sbox[x0] ^ sbox[x0 ^ delta_2]) and (
                                lambda_1 ^ lambda_2 == sbox[x0] ^ sbox[x0 ^ delta_1 ^ delta_2]):
                            table[input, output] = 1

        return table

    def matrix_e1(sbox):
        table = numpy.zeros((2 ** (2 * n), 2 ** (2 * m)))
        for x in range(2 ** n):
            for u0 in range(2 ** n):
                for u1 in range(2 ** n):
                    for v0 in range(2 ** m):
                        for v1 in range(2 ** m):
                            for delta_1 in range(2 ** n):
                                output = (u0 << n) + u1
                                input = (v0 << m) + v1
                                if (sbox[x] ^ sbox[x ^ delta_2] == lambda_2) and (
                                        sbox[x] ^ sbox[x ^ delta_1 ^ delta_2] == lambda_2 ^ sbox[x] ^ sbox[x ^ delta_1]):
                                    if vector_inner_product(u0, x, n) ^ vector_inner_product(u1, delta_1,
                                                                                             n) ^ vector_inner_product(
                                        v0, sbox[x], m) ^ vector_inner_product(v1,
                                                                               sbox[x] ^ sbox[x ^ delta_1],
                                                                               m) == 0:
                                        table[input, output] += 1
                                    else:
                                        table[input, output] -= 1

        for input in range(2 ** (2 * n)):
            for output in range(2 ** (2 * m)):
                if table[input, output] != 0:
                    table[input, output] = table[input, output] / (2 ** (2 * n))

        return table

    # e1 = matrix_e1(sbox)
    f1 = matrix_f1()
    e = matrix_e(sbox)
    f2 = matrix_f2()
    f1_inverse = numpy.linalg.inv(f1)
    # f2_inverse = numpy.linalg.inv(f2)
    quasi_ddt = numpy.dot(numpy.dot(f2, e), f1_inverse)

    return quasi_ddt

def get_ddt_upper_matrices_2n_by_zeros_u2_v2_and_given_delta_1_and_lambda_1(sbox, n, m, delta_1, lambda_1):
    # f1 : (x, delta_1, delta_2) -> (u0, u1, u2)
    def matrix_f1():
        table = numpy.zeros((2 ** (2 * n), 2 ** (1 * n)))
        for u0 in range(2 ** n):
            for x0 in range(2 ** n):
                for delta_2 in range(2 ** n):
                    input = (x0 << n) + delta_2
                    output = u0
                    if (vector_inner_product(u0, x0, n) == 0):
                        table[input, output] = 1
                    else:
                        table[input, output] = -1

        return table

    # f2 : (y, lambda_1, lambda_2) -> (v0, v1, v2)
    def matrix_f2():
        table = numpy.zeros((2 ** (2 * m), 2 ** (1 * m)))
        for y0 in range(2 ** m):
            for lambda_2 in range(2 ** m):
                for v0 in range(2 ** m):
                    input = (y0 << m) + lambda_2
                    output = v0
                    if (vector_inner_product(v0, y0, m) == 0):
                        table[input, output] = 1
                    else:
                        table[input, output] = -1

        return table

    def matrix_e(sbox):
        table = numpy.zeros((2 ** (2 * n), 2 ** (2 * m)))
        for x0 in range(2 ** n):
            for delta_2 in range(2 ** n):
                for y0 in range(2 ** m):
                    for lambda_2 in range(2 ** m):
                        output = (x0 << n) + delta_2
                        input = (y0 << m) + lambda_2
                        if (y0 == sbox[x0]) and (lambda_1 == sbox[x0] ^ sbox[x0 ^ delta_1]) and (
                                lambda_2 == sbox[x0] ^ sbox[x0 ^ delta_2]) and (
                                lambda_1 ^ lambda_2 == sbox[x0] ^ sbox[x0 ^ delta_1 ^ delta_2]):
                            table[input, output] = 1

        return table

    def matrix_e1(sbox):
        table = numpy.zeros((2 ** (1 * n), 2 ** (1 * m)))
        for x in range(2 ** n):
            for u0 in range(2 ** n):
                for v0 in range(2 ** m):
                    for delta_2 in range(2 ** n):
                        output = u0
                        input = v0
                        if (sbox[x] ^ sbox[x ^ delta_1] == lambda_1) and (
                                sbox[x] ^ sbox[x ^ delta_1 ^ delta_2] == lambda_1 ^ sbox[x] ^ sbox[x ^ delta_2]):
                            if vector_inner_product(u0, x, n) ^ vector_inner_product(
                                v0, sbox[x], m) == 0:
                                table[input, output] += 1
                            else:
                                table[input, output] -= 1

        for input in range(2 ** (1 * n)):
            for output in range(2 ** (1 * m)):
                if table[input, output] != 0:
                    table[input, output] = table[input, output] / (2 ** (2 * n))

        return table

    e1 = matrix_e1(sbox)
    quasi_ddt = e1

    return quasi_ddt

def get_bct_matrices_2n_by_zeros_u2_v1_and_given_delta_1_and_lambda_2(sbox, n, m, delta_1, lambda_2):
    def matrix_f1():
        table = numpy.zeros((2 ** (2 * n), 2 ** (1 * n)))
        for u0 in range(2 ** n):
            for x0 in range(2 ** n):
                for delta_2 in range(2 ** n):
                    input = (x0 << n) + delta_2
                    output = u0
                    if (vector_inner_product(u0, x0, n) == 0):
                        table[input, output] = 1
                    else:
                        table[input, output] = -1
        return table

    # f2 : (y, lambda_1, lambda_2) -> (v0, v1, v2)
    def matrix_f2():
        table = numpy.zeros((2 ** (2 * m), 2 ** (1 * m)))
        for y0 in range(2 ** m):
            for lambda_1 in range(2 ** m):
                for v0 in range(2 ** m):
                    input = (y0 << m) + lambda_1
                    output = v0
                    if (vector_inner_product(v0, y0, m) == 0):
                        table[input, output] = 1
                    else:
                        table[input, output] = -1

        return table

    def matrix_e(sbox):
        table = numpy.zeros((2 ** (2 * n), 2 ** (2 * m)))
        for x0 in range(2 ** n):
            for delta_2 in range(2 ** n):
                for y0 in range(2 ** m):
                    for lambda_1 in range(2 ** m):
                        output = (x0 << n) + delta_2
                        input = (y0 << m) + lambda_1
                        if (y0 == sbox[x0]) and (lambda_1 == sbox[x0] ^ sbox[x0 ^ delta_1]) and (
                                lambda_2 == sbox[x0] ^ sbox[x0 ^ delta_2]) and (
                                lambda_1 ^ lambda_2 == sbox[x0] ^ sbox[x0 ^ delta_1 ^ delta_2]):
                            table[input, output] = 1

        return table

    def matrix_e1(sbox):
        table = numpy.zeros((2 ** (1 * n), 2 ** (1 * m)))
        for x in range(2 ** n):
            for u0 in range(2 ** n):
                for v0 in range(2 ** m):
                    for delta_2 in range(2 ** n):
                        output = u0
                        input = v0
                        if (sbox[x] ^ sbox[x ^ delta_2] == lambda_2) and (
                                sbox[x] ^ sbox[x ^ delta_1 ^ delta_2] == lambda_2 ^ sbox[x] ^ sbox[x ^ delta_1]):
                            if vector_inner_product(u0, x, n) ^ vector_inner_product(
                                v0, sbox[x], m) == 0:
                                table[input, output] += 1
                            else:
                                table[input, output] -= 1

        for input in range(2 ** (1 * n)):
            for output in range(2 ** (1 * m)):
                if table[input, output] != 0:
                    table[input, output] = table[input, output] / (2 ** (2 * n))

        return table

    e1 = matrix_e1(sbox)
    quasi_bct = e1

    return quasi_bct

def get_ddt_lower_matrices_2n_by_zeros_u1_v1_and_given_delta_2_and_lambda_2(sbox, n, m, delta_2, lambda_2):
    # f1 : (x, delta_1, delta_2) -> (u0, u1, u2)
    def matrix_f1():
        table = numpy.zeros((2 ** (2 * n), 2 ** (1 * n)))
        for u0 in range(2 ** n):
            for x0 in range(2 ** n):
                for delta_1 in range(2 ** n):
                    input = (x0 << n) + delta_1
                    output = u0
                    if (vector_inner_product(u0, x0, n) == 0):
                        table[input, output] = 1
                    else:
                        table[input, output] = -1

        return table

    # f2 : (y, lambda_1, lambda_2) -> (v0, v1, v2)
    def matrix_f2():
        table = numpy.zeros((2 ** (2 * m), 2 ** (1 * m)))
        for y0 in range(2 ** m):
            for lambda_1 in range(2 ** m):
                for v0 in range(2 ** m):
                    input = (y0 << m) + lambda_1
                    output = v0
                    if (vector_inner_product(v0, y0, m) == 0):
                        table[input, output] = 1
                    else:
                        table[input, output] = -1

        return table

    def matrix_e(sbox):
        table = numpy.zeros((2 ** (2 * n), 2 ** (2 * m)))
        for x0 in range(2 ** n):
            for delta_1 in range(2 ** n):
                for y0 in range(2 ** m):
                    for lambda_1 in range(2 ** m):
                        output = (x0 << n) + delta_1
                        input = (y0 << m) + lambda_1
                        if (y0 == sbox[x0]) and (lambda_1 == sbox[x0] ^ sbox[x0 ^ delta_1]) and (
                                lambda_2 == sbox[x0] ^ sbox[x0 ^ delta_2]) and (
                                lambda_1 ^ lambda_2 == sbox[x0] ^ sbox[x0 ^ delta_1 ^ delta_2]):
                            table[input, output] = 1

        return table

    def matrix_e1(sbox):
        table = numpy.zeros((2 ** (1 * n), 2 ** (1 * m)))
        for x in range(2 ** n):
            for u0 in range(2 ** n):
                for v0 in range(2 ** m):
                    for delta_1 in range(2 ** n):
                        output = u0
                        input = v0
                        if (sbox[x] ^ sbox[x ^ delta_2] == lambda_2) and (
                                sbox[x] ^ sbox[x ^ delta_1 ^ delta_2] == lambda_2 ^ sbox[x] ^ sbox[x ^ delta_1]):
                            if vector_inner_product(u0, x, n) ^ vector_inner_product(
                                v0, sbox[x], m) == 0:
                                table[input, output] += 1
                            else:
                                table[input, output] -= 1

        for input in range(2 ** (1 * n)):
            for output in range(2 ** (1 * m)):
                if table[input, output] != 0:
                    table[input, output] = table[input, output] / (2 ** (2 * n))

        return table

    e1 = matrix_e1(sbox)
    quasi_ddt = e1

    return quasi_ddt

def get_ddt_upper_matrices_2n_by_given_delta_1_lambda_1_delta_2_lambda_2(sbox, n, m, delta_1, lambda_1, delta_2, lambda_2):
    # f1 : (x, delta_1, delta_2) -> (u0, u1, u2)
    def matrix_f1():
        table = numpy.zeros((2 ** (1 * n), 2 ** (2 * n)))
        for u0 in range(2 ** n):
            for u2 in range(2 ** n):
                for x0 in range(2 ** n):
                    input = x0
                    output = (u0 << n) + u2
                    if (vector_inner_product(u0, x0, n) ^ vector_inner_product(u2, delta_2, n) == 0):
                        table[input, output] = 1
                    else:
                        table[input, output] = -1

        return table

    # f2 : (y, lambda_1, lambda_2) -> (v0, v1, v2)
    def matrix_f2():
        table = numpy.zeros((2 ** (1 * n), 2 ** (2 * n)))
        for y0 in range(2 ** m):
            for v0 in range(2 ** m):
                for v2 in range(2 ** m):
                    input = y0
                    output = (v0 << m) + v2
                    if (vector_inner_product(v0, y0, m) ^ vector_inner_product(v2, lambda_2, n) == 0):
                        table[input, output] = 1
                    else:
                        table[input, output] = -1

        return table

    def matrix_e(sbox):
        table = numpy.zeros((2 ** (1 * n), 2 ** (1 * m)))
        for x0 in range(2 ** n):
            for y0 in range(2 ** m):
                output = x0
                input = y0
                if (y0 == sbox[x0]) and (lambda_1 == sbox[x0] ^ sbox[x0 ^ delta_1]) and (
                        lambda_2 == sbox[x0] ^ sbox[x0 ^ delta_2]) and (
                        lambda_1 ^ lambda_2 == sbox[x0] ^ sbox[x0 ^ delta_1 ^ delta_2]):
                    table[input, output] = 1

        return table

    def matrix_e1(sbox):
        table = numpy.zeros((2 ** (2 * n), 2 ** (2 * m)))
        for x in range(2 ** n):
            for u0 in range(2 ** n):
                for u2 in range(2 ** n):
                    for v0 in range(2 ** m):
                        for v2 in range(2 ** m):
                            output = (u0 << n) + u2
                            input = (v0 << m) + v2
                            if (sbox[x] ^ sbox[x ^ delta_1] == lambda_1) and (
                                    sbox[x] ^ sbox[x ^ delta_1 ^ delta_2] == lambda_1 ^ sbox[x] ^ sbox[x ^ delta_2]):
                                if vector_inner_product(u0, x, n) ^ vector_inner_product(u2, delta_2,
                                                                                         n) ^ vector_inner_product(
                                    v0, sbox[x], m) ^ vector_inner_product(v2,
                                                                           sbox[x] ^ sbox[x ^ delta_2],
                                                                           m) == 0:
                                    table[input, output] += 1
                                else:
                                    table[input, output] -= 1

        for input in range(2 ** (2 * n)):
            for output in range(2 ** (2 * m)):
                if table[input, output] != 0:
                    table[input, output] = table[input, output] / (2 ** (2 * n))

        return table

    e1 = matrix_e1(sbox)
    quasi_ddt = e1

    return quasi_ddt

def get_bct_matrices_2n_by_given_delta_1_lambda_2_delta_2_lambda_1(sbox, n, m, delta_1, lambda_2, delta_2, lambda_1):
    def matrix_f1():
        table = numpy.zeros((2 ** (1 * n), 2 ** (2 * n)))
        for u0 in range(2 ** n):
            for u2 in range(2 ** n):
                for x0 in range(2 ** n):
                    input = x0
                    output = (u0 << n) + u2
                    if (vector_inner_product(u0, x0, n) ^ vector_inner_product(u2, delta_2, n) == 0):
                        table[input, output] = 1
                    else:
                        table[input, output] = -1
        return table

    # f2 : (y, lambda_1, lambda_2) -> (v0, v1, v2)
    def matrix_f2():
        table = numpy.zeros((2 ** (1 * n), 2 ** (2 * n)))
        for y0 in range(2 ** m):
            for v0 in range(2 ** m):
                for v1 in range(2 ** m):
                    input = y0
                    output = (v0 << m) + v1
                    if (vector_inner_product(v0, y0, m) ^ vector_inner_product(v1, lambda_1, n) == 0):
                        table[input, output] = 1
                    else:
                        table[input, output] = -1

        return table

    def matrix_e(sbox):
        table = numpy.zeros((2 ** (1 * n), 2 ** (1 * m)))
        for x0 in range(2 ** n):
            for y0 in range(2 ** m):
                output = x0
                input = y0
                if (y0 == sbox[x0]) and (lambda_1 == sbox[x0] ^ sbox[x0 ^ delta_1]) and (
                        lambda_2 == sbox[x0] ^ sbox[x0 ^ delta_2]) and (
                        lambda_1 ^ lambda_2 == sbox[x0] ^ sbox[x0 ^ delta_1 ^ delta_2]):
                    table[input, output] = 1

        return table

    def matrix_e1(sbox):
        table = numpy.zeros((2 ** (2 * n), 2 ** (2 * m)))
        for x in range(2 ** n):
            for u0 in range(2 ** n):
                for u2 in range(2 ** n):
                    for v0 in range(2 ** m):
                        for v1 in range(2 ** m):
                            output = (u0 << n) + u2
                            input = (v0 << m) + v1
                            if (sbox[x] ^ sbox[x ^ delta_2] == lambda_2) and (
                                    sbox[x] ^ sbox[x ^ delta_1 ^ delta_2] == lambda_2 ^ sbox[x] ^ sbox[x ^ delta_1]):
                                if vector_inner_product(u0, x, n) ^ vector_inner_product(u2, delta_2,
                                                                                         n) ^ vector_inner_product(
                                    v0, sbox[x], m) ^ vector_inner_product(v1,
                                                                           sbox[x] ^ sbox[x ^ delta_1],
                                                                           m) == 0:
                                    table[input, output] += 1
                                else:
                                    table[input, output] -= 1

        for input in range(2 ** (2 * n)):
            for output in range(2 ** (2 * m)):
                if table[input, output] != 0:
                    table[input, output] = table[input, output] / (2 ** (2 * n))

        return table

    e1 = matrix_e1(sbox)
    quasi_bct = e1

    return quasi_bct

def get_ddt_lower_matrices_2n_by_given_delta_2_lambda_2_delta_1_lambda_1(sbox, n, m, delta_2, lambda_2, delta_1, lambda_1):
    # f1 : (x, delta_1, delta_2) -> (u0, u1, u2)
    def matrix_f1():
        table = numpy.zeros((2 ** (1 * n), 2 ** (2 * n)))
        for u0 in range(2 ** n):
            for u1 in range(2 ** n):
                for x0 in range(2 ** n):
                    input = x0
                    output = (u0 << n) + u1
                    if (vector_inner_product(u0, x0, n) ^ vector_inner_product(u1, delta_1, n) == 0):
                        table[input, output] = 1
                    else:
                        table[input, output] = -1

        return table

    # f2 : (y, lambda_1, lambda_2) -> (v0, v1, v2)
    def matrix_f2():
        table = numpy.zeros((2 ** (1 * m), 2 ** (2 * m)))
        for y0 in range(2 ** m):
            for v0 in range(2 ** m):
                for v1 in range(2 ** m):
                    input = y0
                    output = (v0 << m) + v1
                    if (vector_inner_product(v0, y0, m) ^ vector_inner_product(v1, lambda_1, n) == 0):
                        table[input, output] = 1
                    else:
                        table[input, output] = -1

        return table

    def matrix_e(sbox):
        table = numpy.zeros((2 ** (1 * n), 2 ** (1 * m)))
        for x0 in range(2 ** n):
            for y0 in range(2 ** m):
                output = x0
                input = y0
                if (y0 == sbox[x0]) and (lambda_1 == sbox[x0] ^ sbox[x0 ^ delta_1]) and (
                        lambda_2 == sbox[x0] ^ sbox[x0 ^ delta_2]) and (
                        lambda_1 ^ lambda_2 == sbox[x0] ^ sbox[x0 ^ delta_1 ^ delta_2]):
                    table[input, output] = 1

        return table

    def matrix_e1(sbox):
        table = numpy.zeros((2 ** (2 * n), 2 ** (2 * m)))
        for x in range(2 ** n):
            for u0 in range(2 ** n):
                for u1 in range(2 ** n):
                    for v0 in range(2 ** m):
                        for v1 in range(2 ** m):
                            output = (u0 << n) + u1
                            input = (v0 << m) + v1
                            if (sbox[x] ^ sbox[x ^ delta_2] == lambda_2) and (
                                    sbox[x] ^ sbox[x ^ delta_1 ^ delta_2] == lambda_2 ^ sbox[x] ^ sbox[x ^ delta_1]):
                                if vector_inner_product(u0, x, n) ^ vector_inner_product(u1, delta_1,
                                                                                         n) ^ vector_inner_product(
                                    v0, sbox[x], m) ^ vector_inner_product(v1,
                                                                           sbox[x] ^ sbox[x ^ delta_1],
                                                                           m) == 0:
                                    table[input, output] += 1
                                else:
                                    table[input, output] -= 1

        for input in range(2 ** (2 * n)):
            for output in range(2 ** (2 * m)):
                if table[input, output] != 0:
                    table[input, output] = table[input, output] / (2 ** (2 * n))

        return table

    e1 = matrix_e1(sbox)
    quasi_ddt = e1

    return quasi_ddt

def get_ddt_upper_matrices_2n_by_zeros_u0_v0_and_given_delta_1_and_lambda_1(sbox, n, m, delta_1, lambda_1):

    def matrix_e1(sbox):
        table = numpy.zeros((2 ** (1 * n), 2 ** (1 * m)))
        for x in range(2 ** n):
            for u2 in range(2 ** n):
                for v2 in range(2 ** m):
                    for delta_2 in range(2 ** n):
                        output = u2
                        input = v2
                        if (sbox[x] ^ sbox[x ^ delta_1] == lambda_1) and (
                                sbox[x] ^ sbox[x ^ delta_1 ^ delta_2] == lambda_1 ^ sbox[x] ^ sbox[x ^ delta_2]):
                            if vector_inner_product(u2, delta_2, n) ^ vector_inner_product(v2, sbox[x] ^ sbox[x ^ delta_2], m) == 0:
                                table[input, output] += 1
                            else:
                                table[input, output] -= 1

        for input in range(2 ** (1 * n)):
            for output in range(2 ** (1 * m)):
                if table[input, output] != 0:
                    table[input, output] = table[input, output] / (2 ** (2 * n))

        return table

    e1 = matrix_e1(sbox)
    quasi_ddt = e1

    return quasi_ddt

def get_bct_matrices_2n_by_zeros_u0_v0_and_given_delta_1_and_lambda_2(sbox, n, m, delta_1, lambda_2):

    def matrix_e1(sbox):
        table = numpy.zeros((2 ** (1 * n), 2 ** (1 * m)))
        for x in range(2 ** n):
            for u2 in range(2 ** n):
                for v1 in range(2 ** m):
                    for delta_2 in range(2 ** n):
                        output = u2
                        input = v1
                        if (sbox[x] ^ sbox[x ^ delta_2] == lambda_2) and (
                                sbox[x] ^ sbox[x ^ delta_1 ^ delta_2] == lambda_2 ^ sbox[x] ^ sbox[x ^ delta_1]):
                            if vector_inner_product(u2, delta_2, n) ^ vector_inner_product(v1, sbox[x] ^ sbox[x ^ delta_1], m) == 0:
                                table[input, output] += 1
                            else:
                                table[input, output] -= 1

        for input in range(2 ** (1 * n)):
            for output in range(2 ** (1 * m)):
                if table[input, output] != 0:
                    table[input, output] = table[input, output] / (2 ** (2 * n))

        return table

    e1 = matrix_e1(sbox)
    quasi_bct = e1

    return quasi_bct

def get_ddt_lower_matrices_2n_by_zeros_u0_v0_and_given_delta_2_and_lambda_2(sbox, n, m, delta_2, lambda_2):

    def matrix_e1(sbox):
        table = numpy.zeros((2 ** (1 * n), 2 ** (1 * m)))
        for x in range(2 ** n):
            for u1 in range(2 ** n):
                for v1 in range(2 ** m):
                    for delta_1 in range(2 ** n):
                        output = u1
                        input = v1
                        if (sbox[x] ^ sbox[x ^ delta_2] == lambda_2) and (
                                sbox[x] ^ sbox[x ^ delta_1 ^ delta_2] == lambda_2 ^ sbox[x] ^ sbox[x ^ delta_1]):
                            if vector_inner_product(u1, delta_1, n) ^ vector_inner_product(v1, sbox[x] ^ sbox[x ^ delta_1], m) == 0:
                                table[input, output] += 1
                            else:
                                table[input, output] -= 1

        for input in range(2 ** (1 * n)):
            for output in range(2 ** (1 * m)):
                if table[input, output] != 0:
                    table[input, output] = table[input, output] / (2 ** (2 * n))

        return table

    e1 = matrix_e1(sbox)
    quasi_ddt = e1

    return quasi_ddt

def get_ddt_upper_matrices_2n_by_u0_v0_and_given_delta_1_and_lambda_1(sbox, n, m, u0, v0, delta_1, lambda_1):

    def matrix_e1(sbox):
        table = numpy.zeros((2 ** (1 * n), 2 ** (1 * m)))
        for x in range(2 ** n):
            for u2 in range(2 ** n):
                for v2 in range(2 ** m):
                    for delta_2 in range(2 ** n):
                        output = u2
                        input = v2
                        if (sbox[x] ^ sbox[x ^ delta_1] == lambda_1) and (
                                sbox[x] ^ sbox[x ^ delta_1 ^ delta_2] == lambda_1 ^ sbox[x] ^ sbox[x ^ delta_2]):
                            if vector_inner_product(u0, x, n) ^ vector_inner_product(u2, delta_2,
                                                                                     n) ^ vector_inner_product(
                                v0, sbox[x], m) ^ vector_inner_product(v2,
                                                                       sbox[x] ^ sbox[x ^ delta_2],
                                                                       m) == 0:
                                table[input, output] += 1
                            else:
                                table[input, output] -= 1

        for input in range(2 ** (1 * n)):
            for output in range(2 ** (1 * m)):
                if table[input, output] != 0:
                    table[input, output] = table[input, output] / (2 ** (2 * n))

        return table

    e1 = matrix_e1(sbox)

    return e1

def get_bct_matrices_2n_by_u0_v0_and_given_delta_1_and_lambda_2(sbox, n, m, u0, v0, delta_1, lambda_2):

    def matrix_e1(sbox):
        table = numpy.zeros((2 ** (1 * n), 2 ** (1 * m)))
        for x in range(2 ** n):
            for u2 in range(2 ** n):
                for v1 in range(2 ** m):
                    for delta_2 in range(2 ** n):
                        output = u2
                        input = v1
                        if (sbox[x] ^ sbox[x ^ delta_2] == lambda_2) and (
                                sbox[x] ^ sbox[x ^ delta_1 ^ delta_2] == lambda_2 ^ sbox[x] ^ sbox[x ^ delta_1]):
                            if vector_inner_product(u0, x, n) ^ vector_inner_product(u2, delta_2,
                                                                                     n) ^ vector_inner_product(
                                v0, sbox[x], m) ^ vector_inner_product(v1,
                                                                       sbox[x] ^ sbox[x ^ delta_1],
                                                                       m) == 0:
                                table[input, output] += 1
                            else:
                                table[input, output] -= 1

        for input in range(2 ** (1 * n)):
            for output in range(2 ** (1 * m)):
                if table[input, output] != 0:
                    table[input, output] = table[input, output] / (2 ** (2 * n))

        return table

    e1 = matrix_e1(sbox)

    return e1

def get_ddt_lower_matrices_2n_by_u0_v0_and_given_delta_2_and_lambda_2(sbox, n, m, u0, v0, delta_2, lambda_2):

    def matrix_e1(sbox):
        table = numpy.zeros((2 ** (1 * n), 2 ** (1 * m)))
        for x in range(2 ** n):
            for u1 in range(2 ** n):
                for v1 in range(2 ** m):
                    for delta_1 in range(2 ** n):
                        output = u1
                        input = v1
                        if (sbox[x] ^ sbox[x ^ delta_2] == lambda_2) and (
                                sbox[x] ^ sbox[x ^ delta_1 ^ delta_2] == lambda_2 ^ sbox[x] ^ sbox[x ^ delta_1]):
                            if vector_inner_product(u0, x, n) ^ vector_inner_product(u1, delta_1,
                                                                                     n) ^ vector_inner_product(
                                v0, sbox[x], m) ^ vector_inner_product(v1,
                                                                       sbox[x] ^ sbox[x ^ delta_1],
                                                                       m) == 0:
                                table[input, output] += 1
                            else:
                                table[input, output] -= 1

        for input in range(2 ** (1 * n)):
            for output in range(2 ** (1 * m)):
                if table[input, output] != 0:
                    table[input, output] = table[input, output] / (2 ** (2 * n))

        return table

    e1 = matrix_e1(sbox)

    return e1



def get_ddt_upper_item_by_given_all(sbox, n, m, u0, v0, delta_1, lambda_1, u2, v2):

    def matrix_e1(sbox):
        count_i = 0
        for x in range(2 ** n):
            for delta_2 in range(2 ** n):
                if (sbox[x] ^ sbox[x ^ delta_1] == lambda_1) and (
                        sbox[x] ^ sbox[x ^ delta_1 ^ delta_2] == lambda_1 ^ sbox[x] ^ sbox[x ^ delta_2]):
                    if vector_inner_product(u0, x, n) ^ vector_inner_product(u2, delta_2,
                                                                             n) ^ vector_inner_product(
                        v0, sbox[x], m) ^ vector_inner_product(v2,
                                                               sbox[x] ^ sbox[x ^ delta_2],
                                                               m) == 0:
                        count_i += 1
                    else:
                        count_i -= 1

        if count_i != 0:
            count_i = count_i / (2 ** (2 * n))

        return count_i

    count_i = matrix_e1(sbox)

    return count_i

def get_bct_item_by_given_all(sbox, n, m, u0, v0, delta_1, v1, u2, lambda_2):

    def matrix_e1(sbox):
        count_i = 0
        for x in range(2 ** n):
            for delta_2 in range(2 ** n):
                if (sbox[x] ^ sbox[x ^ delta_2] == lambda_2) and (
                        sbox[x] ^ sbox[x ^ delta_1 ^ delta_2] == lambda_2 ^ sbox[x] ^ sbox[x ^ delta_1]):
                    if vector_inner_product(u0, x, n) ^ vector_inner_product(u2, delta_2,
                                                                             n) ^ vector_inner_product(
                        v0, sbox[x], m) ^ vector_inner_product(v1,
                                                               sbox[x] ^ sbox[x ^ delta_1],
                                                               m) == 0:
                        count_i += 1
                    else:
                        count_i -= 1

        if count_i != 0:
            count_i = count_i / (2 ** (2 * n))

        return count_i

    count_i = matrix_e1(sbox)

    return count_i

def get_ddt_lower_item_by_given_all(sbox, n, m, u0, v0, u1, v1, delta_2, lambda_2):

    def matrix_e1(sbox):
        count_i = 0
        for x in range(2 ** n):
            for delta_1 in range(2 ** n):
                if (sbox[x] ^ sbox[x ^ delta_2] == lambda_2) and (
                        sbox[x] ^ sbox[x ^ delta_1 ^ delta_2] == lambda_2 ^ sbox[x] ^ sbox[x ^ delta_1]):
                    if vector_inner_product(u0, x, n) ^ vector_inner_product(u1, delta_1,
                                                                             n) ^ vector_inner_product(
                        v0, sbox[x], m) ^ vector_inner_product(v1,
                                                               sbox[x] ^ sbox[x ^ delta_1],
                                                               m) == 0:
                        count_i += 1
                    else:
                        count_i -= 1

        if count_i != 0:
            count_i = count_i / (2 ** (2 * n))

        return count_i

    count_i = matrix_e1(sbox)

    return count_i