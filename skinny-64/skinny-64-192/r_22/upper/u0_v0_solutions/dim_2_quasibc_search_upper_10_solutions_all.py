
import numpy, pyboolector
import generate_tables as tables
from multiprocessing import Pool

SKINNY_64_SBOX = [0xc, 0x6, 0x9, 0x0, 0x1, 0xa, 0x2, 0xb, 0x3, 0x8, 0x5, 0xd, 0x4, 0xe, 0x7, 0xf]
# SKINNY_64_INVERSE_SBOX = [0x3, 4, 6, 8, 12, 10, 1, 14, 9, 2, 5, 7, 0, 11, 13, 15]
n = 4
m = 4
sbox = SKINNY_64_SBOX
# sbox_inverse = SKINNY_64_INVERSE_SBOX
state_bits = 64
state_words = 16
sbox_bits = 4

dim_n = 2

differential_characteristic_rounds_upper = 10

rc_6_bits = [
    0x01, 0x03, 0x07, 0x0F, 0x1F, 0x3E, 0x3D, 0x3B, 0x37, 0x2F, 0x1E, 0x3C, 0x39, 0x33, 0x27, 0x0E,
    0x1D, 0x3A, 0x35, 0x2B, 0x16, 0x2C, 0x18, 0x30, 0x21, 0x02, 0x05, 0x0B, 0x17, 0x2E, 0x1C, 0x38,
    0x31, 0x23, 0x06, 0x0D, 0x1B, 0x36, 0x2D, 0x1A, 0x34, 0x29, 0x12, 0x24, 0x08, 0x11, 0x22, 0x04]


def get_sr_table_by_n(bit_n):
    table = []
    for i in range(4 * n):
        table.append(i)
    for i in range(7 * n, 8 * n):
        table.append(i)
    for i in range(4 * n, 7 * n):
        table.append(i)
    for i in range(10 * n, 12 * n):
        table.append(i)
    for i in range(8 * n, 10 * n):
        table.append(i)
    for i in range(13 * n, 16 * n):
        table.append(i)
    for i in range(12 * n, 13 * n):
        table.append(i)

    return table


sr_bits_table = get_sr_table_by_n(sbox_bits)


def get_matrix_table_by_n(bit_n):
    table = []
    for i in range(4 * n):
        one_bit_table = [i, i + 8 * n, i + 12 * n]
        table.append(one_bit_table)
    for i in range(4 * n, 8 * n):
        one_bit_table = [i - 4 * n]
        table.append(one_bit_table)
    for i in range(8 * n, 12 * n):
        one_bit_table = [i - 4 * n, i]
        table.append(one_bit_table)
    for i in range(12 * n, 16 * n):
        one_bit_table = [i - 12 * n, i - 4 * n]
        table.append(one_bit_table)

    return table


mc_bits_table = get_matrix_table_by_n(sbox_bits)


def get_matrix_t_table_by_n(n):
    table = []
    for i in range(4 * n):
        one_bit_table = [i, i + 4 * n, i + 12 * n]
        table.append(one_bit_table)
    for i in range(4 * n, 8 * n):
        one_bit_table = [i + 4 * n]
        table.append(one_bit_table)
    for i in range(8 * n, 12 * n):
        one_bit_table = [i - 8 * n, i, i + 4 * n]
        table.append(one_bit_table)
    for i in range(12 * n, 16 * n):
        one_bit_table = [i - 12 * n]
        table.append(one_bit_table)

    return table


mc_t_bits_table = get_matrix_t_table_by_n(sbox_bits)


def get_tables_weight_lists_w_0_to_7(table, dim_n, is_ddt):
    weight_list_w_0_to_7 = []
    for w in range(0, 8):
        weight_list_w_0_to_7.append([])

    if dim_n == 2:
        for u in range(2 ** n):
            for uu in range(2 ** n):
                for v in range(2 ** m):
                    for vv in range(2 ** m):
                        input = (v << m) + vv
                        output = (u << n) + uu
                        c = table[input, output]
                        if is_ddt == 0:
                            c *= (2 ** n)
                        if c != 0:
                            w = int(abs(numpy.log2(abs(c))))
                            # print("c != 0 : c = {}, w = {}, int w = {}".format(c, w, int(w)))
                            weight_list_w_0_to_7[w].append([u, uu, v, vv])
    elif dim_n == 1:
        for u in range(2 ** n):
            for v in range(2 ** m):
                input = v
                output = u
                c = table[input, output]
                if is_ddt == 0:
                    c *= (2 ** n)
                if c != 0:
                    w = int(abs(numpy.log2(abs(c))))
                    # print("c != 0 : c = {}, w = {}, int w = {}".format(c, w, int(w)))
                    weight_list_w_0_to_7[w].append([u, v])

    print("---------------------------------")

    return weight_list_w_0_to_7


def compute_sign(route_u0, route_u1, diff_route, round_upper):
    correlation_sign = 0

    # upper
    for r in range(round_upper):
        u0 = route_u0[4 * r]
        u1 = route_u1[4 * r]
        delta_in_1 = diff_route[4 * r]
        v0 = route_u0[4 * r + 1]
        v1 = route_u1[4 * r + 1]
        delta_out_1 = diff_route[4 * r + 1]

        for i in range(0, state_words):
            uu0 = (u0 >> (4 * i)) & (2 ** sbox_bits - 1)
            uu1 = (u1 >> (4 * i)) & (2 ** sbox_bits - 1)
            di1 = (delta_in_1 >> (4 * i)) & (2 ** sbox_bits - 1)
            vv0 = (v0 >> (4 * i)) & (2 ** sbox_bits - 1)
            vv1 = (v1 >> (4 * i)) & (2 ** sbox_bits - 1)
            do1 = (delta_out_1 >> (4 * i)) & (2 ** sbox_bits - 1)

            c = tables.get_ddt_upper_item_by_given_all(sbox, n, m, uu0, vv0, di1, do1, uu1, vv1)
            if c < 0:
                correlation_sign += 1

    # add constants
    for r in range(round_upper):
        rcs = rc_6_bits[r]
        c0 = rcs & 0xf
        c1 = (rcs >> 4) & 0x3
        c2 = 0x2
        mask_c = (c2 << (8 * sbox_bits)) | (c1 << (4 * sbox_bits)) | c0
        mask_u = route_u0[4 * r + 1]
        correlation_sign += bin(mask_c & mask_u).count('1')

    return (-1) ** correlation_sign


# quasidifferential one_solution_search
def get_quasidifferentials_by_one_fixed_input_and_output(diff_route, route_number, min_weight, max_weight):
    def search_differential(f):
        # differential_characteristic_rounds = differential_characteristic_rounds_upper + differential_characteristic_rounds_lower

        btor = pyboolector.Boolector()
        btor.Set_opt(pyboolector.BTOR_OPT_MODEL_GEN, 1)

        # difference
        # input
        u0_a = [btor.Var(btor.BitVecSort(state_bits), "u0_a%d" % i) for i in
                range(differential_characteristic_rounds_upper + 1)]
        u1_a = [btor.Var(btor.BitVecSort(state_bits), "u1_a%d" % i) for i in
                range(differential_characteristic_rounds_upper + 1)]
        # u2_a = [btor.Var(btor.BitVecSort(state_bits), "u2_a%d" % i) for i in range(differential_characteristic_rounds_upper + differential_characteristic_rounds_lower + 1)]
        # after sb
        u0_b = [btor.Var(btor.BitVecSort(state_bits), "u0_b%d" % i) for i in
                range(differential_characteristic_rounds_upper)]
        u1_b = [btor.Var(btor.BitVecSort(state_bits), "u1_b%d" % i) for i in
                range(differential_characteristic_rounds_upper)]
        # u2_b = [btor.Var(btor.BitVecSort(state_bits), "u2_b%d" % i) for i in range(differential_characteristic_rounds_upper + differential_characteristic_rounds_lower)]
        # after_k
        u0_c = [btor.Var(btor.BitVecSort(state_bits), "u0_c%d" % i) for i in
                range(differential_characteristic_rounds_upper)]
        u1_c = [btor.Var(btor.BitVecSort(state_bits), "u1_c%d" % i) for i in
                range(differential_characteristic_rounds_upper)]
        # u2_c = [btor.Var(btor.BitVecSort(state_bits), "u2_c%d" % i) for i in range(differential_characteristic_rounds_upper + differential_characteristic_rounds_lower)]
        # after sr
        u0_d = [btor.Var(btor.BitVecSort(state_bits), "u0_d%d" % i) for i in
                range(differential_characteristic_rounds_upper)]
        u1_d = [btor.Var(btor.BitVecSort(state_bits), "u1_d%d" % i) for i in
                range(differential_characteristic_rounds_upper)]

        # u2_d = [btor.Var(btor.BitVecSort(state_bits), "u2_d%d" % i) for i in range(differential_characteristic_rounds_upper + differential_characteristic_rounds_lower)]

        def xor_k_diff(x, y, k):
            print(k)
            for i in range(state_bits):
                btor.Assert(y[i] == x[i] ^ ((k >> i) & 0x1))

        def xor_k_mask(x, y):
            for i in range(state_bits):
                btor.Assert(y[i] == x[i])

        def permute_bits_sr(x, y):
            for i in range(state_bits):
                btor.Assert(y[i] == x[sr_bits_table[i]])

        def mix_columns(x, y):
            for i in range(state_bits):
                one_bit_table = mc_bits_table[i]
                temp = btor.Const(0)
                for j in range(len(one_bit_table)):
                    temp ^= x[one_bit_table[j]]
                btor.Assert(y[i] == temp)

        def mix_t_columns(x, y):
            for i in range(state_bits):
                one_bit_table = mc_t_bits_table[i]
                temp = btor.Const(0)
                for j in range(len(one_bit_table)):
                    temp ^= y[one_bit_table[j]]
                btor.Assert(x[i] == temp)

        def get_one_words_weight_by_small_quasi_table(u, uu, v, vv, small_table_weight_lists_w_0_to_7):
            weight0 = btor.Const(0)
            weight1 = btor.Const(0)
            weight2 = btor.Const(0)
            weight3 = btor.Const(0)
            weight4 = btor.Const(0)
            weight5 = btor.Const(0)
            weight6 = btor.Const(0)
            weight7 = btor.Const(0)
            for tw in range(len(small_table_weight_lists_w_0_to_7)):
                table_weight_list_w = small_table_weight_lists_w_0_to_7[tw]
                if len((table_weight_list_w)) > 0:
                    for one_group in table_weight_list_w:
                        u0 = one_group[0]
                        uu0 = one_group[1]
                        v0 = one_group[2]
                        vv0 = one_group[3]
                        if tw == 0:
                            weight0 |= (u == u0) & (uu == uu0) & (v == v0) & (vv == vv0)
                        elif tw == 1:
                            weight1 |= (u == u0) & (uu == uu0) & (v == v0) & (vv == vv0)
                        elif tw == 2:
                            weight2 |= (u == u0) & (uu == uu0) & (v == v0) & (vv == vv0)
                        elif tw == 3:
                            weight3 |= (u == u0) & (uu == uu0) & (v == v0) & (vv == vv0)
                        elif tw == 4:
                            weight4 |= (u == u0) & (uu == uu0) & (v == v0) & (vv == vv0)
                        elif tw == 5:
                            weight5 |= (u == u0) & (uu == uu0) & (v == v0) & (vv == vv0)
                        elif tw == 6:
                            weight6 |= (u == u0) & (uu == uu0) & (v == v0) & (vv == vv0)
                        elif tw == 7:
                            weight7 |= (u == u0) & (uu == uu0) & (v == v0) & (vv == vv0)

            btor.Assert(weight0 | weight1 | weight2 | weight3 | weight4 | weight5 | weight6 | weight7)
            return btor.Cond(
                weight1, btor.Const(1, state_words),
                btor.Cond(
                    weight2, btor.Const(2, state_words),
                    btor.Cond(
                        weight3, btor.Const(3, state_words),
                        btor.Cond(
                            weight4, btor.Const(4, state_words),
                            btor.Cond(
                                weight5, btor.Const(5, state_words),
                                btor.Cond(
                                    weight6, btor.Const(6, state_words),
                                    btor.Cond(
                                        weight7, btor.Const(7, state_words),
                                        btor.Const(0, state_words)
                                    )
                                )
                            )
                        )
                    )
                )
            )

        def set_fixed_difference(state, difference):
            for i in range(state_bits):
                btor.Assert(state[i] == ((difference >> i) & 0x1))

        # cost = btor.Const(0, state_words)
        cost_upper = btor.Const(0, state_words)
        cost_lower = btor.Const(0, state_words)
        cost_em = btor.Const(0, state_words)

        count_ddt_upper = []
        count_bct = []
        count_ddt_lower = []

        table_ddt_upper = []
        table_bct = []
        table_ddt_lower = []

        # the upper
        print("upper biddt:")
        for i in range(differential_characteristic_rounds_upper):
            for j in range(0, state_bits, sbox_bits):
                uu0 = u0_a[i][j + sbox_bits - 1:j]
                vv0 = u0_b[i][j + sbox_bits - 1:j]
                uu1 = u1_a[i][j + sbox_bits - 1:j]
                vv1 = u1_b[i][j + sbox_bits - 1:j]
                # uu2 = u2_a[i][j + sbox_bits - 1:j]
                # vv2 = u2_b[i][j + sbox_bits - 1:j]
                delta_in_1 = (diff_route[4 * i] >> j) & (2 ** sbox_bits - 1)
                delta_out_1 = (diff_route[4 * i + 1] >> j) & (2 ** sbox_bits - 1)

                deltas = [delta_in_1, delta_out_1]
                if deltas not in count_ddt_upper:
                    print("0x{:01x} -> 0x{:01x}".format(delta_in_1, delta_out_1))
                    count_ddt_upper.append(deltas)
                    small_quasi_ddt = tables.get_ddt_upper_matrices_2n_by_given_delta_1_and_lambda_1(sbox, n, m,
                                                                                                     delta_in_1,
                                                                                                     delta_out_1)
                    small_quasi_ddt_weight_lists_w_0_to_7 = get_tables_weight_lists_w_0_to_7(small_quasi_ddt, dim_n, 1)
                    w = get_one_words_weight_by_small_quasi_table(uu0, uu1, vv0, vv1,
                                                                  small_quasi_ddt_weight_lists_w_0_to_7)
                    # cost_upper += w
                    cost_upper += w
                    table_ddt_upper.append(small_quasi_ddt_weight_lists_w_0_to_7)
                elif deltas in count_ddt_upper:
                    position = count_ddt_upper.index(deltas)
                    small_quasi_ddt_weight_lists_w_0_to_7 = table_ddt_upper[position]
                    w = get_one_words_weight_by_small_quasi_table(uu0, uu1, vv0, vv1,
                                                                  small_quasi_ddt_weight_lists_w_0_to_7)
                    # cost_upper += w
                    cost_upper += w

            xor_k_mask(u0_b[i], u0_c[i])
            # xor_k_diff(u1_b[i], u1_c[i], diff_k[i])
            xor_k_mask(u1_b[i], u1_c[i])
            permute_bits_sr(u0_c[i], u0_d[i])
            permute_bits_sr(u1_c[i], u1_d[i])
            # permute_bits_sr(u2_c[i], u2_d[i])
            mix_t_columns(u0_d[i], u0_a[i + 1])
            # mix_columns(u1_d[i], u1_a[i + 1])
            mix_t_columns(u1_d[i], u1_a[i + 1])

        cost = cost_upper

        set_fixed_difference(u0_a[0], 0x0)
        set_fixed_difference(u1_a[0], 0x0)
        set_fixed_difference(u0_a[differential_characteristic_rounds_upper],
                             0x0)
        set_fixed_difference(u1_a[differential_characteristic_rounds_upper],
                             0x0)

        btor.Set_opt(pyboolector.BTOR_OPT_INCREMENTAL, 1)

        print("# route {} : differential : 0x{:016x} -> 0x{:016x}".format(route_number, diff_route[0],
                                                                          diff_route[len(diff_route) - 1]))

        differentials = []
        for target in range(min_weight, max_weight):
            # Find all solutions
            previous = []
            # previous_route = []
            # previous_trail = []
            print("# Solution: of weight {}".format(target), file=f)
            print("[", file=f)

            count_negative = 0
            count_positive = 0

            while True:
                btor.Assume(cost == target)
                distinct = btor.Const(1)
                for _, uuu0_a in previous:
                    temp = btor.Const(0)
                    for i in range(1, differential_characteristic_rounds_upper):
                        temp |= (u0_a[i] != btor.Const(uuu0_a[i], state_bits))
                        # temp |= (u1_a[i] != btor.Const(uuu1_a[i], state_bits))
                        # temp |= (u2_a[i] != btor.Const(uuu2_a[i], state_bits))
                    distinct &= temp
                btor.Assume(distinct)

                r = btor.Sat()
                if r == btor.SAT:
                    print("    # all: {}".format(int(cost.assignment, base=2)), file=f)
                    print("    # Solution: [#{} of weight {}]".format(len(previous) + 1, target), file=f)
                    print("    [", file=f)

                    # upper
                    route_u0 = []
                    route_u1 = []
                    # route_u2 = []
                    for i in range(differential_characteristic_rounds_upper):
                        uu0_a = int(u0_a[i].assignment, base=2)
                        uu1_a = int(u1_a[i].assignment, base=2)
                        # uu2_a = int(u2_a[i].assignment, base=2)
                        uu0_b = int(u0_b[i].assignment, base=2)
                        uu1_b = int(u1_b[i].assignment, base=2)
                        # uu2_b = int(u2_b[i].assignment, base=2)
                        uu0_c = int(u0_c[i].assignment, base=2)
                        uu1_c = int(u1_c[i].assignment, base=2)
                        # uu2_c = int(u2_c[i].assignment, base=2)
                        uu0_d = int(u0_d[i].assignment, base=2)
                        uu1_d = int(u1_d[i].assignment, base=2)
                        # uu2_d = int(u2_d[i].assignment, base=2)

                        if i < differential_characteristic_rounds_upper:
                            if i == 0:
                                print("     # upper: {}".format(int(cost_upper.assignment, base=2)), file=f)

                            print("     [0x{:016x}, 0x{:016x}, 0x{:016x}],".format(uu0_a, diff_route[4 * i], uu1_a),
                                  file=f)
                            print("     # after sb", file=f)
                            print("     [0x{:016x}, 0x{:016x}, 0x{:016x}],".format(uu0_b, diff_route[4 * i + 1], uu1_b),
                                  file=f)
                            print("     # after k", file=f)
                            print("     [0x{:016x}, 0x{:016x}, 0x{:016x}],".format(uu0_c, diff_route[4 * i + 2], uu1_c),
                                  file=f)
                            print("     # after sr", file=f)
                            print("     [0x{:016x}, 0x{:016x}, 0x{:016x}],".format(uu0_d, diff_route[4 * i + 3], uu1_d),
                                  file=f)
                            print("     # after mc", file=f)


                        route_u0.append(uu0_a)
                        route_u0.append(uu0_b)
                        route_u0.append(uu0_c)
                        route_u0.append(uu0_d)
                        route_u1.append(uu1_a)
                        route_u1.append(uu1_b)
                        route_u1.append(uu1_c)
                        route_u1.append(uu1_d)
                        # route_u2.append(u2_a)
                        # route_u2.append(u2_b)
                        # route_u2.append(u2_c)
                        # route_u2.append(u2_d)
                    u0_a_final = int(u0_a[
                                         differential_characteristic_rounds_upper].assignment,
                                     base=2)
                    u1_a_final = int(u1_a[
                                         differential_characteristic_rounds_upper].assignment,
                                     base=2)
                    # u2_a_final = int(u2_a[differential_characteristic_rounds_upper + differential_characteristic_rounds_lower].assignment, base=2)
                    print("", file=f)
                    print("     [0x{:016x}, 0x{:016x}, 0x{:016x}],".format(u0_a_final, diff_route[
                        4 * (differential_characteristic_rounds_upper)], u1_a_final),
                          file=f)
                    route_u0.append(u0_a_final)
                    route_u1.append(u1_a_final)
                    # route_u2.append(u2_a_final)

                    s_route = compute_sign(route_u0, route_u1, diff_route, differential_characteristic_rounds_upper)
                    if s_route < 0:
                        count_negative += 1
                        # print("    # sign = -1,", file=f)
                    else:
                        count_positive += 1
                        # print("    # sign = +1,", file=f)

                    print("     # sign = -1: {}".format(count_negative), file=f)
                    print("     # sign = +1: {}".format(count_positive), file=f)

                    print("    ],", file=f)
                    previous.append((s_route, [u0_a[i].assignment for i in range(differential_characteristic_rounds_upper + 1)]))
                else:
                    print("     # No trails with weight equal to {}.".format(target), file=f)
                    print("     # sign = -1: {}".format(count_negative), file=f)
                    print("     # sign = +1: {}".format(count_positive), file=f)
                    break
            print("],", file=f)

        return differentials

    filename = "result/dim_2_solutions_upper_{}_w_{}_to_{}_route_{}.txt".format(
        differential_characteristic_rounds_upper, min_weight, max_weight,
        route_number)
    f = open(filename, "w")
    print("# --------------------------------- route {} ---------------------------------------".format(route_number),
          file=f)
    print("routes = [".format(), file=f)
    # print("[".format(), file=f)
    differentials = search_differential(f)
    print("],", file=f)
    print("", file=f)
    f.close()
    return differentials

min_weight = 0
max_weight = 50

import routes_clustering as routes
rrr = routes.routes[0]
# pool_size = 0
print(len(rrr))
all_routes = []
for routes_w in rrr:
    if len(routes_w) > 0:
        print(len(routes_w))
        # pool_size += len(routes_w)
        for one_route in routes_w:
            all_routes.append(one_route)
print()
print(len(all_routes))

# pool_size = len(all_routes)
# all is 10
pool_size = 40

begin_i = 0
end_i = begin_i + pool_size
if end_i > len(all_routes):
    end_i = len(all_routes)

pool = Pool(end_i - begin_i)

for i in range(begin_i, end_i):
    diff_route = all_routes[i]
    pool.apply_async(get_quasidifferentials_by_one_fixed_input_and_output, (diff_route, i, min_weight, max_weight,))
pool.close()
pool.join()