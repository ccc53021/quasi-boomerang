
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

def key_conditions_by_one_trail(iii, diff_and_trail, begin_round, round_upper, round_lower):
    one_trail_key_bit = state_bits
    one_key_expression_tk1 = [0] * one_trail_key_bit * 3
    one_key_expression_tk2 = [0] * one_trail_key_bit * 3
    one_key_expression_tk3 = [0] * one_trail_key_bit * 3
    correlation = 1
    for round in range(round_upper + round_lower):
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

            if round < round_upper:
                c = tables.get_ddt_upper_item_by_given_all(sbox, n, m, uu0, vv0, uu1, vv1, uu2, vv2)
                correlation *= c
            elif round == round_upper:
                c = tables.get_bct_item_by_given_all(sbox, n, m, uu0, vv0, uu1, vv1, uu2, vv2)
                correlation *= c
            else:
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

            if round < round_upper:
                aa_upper = (v2 >> i * sbox_bits) & (2 ** sbox_bits - 1)
                for j in range(sbox_bits):
                    bb_upper = (aa_upper >> j) & 0x1
                    if bb_upper == 1:
                        if tk_number == 1:
                            pp_tk1_list = tk1s_64[round + begin_round][i * sbox_bits + j]
                            for pp in pp_tk1_list:
                                one_key_expression_tk1[pp + 1 * one_trail_key_bit] ^= 1
                        elif tk_number == 2:
                            pp_tk1_list = tk1s_64[round + begin_round][i * sbox_bits + j]
                            for pp in pp_tk1_list:
                                one_key_expression_tk1[pp + 1 * one_trail_key_bit] ^= 1
                            pp_tk2_list = tk2s_64[round + begin_round][i * sbox_bits + j]
                            for pp in pp_tk2_list:
                                one_key_expression_tk2[pp + 1 * one_trail_key_bit] ^= 1
                        elif tk_number == 3:
                            pp_tk1_list = tk1s_64[round + begin_round][i * sbox_bits + j]
                            for pp in pp_tk1_list:
                                one_key_expression_tk1[pp + 1 * one_trail_key_bit] ^= 1
                            pp_tk2_list = tk2s_64[round + begin_round][i * sbox_bits + j]
                            for pp in pp_tk2_list:
                                one_key_expression_tk2[pp + 1 * one_trail_key_bit] ^= 1
                            pp_tk3_list = tk3s_64[round + begin_round][i * sbox_bits + j]
                            for pp in pp_tk3_list:
                                one_key_expression_tk3[pp + 1 * one_trail_key_bit] ^= 1
            else:
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

import quasi_bcs_all as diffs_and_quasis
quasi_bcs = diffs_and_quasis.routes
print(len(quasi_bcs))
print(len(quasi_bcs[0]))

route_numbers = len(quasi_bcs)
max_w = len(quasi_bcs[0])

begin_round = 0
round_upper = 6
round_lower = 6
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
                one_key_expression, one_key_expression1, key_str = key_conditions_by_one_trail(i + 1, one_quasi_bc, begin_round, round_upper, round_lower)
                print("l {} : {}".format(i + 1, key_str))
                key_list.append(one_key_expression)
                key_list1.append(one_key_expression1)
                key_list1_with_w[ww].append(one_key_expression1)
print()
print("all {} trails".format(len(key_list)))

import gaussian_elimination
rank, rank1, key_rref_str, key_space = gaussian_elimination.get_rank_and_base_master_key(key_list, key_list1, state_bits, tk_number)


