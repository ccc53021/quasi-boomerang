
import numpy, pyboolector
import generate_tables as tables

GIFT_SBOX = [0x1, 0xa, 0x4, 0xc, 0x6, 0xf, 0x3, 0x9, 0x2, 0xd, 0xb, 0x7, 0x5, 0x0, 0x8, 0xe]
n = 4
m = 4
sbox = GIFT_SBOX
state_bits = 64
state_words = 16
sbox_bits = 4

differential_characteristic_rounds_upper = 9

permutation_bits_table_64 = [
    0, 5, 10, 15, 16, 21, 26, 31, 32, 37, 42, 47, 48, 53, 58, 63,
    12, 1, 6, 11, 28, 17, 22, 27, 44, 33, 38, 43, 60, 49, 54, 59,
    8, 13, 2, 7, 24, 29, 18, 23, 40, 45, 34, 39, 56, 61, 50, 55,
    4, 9, 14, 3, 20, 25, 30, 19, 36, 41, 46, 35, 52, 57, 62, 51
]

def get_tables_weight_lists_w_0_to_7(table):
    weight_list_w_0_to_7 = []
    for w in range(0, 8):
        weight_list_w_0_to_7.append([])

    for a in range(2 ** n):
        for b in range(2 ** m):
            input = b
            output = a
            c = table[input, output]
            if c != 0:
                w = int(abs(numpy.log2(abs(c))))
                # print("c != 0 : c = {}, w = {}, int w = {}".format(c, w, int(w)))
                weight_list_w_0_to_7[w].append([a, b])

    print("---------------------------------")

    return weight_list_w_0_to_7

# quasidifferential one_solution_search
def get_routes_by_one_fixed_input_and_output(min_weight, max_weight, input_difference, output_difference, diff_k):

    def search_differential(f):

        btor = pyboolector.Boolector()
        btor.Set_opt(pyboolector.BTOR_OPT_MODEL_GEN, 1)

        # difference
        # input
        d0_a = [btor.Var(btor.BitVecSort(state_bits), "d0_a%d" % i) for i in range(differential_characteristic_rounds_upper + 1)]
        # after sb
        d0_b = [btor.Var(btor.BitVecSort(state_bits), "d0_b%d" % i) for i in range(differential_characteristic_rounds_upper)]
        # after_p
        d0_c = [btor.Var(btor.BitVecSort(state_bits), "d0_c%d" % i) for i in range(differential_characteristic_rounds_upper)]

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

        def get_one_words_weight_by_table(a, b, small_table_weight_lists_w_0_to_7):
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
                        a0 = one_group[0]
                        b0 = one_group[1]
                        if tw == 0:
                            weight0 |= (a == a0) & (b == b0)
                        elif tw == 1:
                            weight1 |= (a == a0) & (b == b0)
                        elif tw == 2:
                            weight2 |= (a == a0) & (b == b0)
                        elif tw == 3:
                            weight3 |= (a == a0) & (b == b0)
                        elif tw == 4:
                            weight4 |= (a == a0) & (b == b0)
                        elif tw == 5:
                            weight5 |= (a == a0) & (b == b0)
                        elif tw == 6:
                            weight6 |= (a == a0) & (b == b0)
                        elif tw == 7:
                            weight7 |= (a == a0) & (b == b0)


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
        # cost_lower = btor.Const(0, state_words)
        # cost_em = btor.Const(0, state_words)

        ddt = tables.get_ddt(sbox, n, m)
        ddt_weight = get_tables_weight_lists_w_0_to_7(ddt)

        bct = tables.get_bct(sbox, n, m)
        bct_weight = get_tables_weight_lists_w_0_to_7(bct)

        # upper
        for i in range(differential_characteristic_rounds_upper):
            for j in range(0, state_bits, sbox_bits):
                aa0 = d0_a[i][j + sbox_bits - 1:j]
                bb0 = d0_b[i][j + sbox_bits - 1:j]

                w = get_one_words_weight_by_table(aa0, bb0, ddt_weight)
                cost_upper += w
                cost_upper += w
            permute_bits(d0_b[i], d0_c[i])
            xor_k_diff(d0_c[i], d0_a[i + 1], diff_k[i])

        cost = cost_upper

        set_fixed_difference(d0_a[0], input_difference)
        set_fixed_difference(d0_a[differential_characteristic_rounds_upper], output_difference)
        btor.Set_opt(pyboolector.BTOR_OPT_INCREMENTAL, 1)


        print("# differential : 0x{:016x} -> 0x{:016x}".format(input_difference, output_difference))

        differentials = []
        count_n = 0
        count_p = 0
        count_p_str = []
        for target in range(min_weight, max_weight):
            previous = []
            print("# Solution: of weight {}".format(target), file=f)
            print("[", file=f)

            # count_negative = 0
            # count_positive = 0

            while True:
                btor.Assume(cost == target)
                distinct = btor.Const(1)
                for aa in previous:
                    temp = btor.Const(0)
                    for i in range(1, differential_characteristic_rounds_upper):
                        temp |= (d0_a[i] != btor.Const(aa[i], state_bits))
                    distinct &= temp
                btor.Assume(distinct)

                r = btor.Sat()
                if r == btor.SAT:
                    print("    # all: {}".format(int(cost.assignment, base=2)), file=f)
                    print("    # Solution: [#{} of weight {}]".format(len(previous) + 1, target), file=f)
                    print("    [", file=f)

                    for i in range(differential_characteristic_rounds_upper):
                        dd0_a = int(d0_a[i].assignment, base=2)
                        dd0_b = int(d0_b[i].assignment, base=2)
                        dd0_c = int(d0_c[i].assignment, base=2)

                        if i == 0:
                            print("     # upper: {}".format(int(cost_upper.assignment, base=2)), file=f)

                        print("     0x{:016x},".format(dd0_a), file=f)
                        print("     # after sb", file=f)
                        print("     0x{:016x},".format(dd0_b), file=f)
                        print("     # after p", file=f)
                        print("     0x{:016x},".format(dd0_c), file=f)
                        print("     # after k", file=f)

                    d0_a_final = int(d0_a[differential_characteristic_rounds_upper].assignment, base=2)
                    print("", file=f)
                    print("     0x{:016x},".format(d0_a_final), file=f)

                    print("    ],", file=f)
                    previous.append(([d0_a[i].assignment for i in range(differential_characteristic_rounds_upper + 1)]))
                else:
                    print("     # No trails with weight equal to {}.".format(target), file=f)
                    print("     # all is {}".format(len(previous)), file=f)
                    break
            print("],", file=f)
            if len(previous) > 0:
                pp = 2 ** (-target) * len(previous)
                # print("p = 2^-{}: {} bcs -> pp = {}".format(target, len(previous), pp))
                count_p_str.append("# p = 2^-{}: {} bcs -> pp = {}".format(target, len(previous), pp))
                count_p += pp
                count_n += len(previous)

        print("")
        for one_p_str in count_p_str:
            print(one_p_str)
        print("# all {} bcs, all p is {}".format(count_n, count_p))

        return differentials

    filename = "result/upper_bc_search_upper_{}_w_{}_to_{}.txt".format(differential_characteristic_rounds_upper, min_weight, max_weight)
    f = open(filename, "w")
    print("routes = [".format(), file=f)
    differentials = search_differential(f)
    print("],", file=f)
    print("", file=f)
    f.close()
    return differentials


min_weight = 0
max_weight = 50

upper_input_difference = 0x000000a000006000
lower_output_difference = 0x0100000001020200

diff_route_k = [
    0x01004000,
    0x00000000,
    0x00000002,
    0x00000000,
    0x00400004,
    0x00000000,
    0x00000020,
    0x00000000,
    0x00100040
]

differentials = get_routes_by_one_fixed_input_and_output(min_weight, max_weight, upper_input_difference, lower_output_difference, diff_route_k)
