
import numpy
# from sage.all import *
import round_key_transition
import generate_tables as tables

rks = round_key_transition.key_recover_bit_from_top_to_bottom_64

GIFT_SBOX = [0x1, 0xa, 0x4, 0xc, 0x6, 0xf, 0x3, 0x9, 0x2, 0xd, 0xb, 0x7, 0x5, 0x0, 0x8, 0xe]
n = 4
m = 4
sbox = GIFT_SBOX
state_bits = 64
state_words = 16
sbox_bits = 4
key_bits = 128

round_constants = [0x01, 0x03, 0x07, 0x0F, 0x1F, 0x3E, 0x3D, 0x3B, 0x37, 0x2F, 0x1E, 0x3C, 0x39, 0x33, 0x27, 0x0E, 0x1D, 0x3A, 0x35, 0x2B, 0x16, 0x2C, 0x18, 0x30, 0x21, 0x02, 0x05, 0x0B, 0x17, 0x2E, 0x1C, 0x38]
round_constant_positions = [3, 7, 11, 15, 19, 23]

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

def get_master_key_by_round_key(round, round_position, key_recovery_round_top):
    true_round = round + 1 + key_recovery_round_top

    if state_bits == 128:
        if round_position % 2 == 0:
            true_position = round_position // 2
            master_key = round_key_transition.key_recover_bit_from_top_to_bottom_128[true_round][true_position]
            return master_key
        elif round_position % 2 == 1:
            true_position = (round_position - 1) // 2
            master_key = round_key_transition.key_recover_bit_from_top_to_bottom_128[true_round][true_position]
            return master_key
    elif state_bits == 64:
        if round_position % 2 == 0:
            true_position = round_position // 2
            master_key = round_key_transition.key_recover_bit_from_top_to_bottom_64[true_round][true_position]
            return master_key
        elif round_position % 2 == 1:
            true_position = ((round_position - 1) // 2) + 1
            master_key = round_key_transition.key_recover_bit_from_top_to_bottom_64[true_round][true_position]
            return master_key

def key_conditions_by_one_trail(iii, diff_and_trail, begin_round, round_lower):
    one_trail_key_bit = key_bits
    one_key_expression = [0] * one_trail_key_bit * 3
    correlation = 1
    for round in range(round_lower):
        # sb

        u0 = diff_and_trail[3 * round][0]
        u1 = diff_and_trail[3 * round][1]
        u2 = diff_and_trail[3 * round][2]
        v0 = diff_and_trail[3 * round + 1][0]
        v1 = diff_and_trail[3 * round + 1][1]
        v2 = diff_and_trail[3 * round + 1][2]

        for i in range(0, state_words):
            uu0 = (u0 >> (sbox_bits * i)) & (2 ** sbox_bits - 1)
            uu1 = (u1 >> (sbox_bits * i)) & (2 ** sbox_bits - 1)
            uu2 = (u2 >> (sbox_bits * i)) & (2 ** sbox_bits - 1)
            vv0 = (v0 >> (sbox_bits * i)) & (2 ** sbox_bits - 1)
            vv1 = (v1 >> (sbox_bits * i)) & (2 ** sbox_bits - 1)
            vv2 = (v2 >> (sbox_bits * i)) & (2 ** sbox_bits - 1)

            c = tables.get_ddt_lower_item_by_given_all(sbox, n, m, uu0, vv0, uu1, vv1, uu2, vv2)
            correlation *= c

        rcs = round_constants[round + begin_round]
        mask_c = (1 << (state_bits - 1)) | (((rcs >> 5) & 0x1) << round_constant_positions[5]) | (
                ((rcs >> 4) & 0x1) << round_constant_positions[4]) | (
                         ((rcs >> 3) & 0x1) << round_constant_positions[3]) | (
                         ((rcs >> 2) & 0x1) << round_constant_positions[2]) | (
                         ((rcs >> 1) & 0x1) << round_constant_positions[1]) | (
                         ((rcs >> 0) & 0x1) << round_constant_positions[0])
        correlation *= ((-1) ** bin(mask_c & v0).count('1'))

        k0 = diff_and_trail[3 * round + 2][0]
        k1 = diff_and_trail[3 * round + 2][1]
        k2 = diff_and_trail[3 * round + 2][2]
        for i in range(state_words):
            aa_x = (k0 >> i * sbox_bits) & (2 ** sbox_bits - 1)
            for j in range(sbox_bits):
                if state_bits == 64:
                    if j != 2 and j != 3:
                        bb_x = (aa_x >> j) & 0x1
                        if bb_x == 1:
                            round_key_full = round * state_bits + (sbox_bits * i + j)
                            round_key_round = round_key_full // state_bits
                            round_key_position = round_key_full % state_bits
                            master_key = get_master_key_by_round_key(round_key_round, round_key_position,
                                                                     begin_round)
                            master_key_word = master_key[0]
                            master_key_position = master_key[1]
                            master_key_full = master_key_word * 16 + master_key_position
                            one_key_expression[master_key_full] ^= 1

            aa_lower = (k1 >> i * sbox_bits) & (2 ** sbox_bits - 1)
            for j in range(sbox_bits):
                if state_bits == 64:
                    if j != 2 and j != 3:
                        bb_lower = (aa_lower >> j) & 0x1
                        if bb_lower == 1:
                            round_key_full = round * state_bits + (sbox_bits * i + j)
                            round_key_round = round_key_full // state_bits
                            round_key_position = round_key_full % state_bits
                            master_key = get_master_key_by_round_key(round_key_round, round_key_position,
                                                                     begin_round)
                            master_key_word = master_key[0]
                            master_key_position = master_key[1]
                            master_key_full = master_key_word * 16 + master_key_position
                            one_key_expression[master_key_full + 2 * one_trail_key_bit] ^= 1

    key_str = ""
    for i in range(one_trail_key_bit):
        if one_key_expression[i] == 1:
            word = i // 16
            position = i % 16
            key_str += "k{}_{} +".format(word, position)
    for i in range(one_trail_key_bit, 2 * one_trail_key_bit):
        if one_key_expression[i] == 1:
            word = (i - one_trail_key_bit) // 16
            position = (i - one_trail_key_bit) % 16
            key_str += "delta_upper_k_{}_{} + ".format(word, position)
    for i in range(2 * one_trail_key_bit, 3 * one_trail_key_bit):
        if one_key_expression[i] == 1:
            word = (i - one_trail_key_bit * 2) // 16
            position = (i - one_trail_key_bit * 2) % 16
            key_str += "delta_lower_k_{}_{} + ".format(word, position)

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

begin_round = 9 + 1 + 1
round_lower = 8
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

import gaussian_elimination
rank, rank1, key_rref_str, key_space = gaussian_elimination.get_rank_and_base_master_key(key_list, key_list1, key_bits)


