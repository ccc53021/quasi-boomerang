
import numpy, pyboolector
import generate_tables as tables
from multiprocessing import Pool

GIFT_SBOX = [0x1, 0xa, 0x4, 0xc, 0x6, 0xf, 0x3, 0x9, 0x2, 0xd, 0xb, 0x7, 0x5, 0x0, 0x8, 0xe]
n = 4
m = 4
sbox = GIFT_SBOX
state_bits = 64
state_words = 16
sbox_bits = 4

dim_n = 1

differential_characteristic_rounds_upper = 9

permutation_bits_table_64 = [
    0, 5, 10, 15, 16, 21, 26, 31, 32, 37, 42, 47, 48, 53, 58, 63,
    12, 1, 6, 11, 28, 17, 22, 27, 44, 33, 38, 43, 60, 49, 54, 59,
    8, 13, 2, 7, 24, 29, 18, 23, 40, 45, 34, 39, 56, 61, 50, 55,
    4, 9, 14, 3, 20, 25, 30, 19, 36, 41, 46, 35, 52, 57, 62, 51
]

round_constants = [0x01, 0x03, 0x07, 0x0F, 0x1F, 0x3E, 0x3D, 0x3B, 0x37, 0x2F, 0x1E, 0x3C, 0x39, 0x33, 0x27, 0x0E, 0x1D, 0x3A, 0x35, 0x2B, 0x16, 0x2C, 0x18, 0x30, 0x21, 0x02, 0x05, 0x0B, 0x17, 0x2E, 0x1C, 0x38]
round_constant_positions = [3, 7, 11, 15, 19, 23]

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

def compute_sign(route_u1, route_mask, route_diff, round_upper):
    correlation_sign = 0

    # upper
    for r in range(round_upper):
        u0 = route_mask[3 * r]
        delta_in_1 = route_diff[3 * r]
        u1 = route_u1[3 * r]
        v0 = route_mask[3 * r + 1]
        delta_out_1 = route_diff[3 * r + 1]
        v1 = route_u1[3 * r + 1]

        for i in range(0, state_words):
            uu0 = (u0 >> (4 * i)) & (2 ** sbox_bits - 1)
            di1 = (delta_in_1 >> (4 * i)) & (2 ** sbox_bits - 1)
            uu1 = (u1 >> (4 * i)) & (2 ** sbox_bits - 1)
            vv0 = (v0 >> (4 * i)) & (2 ** sbox_bits - 1)
            do1 = (delta_out_1 >> (4 * i)) & (2 ** sbox_bits - 1)
            vv1 = (v1 >> (4 * i)) & (2 ** sbox_bits - 1)

            c = tables.get_ddt_upper_item_by_given_all(sbox, n, m, uu0, vv0, di1, do1, uu1, vv1)
            if c < 0:
                correlation_sign += 1


    # add constants
    for r in range(round_upper):
        rcs = round_constants[r]
        mask_c = (1 << (state_bits - 1)) | (((rcs >> 5) & 0x1) << round_constant_positions[5]) | (
                ((rcs >> 4) & 0x1) << round_constant_positions[4]) | (
                         ((rcs >> 3) & 0x1) << round_constant_positions[3]) | (
                         ((rcs >> 2) & 0x1) << round_constant_positions[2]) | (
                         ((rcs >> 1) & 0x1) << round_constant_positions[1]) | (
                         ((rcs >> 0) & 0x1) << round_constant_positions[0])
        v0 = route_mask[3 * r + 1]
        correlation_sign += bin(mask_c & v0).count('1')

    return (-1) ** correlation_sign

# quasidifferential one_solution_search
def get_quasidifferentials_by_u0_v0(route_mask, route_diff, route_number, min_weight, max_weight):
    def search_differential(f):

        btor = pyboolector.Boolector()
        btor.Set_opt(pyboolector.BTOR_OPT_MODEL_GEN, 1)

        # difference
        # input
        # u0_a = [btor.Var(btor.BitVecSort(state_bits), "u0_a%d" % i) for i in range(differential_characteristic_rounds_upper + differential_characteristic_rounds_lower + 1)]
        u1_a = [btor.Var(btor.BitVecSort(state_bits), "u1_a%d" % i) for i in
                range(differential_characteristic_rounds_upper + 1)]
        # after sb
        # u0_b = [btor.Var(btor.BitVecSort(state_bits), "u0_b%d" % i) for i in range(differential_characteristic_rounds_upper + differential_characteristic_rounds_lower)]
        u1_b = [btor.Var(btor.BitVecSort(state_bits), "u1_b%d" % i) for i in
                range(differential_characteristic_rounds_upper)]
        # after p
        # u0_c = [btor.Var(btor.BitVecSort(state_bits), "u0_c%d" % i) for i in range(differential_characteristic_rounds_upper + differential_characteristic_rounds_lower)]
        u1_c = [btor.Var(btor.BitVecSort(state_bits), "u1_c%d" % i) for i in
                range(differential_characteristic_rounds_upper)]

        def xor_k_diff(x, y, k):
            rk0 = k & 0xffff
            rk1 = (k >> 16) & 0xffff
            for i in range(state_words):
                btor.Assert(y[4 * i] == x[4 * i] ^ ((rk0 >> i) & 0x1))
                btor.Assert(y[4 * i + 1] == x[4 * i + 1] ^ ((rk1 >> i) & 0x1))
                btor.Assert(y[4 * i + 2] == x[4 * i + 2])
                btor.Assert(y[4 * i + 3] == x[4 * i + 3])

        def xor_k_mask(x, y):
            for i in range(state_bits):
                btor.Assert(y[i] == x[i])

        def permute_bits(x, y):
            for i in range(state_bits):
                btor.Assert(y[i] == x[permutation_bits_table_64[i]])

        def get_one_words_weight_by_small_quasi_table(u, v, small_table_weight_lists_w_0_to_7):
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
                        v0 = one_group[1]
                        if tw == 0:
                            weight0 |= (u == u0) & (v == v0)
                        elif tw == 1:
                            weight1 |= (u == u0) & (v == v0)
                        elif tw == 2:
                            weight2 |= (u == u0) & (v == v0)
                        elif tw == 3:
                            weight3 |= (u == u0) & (v == v0)
                        elif tw == 4:
                            weight4 |= (u == u0) & (v == v0)
                        elif tw == 5:
                            weight5 |= (u == u0) & (v == v0)
                        elif tw == 6:
                            weight6 |= (u == u0) & (v == v0)
                        elif tw == 7:
                            weight7 |= (u == u0) & (v == v0)

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

        cost_upper = btor.Const(0, state_words)

        count_ddt_upper = []
        table_ddt_upper = []

        count_bct = []
        table_bct = []

        count_ddt_lower = []
        table_ddt_lower = []

        # the upper
        for i in range(differential_characteristic_rounds_upper):
            for j in range(0, state_bits, sbox_bits):
                uu0 = (route_mask[3 * i] >> j) & (2 ** sbox_bits - 1)
                delta_in_1 = (route_diff[3 * i] >> j) & (2 ** sbox_bits - 1)
                uu1 = u1_a[i][j + sbox_bits - 1:j]
                vv0 = (route_mask[3 * i + 1] >> j) & (2 ** sbox_bits - 1)
                delta_out_1 = (route_diff[3 * i + 1] >> j) & (2 ** sbox_bits - 1)
                vv1 = u1_b[i][j + sbox_bits - 1:j]

                deltas = [uu0, delta_in_1, vv0, delta_out_1]
                if deltas not in count_ddt_upper:
                    print("upper biddt : (0x{:01x}, 0x{:01x}) -> (0x{:01x}, 0x{:01x})".format(uu0, delta_in_1, vv0,
                                                                                              delta_out_1))
                    count_ddt_upper.append(deltas)
                    small_quasi_ddt = tables.get_ddt_upper_matrices_2n_by_u0_v0_and_given_delta_1_and_lambda_1(sbox, n,
                                                                                                               m, uu0,
                                                                                                               vv0,
                                                                                                               delta_in_1,
                                                                                                               delta_out_1)
                    small_quasi_ddt_weight_lists_w_0_to_7 = get_tables_weight_lists_w_0_to_7(small_quasi_ddt, dim_n, 1)
                    w = get_one_words_weight_by_small_quasi_table(uu1, vv1, small_quasi_ddt_weight_lists_w_0_to_7)
                    cost_upper += w
                    table_ddt_upper.append(small_quasi_ddt_weight_lists_w_0_to_7)
                elif deltas in count_ddt_upper:
                    position = count_ddt_upper.index(deltas)
                    small_quasi_ddt_weight_lists_w_0_to_7 = table_ddt_upper[position]
                    w = get_one_words_weight_by_small_quasi_table(uu1, vv1, small_quasi_ddt_weight_lists_w_0_to_7)
                    cost_upper += w
            permute_bits(u1_b[i], u1_c[i])
            xor_k_mask(u1_c[i], u1_a[i + 1])


        cost = cost_upper

        set_fixed_difference(u1_a[0], 0x0)
        set_fixed_difference(u1_a[differential_characteristic_rounds_upper],
                             0x0)
        btor.Set_opt(pyboolector.BTOR_OPT_INCREMENTAL, 1)

        print("# route {} : differential : 0x{:016x} -> 0x{:016x}".format(route_number, route_diff[0],
                                                                          route_diff[len(route_diff) - 1]))

        differentials = []
        for target in range(min_weight, max_weight):
            previous = []
            print("# Solution: of weight {}".format(target), file=f)
            print("[", file=f)

            count_negative = 0
            count_positive = 0

            while True:
                btor.Assume(cost == target)
                distinct = btor.Const(1)
                for _, uuu1_a in previous:
                    temp = btor.Const(0)
                    for i in range(1,
                                   differential_characteristic_rounds_upper):
                        # temp |= (u0_a[i] != btor.Const(uuu0_a[i], state_bits))
                        temp |= (u1_a[i] != btor.Const(uuu1_a[i], state_bits))
                        # temp |= (u2_a[i] != btor.Const(uuu2_a[i], state_bits))
                    distinct &= temp
                btor.Assume(distinct)

                r = btor.Sat()
                if r == btor.SAT:
                    print("    # all: {}".format(int(cost.assignment, base=2)), file=f)
                    print("    # Solution: [#{} of weight {}]".format(len(previous) + 1, target), file=f)
                    print("    [", file=f)

                    # upper
                    # route_u0 = []
                    route_u1 = []
                    # route_u2 = []
                    for i in range(differential_characteristic_rounds_upper):
                        # uu0_a = int(u0_a[i].assignment, base=2)
                        uu1_a = int(u1_a[i].assignment, base=2)
                        # uu2_a = int(u2_a[i].assignment, base=2)
                        # uu0_b = int(u0_b[i].assignment, base=2)
                        uu1_b = int(u1_b[i].assignment, base=2)
                        # uu2_b = int(u2_b[i].assignment, base=2)
                        # uu0_c = int(u0_c[i].assignment, base=2)
                        uu1_c = int(u1_c[i].assignment, base=2)
                        # uu2_c = int(u2_c[i].assignment, base=2)

                        if i == 0:
                            print("     # upper: {}".format(int(cost_upper.assignment, base=2)), file=f)

                        print("     [0x{:016x}, 0x{:016x}, 0x{:016x}],".format(route_mask[3 * i], route_diff[3 * i],
                                                                               uu1_a), file=f)
                        print("     # after sb", file=f)
                        print("     [0x{:016x}, 0x{:016x}, 0x{:016x}],".format(route_mask[3 * i + 1],
                                                                               route_diff[3 * i + 1], uu1_b),
                              file=f)
                        print("     # after p", file=f)
                        print("     [0x{:016x}, 0x{:016x}, 0x{:016x}],".format(route_mask[3 * i + 2],
                                                                               route_diff[3 * i + 2], uu1_c),
                              file=f)
                        print("     # after k", file=f)

                        route_u1.append(uu1_a)
                        route_u1.append(uu1_b)
                        route_u1.append(uu1_c)
                    # u0_a_final = int(u0_a[differential_characteristic_rounds_upper + differential_characteristic_rounds_lower].assignment, base=2)
                    u1_a_final = int(u1_a[
                                         differential_characteristic_rounds_upper].assignment,
                                     base=2)
                    # u2_a_final = int(u2_a[differential_characteristic_rounds_upper + differential_characteristic_rounds_lower].assignment, base=2)
                    print("", file=f)
                    print("     [0x{:016x}, 0x{:016x}, 0x{:016x}],".format(route_mask[3 * (
                                differential_characteristic_rounds_upper)], route_diff[3 * (
                                    differential_characteristic_rounds_upper)], u1_a_final),
                          file=f)
                    # route_u0.append(u0_a_final)
                    route_u1.append(u1_a_final)
                    # route_u2.append(u2_a_final)

                    s_route = compute_sign(route_u1, route_mask, route_diff, differential_characteristic_rounds_upper)
                    if s_route < 0:
                        count_negative += 1
                        # print("    # sign = -1,", file=f)
                    else:
                        count_positive += 1
                        # print("    # sign = +1,", file=f)

                    print("     # sign = -1: {}".format(count_negative), file=f)
                    print("     # sign = +1: {}".format(count_positive), file=f)

                    print("    ],", file=f)
                    previous.append((s_route, [u1_a[i].assignment for i in range(
                        differential_characteristic_rounds_upper + 1)]))
                else:
                    print("     # No trails with weight equal to {}.".format(target), file=f)
                    print("     # sign = -1: {}".format(count_negative), file=f)
                    print("     # sign = +1: {}".format(count_positive), file=f)
                    break
            print("],", file=f)

        return differentials

    filename = "result/quasibc_search_upper_{}_w_{}_to_{}_route_{}.txt".format(differential_characteristic_rounds_upper, min_weight, max_weight, route_number)
    f = open(filename, "w")
    print("# --------------------------------- route {} ---------------------------------------".format(route_number),
          file=f)
    print("routes = [".format(), file=f)
    differentials = search_differential(f)
    print("],", file=f)
    print("", file=f)
    f.close()
    return differentials


min_weight = 0
max_weight = 50

import routes_clustering as routes
rrr = routes.routes[0]
print(len(rrr))
all_routes = []
for routes_w in rrr:
    if len(routes_w) > 0:
        print(len(routes_w))
        for one_route in routes_w:
            all_routes.append(one_route)
print()
print(len(all_routes))

# pool_size = len(all_routes)
# all is 1
pool_size = 40

begin_i = 0
end_i = begin_i + pool_size
if end_i > len(all_routes):
    end_i = len(all_routes)

pool = Pool(end_i - begin_i)

for i in range(begin_i, end_i):
    route_diff = all_routes[i]
    route_mask = []
    for j in range(len(route_diff)):
        route_mask.append(0x0)
    pool.apply_async(get_quasidifferentials_by_u0_v0, (route_mask, route_diff, i, min_weight, max_weight,))
pool.close()
pool.join()