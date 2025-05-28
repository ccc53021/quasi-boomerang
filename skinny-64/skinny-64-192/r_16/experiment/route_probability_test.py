
import random

import numpy

SKINNY_64_SBOX = [0xc, 0x6, 0x9, 0x0, 0x1, 0xa, 0x2, 0xb, 0x3, 0x8, 0x5, 0xd, 0x4, 0xe, 0x7, 0xf]

n = 4
m = 4
sbox = SKINNY_64_SBOX
state_bits = 64
state_words = 16
sbox_bits = 4

tk_number = 3

rc_6_bits = [
    0x01, 0x03, 0x07, 0x0F, 0x1F, 0x3E, 0x3D, 0x3B, 0x37, 0x2F, 0x1E, 0x3C, 0x39, 0x33, 0x27, 0x0E,
    0x1D, 0x3A, 0x35, 0x2B, 0x16, 0x2C, 0x18, 0x30, 0x21, 0x02, 0x05, 0x0B, 0x17, 0x2E, 0x1C, 0x38,
    0x31, 0x23, 0x06, 0x0D, 0x1B, 0x36, 0x2D, 0x1A, 0x34, 0x29, 0x12, 0x24, 0x08, 0x11, 0x22, 0x04]

import round_key_generating
tk1s_transition_64 = round_key_generating.tk1s_64
tk2s_transition_64 = round_key_generating.tk2s_64
tk3s_transition_64 = round_key_generating.tk3s_64

def get_inverse_box(sbox, n, m):
    inverse_sbox = [0] * (2 ** n)
    for i in range(2 ** n):
        inverse_sbox[sbox[i]] = i

    return inverse_sbox

lbox = []
for x in range(2 ** sbox_bits):
    x0 = x >> 3 & 0x1
    x1 = x >> 2 & 0x1
    x2 = x >> 1 & 0x1
    x3 = x >> 0 & 0x1
    y0 = x0 ^ x2 ^ x3
    y1 = x0
    y2 = x1 ^ x2
    y3 = x0 ^ x2
    lbox.append( (y0 << 3) ^ (y1 << 2) ^ (y2 << 1) ^ (y3) )


def get_sr_table_by_n(sbox_bits):
    tt = [0, 1, 2, 3, 7, 4, 5, 6, 10, 11, 8, 9, 13, 14, 15, 12]
    table = []
    for ii in tt:
        for i in range(ii * sbox_bits, (ii + 1) * sbox_bits):
            table.append(i)

    return table

def get_inverse_sr_table_by_n(sbox_bits):
    tt = [0, 1, 2, 3, 5, 6, 7, 4, 10, 11, 8, 9, 15, 12, 13, 14]
    table = []
    for ii in tt:
        for i in range(ii * sbox_bits, (ii + 1) * sbox_bits):
            table.append(i)

    return table

def get_pn_table_by_n(sbox_bits):
    tt = [9, 15, 8, 13, 10, 14, 12, 11, 0, 1, 2, 3, 4, 5, 6, 7]
    table = []
    for ii in tt:
        for i in range(ii * sbox_bits, (ii + 1) * sbox_bits):
            table.append(i)

    return table

def get_inverse_pn_table_by_n(sbox_bits):
    tt = [8, 9, 10, 11, 12, 13, 14, 15, 2, 0, 4, 7, 6, 3, 5, 1]
    table = []
    for ii in tt:
        for i in range(ii * sbox_bits, (ii + 1) * sbox_bits):
            table.append(i)

    return table

def permute_bits_by_table(x, table):
    y = [0] * state_bits
    for i in range(state_bits):
        y[i] = x[table[i]]

    return y

def sbox_layer_by_table(x, table):
    y = [0] * state_bits
    for i in range(0, state_bits, sbox_bits):
        sbox_input_str = ""
        for j in range(sbox_bits):
            sbox_input_str = str(x[i + j]) + sbox_input_str
        sbox_input = int(sbox_input_str, base=2)
        sbox_output = table[sbox_input]
        for j in range(sbox_bits):
            y[i + j] = (sbox_output >> j) & 0x1

    return y

def lbox_layer_by_table(x, table):
    y = [0] * state_bits
    for i in range(0, state_words):
        sbox_input_str = ""
        for j in range(sbox_bits):
            sbox_input_str = sbox_input_str + str(x[i + j * 4 * sbox_bits])
        sbox_input = int(sbox_input_str, base=2)
        sbox_output = table[sbox_input]
        for j in range(sbox_bits):
            y[i + j * 4 * sbox_bits] = (sbox_output >> (sbox_bits - 1 - j)) & 0x1

    return y

def xor_rc(x, rcs):
    y = x[::]
    c0 = rcs & 0xf
    c1 = (rcs >> 4) & 0x3
    c2 = 0x2
    for i in range(0, sbox_bits):
        y[i] ^= (c0 >> i) & 0x1
    for i in range(4 * sbox_bits, 5 * sbox_bits):
        y[i] ^= (c1 >> i) & 0x1
    for i in range(8 * sbox_bits, 9 * sbox_bits):
        y[i] ^= (c2 >> i) & 0x1

    return y

def xor_tk1(x, tk1):
    y = x[::]
    for i in range(state_bits // 2):
        y[i] ^= tk1[i]

    return y

def xor_tk1_and_tk2(x, tk1, tk2):
    y = x[::]
    for i in range(state_bits // 2):
        y[i] ^= tk1[i]
        y[i] ^= tk2[i]

    return y

def xor_tk1_and_tk2_and_tk3(x, tk1, tk2, tk3):
    y = x[::]
    for i in range(state_bits // 2):
        y[i] ^= tk1[i]
        y[i] ^= tk2[i]
        y[i] ^= tk3[i]

    return y

def get_initial_random_tk1_and_tk2_and_tk3():
    initial_tk1 = []
    initial_tk2 = []
    initial_tk3 = []
    for i in range(state_bits):
        initial_tk1.append(random.randint(0, 1))
        initial_tk2.append(random.randint(0, 1))
        initial_tk3.append(random.randint(0, 1))

    return initial_tk1, initial_tk2, initial_tk3

def get_initial_random_tk1_and_tk2_and_tk3_by_given_constraints(constraints, values):
    initial_tk1 = [0] * state_bits
    initial_tk2 = [0] * state_bits
    initial_tk3 = [0] * state_bits

    flag_t = 0
    while flag_t == 0:

        for i in range(state_bits):
            initial_tk1[i] = random.randint(0, 1)
            initial_tk2[i] = random.randint(0, 1)
            initial_tk3[i] = random.randint(0, 1)

        count_t = 0
        if tk_number == 1:
            for i in range(len(constraints)):
                one_constraint_tk1 = constraints[i][0]
                one_value = values[i]
                temp = 0
                for tkk1 in one_constraint_tk1:
                    temp ^= initial_tk1[tkk1]
                if temp == one_value:
                    count_t += 1
        elif tk_number == 2:
            for i in range(len(constraints)):
                one_constraint_tk1 = constraints[i][0]
                one_constraint_tk2 = constraints[i][1]
                one_value = values[i]

                temp = 0
                for tkk1 in one_constraint_tk1:
                    temp ^= initial_tk1[tkk1]
                for tkk2 in one_constraint_tk2:
                    temp ^= initial_tk2[tkk2]
                if temp == one_value:
                    count_t += 1
        elif tk_number == 3:
            for i in range(len(constraints)):
                one_constraint_tk1 = constraints[i][0]
                one_constraint_tk2 = constraints[i][1]
                one_constraint_tk3 = constraints[i][2]
                one_value = values[i]
                temp = 0
                for tkk1 in one_constraint_tk1:
                    temp ^= initial_tk1[tkk1]
                for tkk2 in one_constraint_tk2:
                    temp ^= initial_tk2[tkk2]
                for tkk3 in one_constraint_tk3:
                    temp ^= initial_tk3[tkk3]
                if temp == one_value:
                    count_t += 1

        if count_t == len(constraints):
            flag_t = 1

    return initial_tk1, initial_tk2, initial_tk3

def get_round_tks_by_initial_tk1(initial_tk1, round):
    round_tk1s = []

    for r in range(round):
        if tk_number == 1:
            bits_tk1 = tk1s_transition_64[r]
            rk1 = []
            for i in range(len(bits_tk1)):
                temp = 0
                one_i = bits_tk1[i]
                for kk1 in one_i:
                    temp ^= initial_tk1[kk1]
                rk1.append(temp)
            round_tk1s.append(rk1)

    return round_tk1s

def get_round_tks_by_initial_tk1_and_tk2(initial_tk1, initial_tk2, round):
    round_tk1s = []
    round_tk2s = []

    for r in range(round):
        if tk_number == 1:
            bits_tk1 = tk1s_transition_64[r]
            rk1 = []
            for i in range(len(bits_tk1)):
                temp = 0
                one_i = bits_tk1[i]
                for kk1 in one_i:
                    temp ^= initial_tk1[kk1]
                rk1.append(temp)
            round_tk1s.append(rk1)
        elif tk_number == 2:
            bits_tk1 = tk1s_transition_64[r]
            rk1 = []
            for i in range(len(bits_tk1)):
                temp = 0
                one_i = bits_tk1[i]
                for kk1 in one_i:
                    temp ^= initial_tk1[kk1]
                rk1.append(temp)
            round_tk1s.append(rk1)

            bits_tk2 = tk2s_transition_64[r]
            rk2 = []
            for i in range(len(bits_tk2)):
                temp = 0
                one_i = bits_tk2[i]
                for kk2 in one_i:
                    temp ^= initial_tk2[kk2]
                rk2.append(temp)
            round_tk2s.append(rk2)

    return round_tk1s, round_tk2s

def get_round_tks_by_initial_tk1_and_tk2_and_tk3(initial_tk1, initial_tk2, initial_tk3, round):
    round_tk1s = []
    round_tk2s = []
    round_tk3s = []

    for r in range(round):
        if tk_number == 1:
            bits_tk1 = tk1s_transition_64[r]
            rk1 = []
            for i in range(len(bits_tk1)):
                temp = 0
                one_i = bits_tk1[i]
                for kk1 in one_i:
                    temp ^= initial_tk1[kk1]
                rk1.append(temp)
            round_tk1s.append(rk1)
        elif tk_number == 2:
            bits_tk1 = tk1s_transition_64[r]
            rk1 = []
            for i in range(len(bits_tk1)):
                temp = 0
                one_i = bits_tk1[i]
                for kk1 in one_i:
                    temp ^= initial_tk1[kk1]
                rk1.append(temp)
            round_tk1s.append(rk1)

            bits_tk2 = tk2s_transition_64[r]
            rk2 = []
            for i in range(len(bits_tk2)):
                temp = 0
                one_i = bits_tk2[i]
                for kk2 in one_i:
                    temp ^= initial_tk2[kk2]
                rk2.append(temp)
            round_tk2s.append(rk2)
        elif tk_number == 3:
            bits_tk1 = tk1s_transition_64[r]
            rk1 = []
            for i in range(len(bits_tk1)):
                temp = 0
                one_i = bits_tk1[i]
                for kk1 in one_i:
                    temp ^= initial_tk1[kk1]
                rk1.append(temp)
            round_tk1s.append(rk1)

            bits_tk2 = tk2s_transition_64[r]
            rk2 = []
            for i in range(len(bits_tk2)):
                temp = 0
                one_i = bits_tk2[i]
                for kk2 in one_i:
                    temp ^= initial_tk2[kk2]
                rk2.append(temp)
            round_tk2s.append(rk2)

            bits_tk3 = tk3s_transition_64[r]
            rk3 = []
            for i in range(len(bits_tk3)):
                temp = 0
                one_i = bits_tk3[i]
                for kk3 in one_i:
                    temp ^= initial_tk3[kk3]
                rk3.append(temp)
            round_tk3s.append(rk3)

    return round_tk1s, round_tk2s, round_tk3s



def get_an_random_plaintext_and_another_by_difference(input_difference):
    x = [0] * state_bits
    x1 = [0] * state_bits
    for i in range(state_bits):
        x[i] = random.randint(0, 1)
        x1[i] = x[i] ^ input_difference[i]

    return x, x1

def get_another_key_by_k_and_difference(input_difference_1d, one_key_1d):
    k1 = [0] * state_bits
    for i in range(state_bits):
        k1[i] = one_key_1d[i] ^ input_difference_1d[i]

    return k1

def get_a_difference_1d(difference):
    difference_1d = [0] * state_bits
    for i in range(0, state_bits, sbox_bits):
        for j in range(sbox_bits):
            difference_1d[i + j] = (difference >> (i + j)) & 0x1

    return difference_1d

def get_a_difference_by_two_state(x, x1):
    diff = [0] * state_bits
    for i in range(state_bits):
        diff[i] = x[i] ^ x1[i]

    return diff
def one_experiment_amplified_em(input_difference, output_difference, number, experiment_time, sbox, sbox_inverse, lbox, lbox_inverse, sr_bits_table, sr_inverse_bits_table, round_tk1, round_tk2, round_tk3, begin_round, round_upper, round_lower):
    count_rp = 0
    count_eq = 0
    count_neq = 0
    for et in range(experiment_time):
        x, x1 = get_an_random_plaintext_and_another_by_difference(get_a_difference_1d(input_difference))

        y = x[::]
        y1 = x1[::]

        flag_rp = 1
        for i in range(round_upper + round_lower):

            # sb
            y = sbox_layer_by_table(y, sbox)
            y1 = sbox_layer_by_table(y1, sbox)

            # ac
            y = xor_rc(y, rc_6_bits[i + begin_round])
            y1 = xor_rc(y1, rc_6_bits[i + begin_round])

            # art
            if tk_number == 1:
                round_tk1_1 = round_tk1[0]
                round_tk1_2 = round_tk1[1]
                y = xor_tk1(y, round_tk1_1[i + begin_round])
                y1 = xor_tk1(y1, round_tk1_2[i + begin_round])
            elif tk_number == 2:
                round_tk1_1 = round_tk1[0]
                round_tk2_1 = round_tk2[0]
                round_tk1_2 = round_tk1[1]
                round_tk2_2 = round_tk2[1]
                y = xor_tk1_and_tk2(y, round_tk1_1[i + begin_round], round_tk2_1[i + begin_round])
                y1 = xor_tk1_and_tk2(y1, round_tk1_2[i + begin_round], round_tk2_2[i + begin_round])
            elif tk_number == 3:
                round_tk1_1 = round_tk1[0]
                round_tk2_1 = round_tk2[0]
                round_tk3_1 = round_tk3[0]
                round_tk1_2 = round_tk1[1]
                round_tk2_2 = round_tk2[1]
                round_tk3_2 = round_tk3[1]
                y = xor_tk1_and_tk2_and_tk3(y, round_tk1_1[i + begin_round], round_tk2_1[i + begin_round], round_tk3_1[i + begin_round])
                y1 = xor_tk1_and_tk2_and_tk3(y1, round_tk1_2[i + begin_round], round_tk2_2[i + begin_round], round_tk3_2[i + begin_round])

            # sr
            y = permute_bits_by_table(y, sr_bits_table)
            y1 = permute_bits_by_table(y1, sr_bits_table)

            # mc
            y = lbox_layer_by_table(y, lbox)
            y1 = lbox_layer_by_table(y1, lbox)

        y2 = y[::]
        y3 = y1[::]
        y2 = get_another_key_by_k_and_difference(get_a_difference_1d(output_difference), y2)
        y3 = get_another_key_by_k_and_difference(get_a_difference_1d(output_difference), y3)

        for i in range(round_upper + round_lower - 1, -1, -1):

            # mc inverse
            # y = lbox_layer_by_table(y, lbox_inverse)
            # y1 = lbox_layer_by_table(y1, lbox_inverse)
            y2 = lbox_layer_by_table(y2, lbox_inverse)
            y3 = lbox_layer_by_table(y3, lbox_inverse)

            # sr inverse
            # y = permute_bits_by_table(y, sr_inverse_bits_table)
            # y1 = permute_bits_by_table(y1, sr_inverse_bits_table)
            y2 = permute_bits_by_table(y2, sr_inverse_bits_table)
            y3 = permute_bits_by_table(y3, sr_inverse_bits_table)

            # art
            if tk_number == 1:
                # y = xor_tk1(y, round_tk1[i])
                # y1 = xor_tk1(y1, round_tk1[i])

                round_tk1_3 = round_tk1[2]
                round_tk1_4 = round_tk1[3]
                y2 = xor_tk1(y2, round_tk1_3[i + begin_round])
                y3 = xor_tk1(y3, round_tk1_4[i + begin_round])
            elif tk_number == 2:
                # y = xor_tk1_and_tk2(y, round_tk1[i], round_tk2[i])
                # y1 = xor_tk1_and_tk2(y1, round_tk1[i], round_tk2[i])

                round_tk1_3 = round_tk1[2]
                round_tk2_3 = round_tk2[2]
                round_tk1_4 = round_tk1[3]
                round_tk2_4 = round_tk2[3]
                y2 = xor_tk1_and_tk2(y2, round_tk1_3[i + begin_round], round_tk2_3[i + begin_round])
                y3 = xor_tk1_and_tk2(y3, round_tk1_4[i + begin_round], round_tk2_4[i + begin_round])
            elif tk_number == 3:
                # y = xor_tk1_and_tk2_and_tk3(y, round_tk1[i], round_tk2[i], round_tk3[i])
                # y1 = xor_tk1_and_tk2_and_tk3(y1, round_tk1[i], round_tk2[i], round_tk3[i])

                round_tk1_3 = round_tk1[2]
                round_tk2_3 = round_tk2[2]
                round_tk3_3 = round_tk3[2]
                round_tk1_4 = round_tk1[3]
                round_tk2_4 = round_tk2[3]
                round_tk3_4 = round_tk3[3]
                y2 = xor_tk1_and_tk2_and_tk3(y2, round_tk1_3[i + begin_round], round_tk2_3[i + begin_round], round_tk3_3[i + begin_round])
                y3 = xor_tk1_and_tk2_and_tk3(y3, round_tk1_4[i + begin_round], round_tk2_4[i + begin_round], round_tk3_4[i + begin_round])

            # ac
            # y = xor_rc(y, rc_6_bits[i])
            # y1 = xor_rc(y1, rc_6_bits[i])
            y2 = xor_rc(y2, rc_6_bits[i + begin_round])
            y3 = xor_rc(y3, rc_6_bits[i + begin_round])

            # sb inverse
            # y = sbox_layer_by_table(y, sbox_inverse)
            # y1 = sbox_layer_by_table(y1, sbox_inverse)
            y2 = sbox_layer_by_table(y2, sbox_inverse)
            y3 = sbox_layer_by_table(y3, sbox_inverse)

        diff_y = get_a_difference_by_two_state(y2, y3)
        diff_r = get_a_difference_1d(input_difference)
        if diff_y != diff_r:
            count_neq += 1
            flag_rp = 0
        else:
            count_eq += 1
            flag_rp = 1


        count_rp += flag_rp

    print()
    print("em: ")
    print(count_eq, count_neq, count_neq + count_eq)
    print("time {}, right pairs : {}, p = {} = 2^-{}".format(experiment_time, count_rp, count_rp / experiment_time, -numpy.log2(count_rp / experiment_time)))

sbox_inverse = get_inverse_box(sbox, n, m)
lbox_inverse = get_inverse_box(lbox, n, m)
sr_bits_table = get_sr_table_by_n(sbox_bits)
sr_inverse_bits_table = get_inverse_sr_table_by_n(sbox_bits)
pn_bits_table = get_pn_table_by_n(sbox_bits)

print("------------- begining ----------------")

encrypt_round = 16
number = 4

em_begin_round = 0
em_round_upper = 8
em_round_lower = 8
em_input_difference = 0x0000000000000800
em_output_difference = 0x000000b000000000

tk_constraints = []
tk_values = []

print("---------- generating initial tk ----------------")
tk1_1, tk2_1, tk3_1 = get_initial_random_tk1_and_tk2_and_tk3_by_given_constraints(tk_constraints, tk_values)
print("tk1_1 = {}".format(tk1_1))
print("tk2_1 = {}".format(tk2_1))
print("tk3_1 = {}".format(tk3_1))

print("-------------- generating tks -------------------")
difference_tk1_delta_1 = 0x0000000000000700
difference_tk1_delta_2 = 0x0004000000000000
difference_tk2_delta_1 = 0x0000000000000600
difference_tk2_delta_2 = 0x000a000000000000
difference_tk3_delta_1 = 0x0000000000000500
difference_tk3_delta_2 = 0x0006000000000000
tk1_2 = get_another_key_by_k_and_difference(get_a_difference_1d(difference_tk1_delta_1), tk1_1)
tk1_3 = get_another_key_by_k_and_difference(get_a_difference_1d(difference_tk1_delta_2), tk1_1)
tk1_4 = get_another_key_by_k_and_difference(get_a_difference_by_two_state(get_a_difference_1d(difference_tk1_delta_1), get_a_difference_1d(difference_tk1_delta_2)), tk1_1)
tk2_2 = get_another_key_by_k_and_difference(get_a_difference_1d(difference_tk2_delta_1), tk2_1)
tk2_3 = get_another_key_by_k_and_difference(get_a_difference_1d(difference_tk2_delta_2), tk2_1)
tk2_4 = get_another_key_by_k_and_difference(get_a_difference_by_two_state(get_a_difference_1d(difference_tk2_delta_1), get_a_difference_1d(difference_tk2_delta_2)), tk2_1)
tk3_2 = get_another_key_by_k_and_difference(get_a_difference_1d(difference_tk3_delta_1), tk3_1)
tk3_3 = get_another_key_by_k_and_difference(get_a_difference_1d(difference_tk3_delta_2), tk3_1)
tk3_4 = get_another_key_by_k_and_difference(get_a_difference_by_two_state(get_a_difference_1d(difference_tk3_delta_1), get_a_difference_1d(difference_tk3_delta_2)), tk3_1)
print("tk1_2 = {}".format(tk1_2))
print("tk2_2 = {}".format(tk2_2))
print("tk3_2 = {}".format(tk3_2))
print("tk1_3 = {}".format(tk1_3))
print("tk2_3 = {}".format(tk2_3))
print("tk3_3 = {}".format(tk3_3))
print("tk1_4 = {}".format(tk1_4))
print("tk2_4 = {}".format(tk2_4))
print("tk3_4 = {}".format(tk3_4))


print("----------------- generating rks ---------------------")
round_tk1_1, round_tk2_1, round_tk3_1 = get_round_tks_by_initial_tk1_and_tk2_and_tk3(tk1_1, tk2_1, tk3_1, encrypt_round)
round_tk1_2, round_tk2_2, round_tk3_2 = get_round_tks_by_initial_tk1_and_tk2_and_tk3(tk1_2, tk2_2, tk3_2, encrypt_round)
round_tk1_3, round_tk2_3, round_tk3_3 = get_round_tks_by_initial_tk1_and_tk2_and_tk3(tk1_3, tk2_3, tk3_3, encrypt_round)
round_tk1_4, round_tk2_4, round_tk3_4 = get_round_tks_by_initial_tk1_and_tk2_and_tk3(tk1_4, tk2_4, tk3_4, encrypt_round)

round_tk1 = [round_tk1_1, round_tk1_2, round_tk1_3, round_tk1_4]
round_tk2 = [round_tk2_1, round_tk2_2, round_tk2_3, round_tk2_4]
round_tk3 = [round_tk3_1, round_tk3_2, round_tk3_3, round_tk3_4]

print("------------------------ experiment ------------------")
# p = 1
em_experiment_time = 2 ** 10
one_experiment_amplified_em(em_input_difference, em_output_difference, number, em_experiment_time, sbox, sbox_inverse, lbox, lbox_inverse, sr_bits_table, sr_inverse_bits_table, round_tk1, round_tk2, round_tk3, em_begin_round, em_round_upper, em_round_lower)