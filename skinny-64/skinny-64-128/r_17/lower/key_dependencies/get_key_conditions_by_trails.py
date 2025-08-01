
import numpy
# from sage.all import *
import round_key_generating
import generate_tables as tables

tk1s_64 = round_key_generating.tk1s_64
tk2s_64 = round_key_generating.tk2s_64
tk3s_64 = round_key_generating.tk3s_64

tk_number = 2

SKINNY_64_SBOX = [0xc, 0x6, 0x9, 0x0, 0x1, 0xa, 0x2, 0xb, 0x3, 0x8, 0x5, 0xd, 0x4, 0xe, 0x7, 0xf]
# SKINNY_64_INVERSE_SBOX = [0x3, 4, 6, 8, 12, 10, 1, 14, 9, 2, 5, 7, 0, 11, 13, 15]
n = 4
m = 4
sbox = SKINNY_64_SBOX
# sbox_inverse = SKINNY_64_INVERSE_SBOX
state_bits = 64
state_words = 16
sbox_bits = 4

rc_6_bits = [
    0x01, 0x03, 0x07, 0x0F, 0x1F, 0x3E, 0x3D, 0x3B, 0x37, 0x2F, 0x1E, 0x3C, 0x39, 0x33, 0x27, 0x0E,
    0x1D, 0x3A, 0x35, 0x2B, 0x16, 0x2C, 0x18, 0x30, 0x21, 0x02, 0x05, 0x0B, 0x17, 0x2E, 0x1C, 0x38,
    0x31, 0x23, 0x06, 0x0D, 0x1B, 0x36, 0x2D, 0x1A, 0x34, 0x29, 0x12, 0x24, 0x08, 0x11, 0x22, 0x04]

def get_DDT(sbox, n, m):
    DDT = numpy.zeros((2 ** n, 2 ** m))

    for input_d in range(2 ** n):
        for output_d in range(2 ** m):
            for x in range(2 ** n):
                y = x ^ input_d
                sx = sbox[x]
                sy = sbox[y]
                if (sx ^ sy) == output_d:
                    DDT[input_d, output_d] += 1

    return DDT


def get_1d_by_hex(x):
    y = [0] * state_bits
    for i in range(state_bits):
        y[i] = (x >> i) & 0x1

    return y

def vector_inner_product(u, x, n):
    left = 0
    for i in range(n):
        left += ((u >> i) & 0x1) * ((x >> i) & 0x1)
    left = left % 2

    return left

def key_conditions_by_one_trail(iii, diff_and_trail, begin_round, round_lower):
    one_trail_key_bit = state_bits
    one_key_expression_tk1 = [0] * one_trail_key_bit * 3
    one_key_expression_tk2 = [0] * one_trail_key_bit * 3
    one_key_expression_tk3 = [0] * one_trail_key_bit * 3
    correlation = 1
    for round in range(round_lower):
        # sb
        u0 = diff_and_trail[4 * round][0]
        u1 = diff_and_trail[4 * round][1]
        u2 = diff_and_trail[4 * round][2]
        v0 = diff_and_trail[4 * round + 1][0]
        v1 = diff_and_trail[4 * round + 1][1]
        v2 = diff_and_trail[4 * round + 1][2]

        for i in range(0, state_words):
            uu0 = (u0 >> (sbox_bits * i)) & (2 ** sbox_bits - 1)
            uu1 = (u1 >> (sbox_bits * i)) & (2 ** sbox_bits - 1)
            uu2 = (u2 >> (sbox_bits * i)) & (2 ** sbox_bits - 1)
            vv0 = (v0 >> (sbox_bits * i)) & (2 ** sbox_bits - 1)
            vv1 = (v1 >> (sbox_bits * i)) & (2 ** sbox_bits - 1)
            vv2 = (v2 >> (sbox_bits * i)) & (2 ** sbox_bits - 1)

            c = tables.get_ddt_lower_item_by_given_all(sbox, n, m, uu0, vv0, uu1, vv1, uu2, vv2)
            correlation *= c

        rcs = rc_6_bits[round + begin_round]
        c0 = rcs & 0xf
        c1 = (rcs >> 4) & 0x3
        c2 = 0x2
        mask_c = (c2 << (8 * sbox_bits)) | (c1 << (4 * sbox_bits)) | c0
        correlation *= ((-1) ** bin(mask_c & v0).count('1'))

        for i in range(8):
            aa_x = (v0 >> i * sbox_bits) & (2 ** sbox_bits - 1)
            for j in range(sbox_bits):
                bb_x = (aa_x >> j) & 0x1
                if bb_x == 1:
                    if tk_number == 1:
                        pp_tk1_list = tk1s_64[round + begin_round][i * sbox_bits + j]
                        for pp in pp_tk1_list:
                            one_key_expression_tk1[pp] ^= 1
                    elif tk_number == 2:
                        pp_tk1_list = tk1s_64[round + begin_round][i * sbox_bits + j]
                        for pp in pp_tk1_list:
                            one_key_expression_tk1[pp] ^= 1
                        pp_tk2_list = tk2s_64[round + begin_round][i * sbox_bits + j]
                        for pp in pp_tk2_list:
                            one_key_expression_tk2[pp] ^= 1
                    elif tk_number == 3:
                        pp_tk1_list = tk1s_64[round + begin_round][i * sbox_bits + j]
                        for pp in pp_tk1_list:
                            one_key_expression_tk1[pp] ^= 1
                        pp_tk2_list = tk2s_64[round + begin_round][i * sbox_bits + j]
                        for pp in pp_tk2_list:
                            one_key_expression_tk2[pp] ^= 1
                        pp_tk3_list = tk3s_64[round + begin_round][i * sbox_bits + j]
                        for pp in pp_tk3_list:
                            one_key_expression_tk3[pp] ^= 1

            aa_lower = (v1 >> i * sbox_bits) & (2 ** sbox_bits - 1)
            for j in range(sbox_bits):
                bb_lower = (aa_lower >> j) & 0x1
                if bb_lower == 1:
                    if tk_number == 1:
                        pp_tk1_list = tk1s_64[round + begin_round][i * sbox_bits + j]
                        for pp in pp_tk1_list:
                            one_key_expression_tk1[pp + 2 * one_trail_key_bit] ^= 1
                    elif tk_number == 2:
                        pp_tk1_list = tk1s_64[round + begin_round][i * sbox_bits + j]
                        for pp in pp_tk1_list:
                            one_key_expression_tk1[pp + 2 * one_trail_key_bit] ^= 1
                        pp_tk2_list = tk2s_64[round + begin_round][i * sbox_bits + j]
                        for pp in pp_tk2_list:
                            one_key_expression_tk2[pp + 2 * one_trail_key_bit] ^= 1
                    elif tk_number == 3:
                        pp_tk1_list = tk1s_64[round + begin_round][i * sbox_bits + j]
                        for pp in pp_tk1_list:
                            one_key_expression_tk1[pp + 2 * one_trail_key_bit] ^= 1
                        pp_tk2_list = tk2s_64[round + begin_round][i * sbox_bits + j]
                        for pp in pp_tk2_list:
                            one_key_expression_tk2[pp + 2 * one_trail_key_bit] ^= 1
                        pp_tk3_list = tk3s_64[round + begin_round][i * sbox_bits + j]
                        for pp in pp_tk3_list:
                            one_key_expression_tk3[pp + 2 * one_trail_key_bit] ^= 1



    key_str = ""
    one_key_expression = []
    if tk_number == 1:
        for i in range(one_trail_key_bit):
            if one_key_expression_tk1[i] == 1:
                key_str += "tk1_{} + ".format(i)
        for i in range(one_trail_key_bit, 2 * one_trail_key_bit):
            if one_key_expression_tk1[i] == 1:
                key_str += "delta_upper_tk1_{} + ".format(i - one_trail_key_bit)
        for i in range(2 * one_trail_key_bit, 3 * one_trail_key_bit):
            if one_key_expression_tk1[i] == 1:
                key_str += "delta_lower_tk1_{} + ".format(i - one_trail_key_bit * 2)
        one_key_expression = one_key_expression_tk1
    elif tk_number == 2:
        for i in range(one_trail_key_bit):
            if one_key_expression_tk1[i] == 1:
                key_str += "tk1_{} + ".format(i)
        for i in range(one_trail_key_bit, 2 * one_trail_key_bit):
            if one_key_expression_tk1[i] == 1:
                key_str += "delta_upper_tk1_{} + ".format(i - one_trail_key_bit)
        for i in range(2 * one_trail_key_bit, 3 * one_trail_key_bit):
            if one_key_expression_tk1[i] == 1:
                key_str += "delta_lower_tk1_{} + ".format(i - one_trail_key_bit * 2)
        for i in range(one_trail_key_bit):
            if one_key_expression_tk2[i] == 1:
                key_str += "tk2_{} + ".format(i)
        for i in range(one_trail_key_bit, 2 * one_trail_key_bit):
            if one_key_expression_tk2[i] == 1:
                key_str += "delta_upper_tk2_{} + ".format(i - one_trail_key_bit)
        for i in range(2 * one_trail_key_bit, 3 * one_trail_key_bit):
            if one_key_expression_tk2[i] == 1:
                key_str += "delta_lower_tk2_{} + ".format(i - one_trail_key_bit * 2)
        one_key_expression = one_key_expression_tk1 + one_key_expression_tk2
    elif tk_number == 3:
        for i in range(one_trail_key_bit):
            if one_key_expression_tk1[i] == 1:
                key_str += "tk1_{} + ".format(i)
        for i in range(one_trail_key_bit, 2 * one_trail_key_bit):
            if one_key_expression_tk1[i] == 1:
                key_str += "delta_upper_tk1_{} + ".format(i - one_trail_key_bit)
        for i in range(2 * one_trail_key_bit, 3 * one_trail_key_bit):
            if one_key_expression_tk1[i] == 1:
                key_str += "delta_lower_tk1_{} + ".format(i - one_trail_key_bit * 2)
        for i in range(one_trail_key_bit):
            if one_key_expression_tk2[i] == 1:
                key_str += "tk2_{} + ".format(i)
        for i in range(one_trail_key_bit, 2 * one_trail_key_bit):
            if one_key_expression_tk2[i] == 1:
                key_str += "delta_upper_tk2_{} + ".format(i - one_trail_key_bit)
        for i in range(2 * one_trail_key_bit, 3 * one_trail_key_bit):
            if one_key_expression_tk2[i] == 1:
                key_str += "delta_lower_tk2_{} + ".format(i - one_trail_key_bit * 2)
        for i in range(one_trail_key_bit):
            if one_key_expression_tk3[i] == 1:
                key_str += "tk3_{} + ".format(i)
        for i in range(one_trail_key_bit, 2 * one_trail_key_bit):
            if one_key_expression_tk3[i] == 1:
                key_str += "delta_upper_tk3_{} + ".format(i - one_trail_key_bit)
        for i in range(2 * one_trail_key_bit, 3 * one_trail_key_bit):
            if one_key_expression_tk3[i] == 1:
                key_str += "delta_lower_tk3_{} + ".format(i - one_trail_key_bit * 2)
        one_key_expression = one_key_expression_tk1 + one_key_expression_tk2 + one_key_expression_tk3
    one_key_expression1 = one_key_expression[::]
    if correlation < 0:
        one_key_expression1.append(1)
        key_str += " = 1"
    else:
        one_key_expression1.append(0)
        key_str += " = 0"

    return one_key_expression, one_key_expression1, key_str


def solve_linear_system(target, candidates):
    U_set = set(target)
    for cand in candidates:
        U_set.update(cand)
    U = sorted(U_set)
    num_rows = len(U)
    num_candidates = len(candidates)

    event_to_idx = {event: idx for idx, event in enumerate(U)}

    matrix = [[0] * (num_candidates + 1) for _ in range(num_rows)]

    for j, cand in enumerate(candidates):
        for event in cand:
            idx = event_to_idx.get(event)
            if idx is not None:
                matrix[idx][j] = 1

    for event in target:
        idx = event_to_idx.get(event)
        if idx is not None:
            matrix[idx][num_candidates] = 1

    pivot_cols = [-1] * num_rows
    pivot_row_for_col = [-1] * num_candidates
    pivot_row = 0

    for col in range(num_candidates):
        pivot = -1
        for r in range(pivot_row, num_rows):
            if matrix[r][col] == 1:
                pivot = r
                break
        if pivot == -1:
            continue

        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        pivot_cols[pivot_row] = col
        pivot_row_for_col[col] = pivot_row

        for r in range(pivot_row + 1, num_rows):
            if matrix[r][col] == 1:
                for c in range(col, num_candidates + 1):
                    matrix[r][c] ^= matrix[pivot_row][c]

        pivot_row += 1

    for r in range(pivot_row, num_rows):
        if matrix[r][num_candidates] == 1:
            return None

    for r in range(pivot_row - 1, -1, -1):
        col = pivot_cols[r]
        if col == -1:
            continue
        for r2 in range(r):
            if matrix[r2][col] == 1:
                for c in range(col, num_candidates + 1):
                    matrix[r2][c] ^= matrix[r][c]

    solution = [0] * num_candidates
    for col in range(num_candidates):
        if pivot_row_for_col[col] != -1:
            r = pivot_row_for_col[col]
            solution[col] = matrix[r][num_candidates]

    return solution

def count_valid_by_given_basis(key_list1, basis, basis_values):
    key_0 = [0] * (tk_number * state_bits * 3 + 1)
    key_1 = [0] * (tk_number * state_bits * 3 + 1)
    key_1[tk_number * state_bits * 3] = 1
    count_mask_0_sign_0 = 0
    count_mask_0_sign_1 = 0
    count_mask_1_sign_0 = 0
    count_mask_1_sign_1 = 0
    trails_mask_0_sign_0 = []
    trails_mask_0_sign_1 = []
    trails_mask_1_sign_0 = []
    trails_mask_1_sign_1 = []
    for i in range(len(key_list1)):
        one_key = key_list1[i]
        if one_key == key_0:
            count_mask_0_sign_0 += 1
            trails_mask_0_sign_0.append(i + 1)
        elif one_key == key_1:
            count_mask_0_sign_1 += 1
            trails_mask_0_sign_1.append(i + 1)
        else:
            sign = 0
            one_key_list = []
            # for j in range(tk_number * state_bits * 3):
            #     if one_key[j] == 1:
            #         one_key_list.append(j)
            # for j in range(len(basis)):
            #     one_basis = basis[j]
            #     one_value = basis_values[j]
            #     if tk_number == 1:
            #         flag_y = 1
            #         pp_tk1_list = one_basis[0]
            #         one_basis_tk1_x = pp_tk1_list[0]
            #         one_basis_tk1_upper = pp_tk1_list[1]
            #         one_basis_tk1_lower = pp_tk1_list[2]
            #         for one_key_pp in one_basis_tk1_x:
            #             if one_key_pp not in one_key_list:
            #                 flag_y = 0
            #                 break
            #         for one_key_pp in one_basis_tk1_upper:
            #             if one_key_pp + state_bits not in one_key_list:
            #                 flag_y = 0
            #                 break
            #         for one_key_pp in one_basis_tk1_lower:
            #             if one_key_pp + state_bits * 2 not in one_key_list:
            #                 flag_y = 0
            #                 break
            #         if flag_y == 1:
            #             sign ^= one_value
            #     elif tk_number == 2:
            #         flag_y = 1
            #         pp_tk1_list = one_basis[0]
            #         one_basis_tk1_x = pp_tk1_list[0]
            #         one_basis_tk1_upper = pp_tk1_list[1]
            #         one_basis_tk1_lower = pp_tk1_list[2]
            #         for one_key_pp in one_basis_tk1_x:
            #             if one_key_pp not in one_key_list:
            #                 flag_y = 0
            #                 break
            #         for one_key_pp in one_basis_tk1_upper:
            #             if one_key_pp + state_bits not in one_key_list:
            #                 flag_y = 0
            #                 break
            #         for one_key_pp in one_basis_tk1_lower:
            #             if one_key_pp + state_bits * 2 not in one_key_list:
            #                 flag_y = 0
            #                 break
            #
            #         pp_tk2_list = one_basis[1]
            #         one_basis_tk2_x = pp_tk2_list[0]
            #         one_basis_tk2_upper = pp_tk2_list[1]
            #         one_basis_tk2_lower = pp_tk2_list[2]
            #         for one_key_pp in one_basis_tk2_x:
            #             if one_key_pp + state_bits * 3 not in one_key_list:
            #                 flag_y = 0
            #                 break
            #         for one_key_pp in one_basis_tk2_upper:
            #             if one_key_pp + state_bits * 4 not in one_key_list:
            #                 flag_y = 0
            #                 break
            #         for one_key_pp in one_basis_tk2_lower:
            #             if one_key_pp + state_bits * 5 not in one_key_list:
            #                 flag_y = 0
            #                 break
            #         if flag_y == 1:
            #             sign ^= one_value
            #     elif tk_number == 3:
            #         flag_y = 1
            #         pp_tk1_list = one_basis[0]
            #         one_basis_tk1_x = pp_tk1_list[0]
            #         one_basis_tk1_upper = pp_tk1_list[1]
            #         one_basis_tk1_lower = pp_tk1_list[2]
            #         for one_key_pp in one_basis_tk1_x:
            #             if one_key_pp not in one_key_list:
            #                 flag_y = 0
            #                 break
            #         for one_key_pp in one_basis_tk1_upper:
            #             if one_key_pp + state_bits not in one_key_list:
            #                 flag_y = 0
            #                 break
            #         for one_key_pp in one_basis_tk1_lower:
            #             if one_key_pp + state_bits * 2 not in one_key_list:
            #                 flag_y = 0
            #                 break
            #
            #         pp_tk2_list = one_basis[1]
            #         one_basis_tk2_x = pp_tk2_list[0]
            #         one_basis_tk2_upper = pp_tk2_list[1]
            #         one_basis_tk2_lower = pp_tk2_list[2]
            #         for one_key_pp in one_basis_tk2_x:
            #             if one_key_pp + state_bits * 3 not in one_key_list:
            #                 flag_y = 0
            #                 break
            #         for one_key_pp in one_basis_tk2_upper:
            #             if one_key_pp + state_bits * 4 not in one_key_list:
            #                 flag_y = 0
            #                 break
            #         for one_key_pp in one_basis_tk2_lower:
            #             if one_key_pp + state_bits * 5 not in one_key_list:
            #                 flag_y = 0
            #                 break
            #
            #         pp_tk3_list = one_basis[2]
            #         one_basis_tk3_x = pp_tk3_list[0]
            #         one_basis_tk3_upper = pp_tk3_list[1]
            #         one_basis_tk3_lower = pp_tk3_list[2]
            #         for one_key_pp in one_basis_tk3_x:
            #             if one_key_pp + state_bits * 6 not in one_key_list:
            #                 flag_y = 0
            #                 break
            #         for one_key_pp in one_basis_tk3_upper:
            #             if one_key_pp + state_bits * 7 not in one_key_list:
            #                 flag_y = 0
            #                 break
            #         for one_key_pp in one_basis_tk3_lower:
            #             if one_key_pp + state_bits * 8 not in one_key_list:
            #                 flag_y = 0
            #                 break
            #
            #         if flag_y == 1:
            #             sign ^= one_value

            # one_key_list.append([[], [], []])
            # one_key_list.append([[], [], []])
            # one_key_list.append([[], [], []])
            # for j in range(tk_number * state_bits * 3):
            #     if one_key[j] == 1:
            #         # one_key_list.append(j)
            #         tkn = j // (3 * state_bits)
            #         xdn = (j - tkn * 3 * state_bits) // state_bits
            #         nnn = (j - tkn * 3 * state_bits) % state_bits
            #         one_key_list[tkn][xdn].append(nnn)
            # print(one_key_list)

            for j in range(tk_number * state_bits * 3):
                if one_key[j] == 1:
                    one_key_list.append(j)
            solution = solve_linear_system(one_key_list, basis)
            if solution is None:
                print("error")
            else:
                selected_indices = [i for i, x in enumerate(solution) if x == 1]
                for iii in selected_indices:
                    sign ^= basis_values[iii]

            sign ^= one_key[tk_number * state_bits * 3]
            if sign == 0:
                count_mask_1_sign_0 += 1
                trails_mask_1_sign_0.append(i + 1)
            else:
                count_mask_1_sign_1 += 1
                trails_mask_1_sign_1.append(i + 1)

    print("no key , +1 : {}".format(count_mask_0_sign_0))
    print(trails_mask_0_sign_0)
    print("no key , -1 : {}".format(count_mask_0_sign_1))
    print(trails_mask_0_sign_1)
    print("xor key, +1 : {}".format(count_mask_1_sign_0))
    print(trails_mask_1_sign_0)
    print("xor key, -1 : {}".format(count_mask_1_sign_1))
    print(trails_mask_1_sign_1)
    all = count_mask_0_sign_0 + count_mask_1_sign_0 - count_mask_0_sign_1 - count_mask_1_sign_1
    print("all is {}".format(all))

    return all

import quasi_bcs_all as diffs_and_quasis
quasi_bcs = diffs_and_quasis.routes
print(len(quasi_bcs))
print(len(quasi_bcs[0]))

route_numbers = len(quasi_bcs)
max_w = len(quasi_bcs[0])

begin_round = 7 + 1 + 1
round_lower = 8
# round_lower = 4
key_list = []
key_list1 = []
key_list1_with_w = [[] for i in range(max_w)]
count_w_and_numbers = [0] * max_w
for rn in range(route_numbers):
    one_route_quasi_bcs = quasi_bcs[rn]
    for ww in range(max_w):
        dts_w = one_route_quasi_bcs[ww]
        if len(dts_w) > 0:
            print()
            print("---------------------------------------------------------------")
            print("route {}, w {} : {} quasi-bcs".format(rn, ww, len(dts_w)))
            count_w_and_numbers[ww] += len(dts_w)
            for i in range(len(dts_w)):
                one_quasi_bc = dts_w[i]
                one_key_expression, one_key_expression1, key_str = key_conditions_by_one_trail(i + 1, one_quasi_bc, begin_round, round_lower)
                print("l {} : {}".format(i + 1, key_str))
                key_list.append(one_key_expression)
                key_list1.append(one_key_expression1)
                key_list1_with_w[ww].append(one_key_expression1)
print()
print("all {} trails".format(len(key_list)))

# import gaussian_elimination
# rank, rank1, key_rref_str, key_space = gaussian_elimination.get_rank_and_base_master_key(key_list, key_list1, state_bits, tk_number)

count_non_zero = []
condition_bits = 4
count_w_and_numbers_in_fixed_key = [0] * max_w
for i in range(2 ** 2):
    c0 = (i >> 0) & 0x1
    c1 = (i >> 1) & 0x1
    # c2 = (i >> 2) & 0x1
    # c3 = (i >> 3) & 0x1

    c2 = 0
    c3 = 0
    basis = [
    #     [[[16], [], []], [[17, 19], [], []]],
    #     [[[18], [], []], [[16, 17], [], []]],
    #     [[[], [], [16]], [[], [], [17, 19]]], # = 0
    #     [[[], [], [18]], [[], [], [16, 17]]], # = 0
    #
    #     [[[16, 18], [], []], [[16, 19], [], []]],
    #     [[[], [], [16, 18]], [[], [], [16, 19]]],

        [16, 209, 211],
        [18, 208, 209],
        [144, 337, 339],  # = 0
        [146, 336, 337],  # = 0

        [16, 18, 208, 211],
        [144, 146, 336, 337],
    ]
    basis_values = [c0, c1, c2, c3, c0 ^ c1, c2 ^ c3]
    print()
    print("the {}-th basis : {}".format(i, basis))
    count_p_all = 0
    for ww in range(max_w):
        if len(key_list1_with_w[ww]) > 0:
            count_w_and_numbers_in_fixed_key[ww] = count_valid_by_given_basis(key_list1_with_w[ww], basis, basis_values)
            # print("w = {} : {} quasi-bcs, {} quasi-bcs in fixed-key, p = 2^-{} * {}".format(ww, count_w_and_numbers[ww], count_w_and_numbers_in_fixed_key[ww], ww / 2, count_w_and_numbers_in_fixed_key[ww]))
            print("w = {} : {} quasi-bcs, {} quasi-bcs in fixed-key, p = 2^-{} * {}".format(ww, count_w_and_numbers[ww], count_w_and_numbers_in_fixed_key[ww], ww, count_w_and_numbers_in_fixed_key[ww]))
            # count_p_all += count_w_and_numbers_in_fixed_key[ww] * (2 ** (-(ww / 2)))
            count_p_all += count_w_and_numbers_in_fixed_key[ww] * (2 ** (-(ww)))
    print("p = {} = 2^-{}".format(count_p_all, -numpy.log2(count_p_all)))
    # all = count_valid_by_given_basis(key_list1, basis, basis_values)
    # if all != 0:
    #     count_non_zero.append([i, all])
print()
print("--------------------------------")
# print(count_non_zero)

