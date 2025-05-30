
from sage.all import *

# 高斯消元 sage版
from sympy import Matrix
def get_rank_and_base_master_key(key_list, key_list1, state_bits, tk):
    km = MatrixSpace(GF(2), len(key_list), tk * state_bits * 3)
    km1 = MatrixSpace(GF(2), len(key_list1), tk * state_bits * 3 + 1)

    key_matrix = km.matrix(Matrix(key_list))
    key_matrix1 = km1.matrix(Matrix(key_list1))

    rank = key_matrix.rank()
    rank1 = key_matrix1.rank()
    print("# rank = {}, rank1 = {}".format(rank, rank1))

    # key_matrix_rref = key_matrix1.echelon_form()
    key_matrix_rref = key_matrix1.rref()
    key_matrix_rref_list = list(key_matrix_rref)
    key_rref_str = []
    key_space = []
    one_trail_key_bit = tk * state_bits
    for r in range(rank1):
        one_trail_rref_str = ''
        one_key_linear_contraint = []
        if tk == 1:
            for i in range(state_bits):
                if key_matrix_rref_list[r][i] != 0:
                    one_trail_rref_str += "tk1_{} + ".format(i)
                    one_key_linear_contraint.append(i)
            for i in range(state_bits, 2 * state_bits):
                if key_matrix_rref_list[r][i] != 0:
                    one_trail_rref_str += "delta_upper_tk1_{} + ".format(i - state_bits)
                    one_key_linear_contraint.append(i)
            for i in range(2 * state_bits, 3 * state_bits):
                if key_matrix_rref_list[r][i] != 0:
                    one_trail_rref_str += "delta_lower_tk1_{} + ".format(i - state_bits * 2)
                    one_key_linear_contraint.append(i)
        elif tk == 2:
            for i in range(state_bits):
                if key_matrix_rref_list[r][i] != 0:
                    one_trail_rref_str += "tk1_{} + ".format(i)
                    one_key_linear_contraint.append(i)
            for i in range(state_bits, 2 * state_bits):
                if key_matrix_rref_list[r][i] != 0:
                    one_trail_rref_str += "delta_upper_tk1_{} + ".format(i - state_bits)
                    one_key_linear_contraint.append(i)
            for i in range(2 * state_bits, 3 * state_bits):
                if key_matrix_rref_list[r][i] != 0:
                    one_trail_rref_str += "delta_lower_tk1_{} + ".format(i - state_bits * 2)
                    one_key_linear_contraint.append(i)
            for i in range(3 * state_bits, 4 * state_bits):
                if key_matrix_rref_list[r][i] != 0:
                    one_trail_rref_str += "tk2_{} + ".format(i - state_bits * 3)
                    one_key_linear_contraint.append(i)
            for i in range(4 * state_bits, 5 * state_bits):
                if key_matrix_rref_list[r][i] != 0:
                    one_trail_rref_str += "delta_upper_tk2_{} + ".format(i - state_bits * 4)
                    one_key_linear_contraint.append(i)
            for i in range(5 * state_bits, 6 * state_bits):
                if key_matrix_rref_list[r][i] != 0:
                    one_trail_rref_str += "delta_lower_tk2_{} + ".format(i - state_bits * 5)
                    one_key_linear_contraint.append(i)
        elif tk == 3:
            for i in range(state_bits):
                if key_matrix_rref_list[r][i] != 0:
                    one_trail_rref_str += "tk1_{} + ".format(i)
                    one_key_linear_contraint.append(i)
            for i in range(state_bits, 2 * state_bits):
                if key_matrix_rref_list[r][i] != 0:
                    one_trail_rref_str += "delta_upper_tk1_{} + ".format(i - state_bits)
                    one_key_linear_contraint.append(i)
            for i in range(2 * state_bits, 3 * state_bits):
                if key_matrix_rref_list[r][i] != 0:
                    one_trail_rref_str += "delta_lower_tk1_{} + ".format(i - state_bits * 2)
                    one_key_linear_contraint.append(i)
            for i in range(3 * state_bits, 4 * state_bits):
                if key_matrix_rref_list[r][i] != 0:
                    one_trail_rref_str += "tk2_{} + ".format(i - state_bits * 3)
                    one_key_linear_contraint.append(i)
            for i in range(4 * state_bits, 5 * state_bits):
                if key_matrix_rref_list[r][i] != 0:
                    one_trail_rref_str += "delta_upper_tk2_{} + ".format(i - state_bits * 4)
                    one_key_linear_contraint.append(i)
            for i in range(5 * state_bits, 6 * state_bits):
                if key_matrix_rref_list[r][i] != 0:
                    one_trail_rref_str += "delta_lower_tk2_{} + ".format(i - state_bits * 5)
                    one_key_linear_contraint.append(i)
            for i in range(6 * state_bits, 7 * state_bits):
                if key_matrix_rref_list[r][i] != 0:
                    one_trail_rref_str += "tk3_{} + ".format(i - state_bits * 6)
                    one_key_linear_contraint.append(i)
            for i in range(7 * state_bits, 8 * state_bits):
                if key_matrix_rref_list[r][i] != 0:
                    one_trail_rref_str += "delta_upper_tk3_{} + ".format(i - state_bits * 7)
                    one_key_linear_contraint.append(i)
            for i in range(8 * state_bits, 9 * state_bits):
                if key_matrix_rref_list[r][i] != 0:
                    one_trail_rref_str += "delta_lower_tk3_{} + ".format(i - state_bits * 8)
                    one_key_linear_contraint.append(i)
        one_trail_rref_str += " = " + str(key_matrix_rref_list[r][one_trail_key_bit])
        one_key_linear_contraint.append(key_matrix_rref_list[r][one_trail_key_bit])

        key_rref_str.append(one_trail_rref_str)
        key_space.append(one_key_linear_contraint)
    for k in range(len(key_rref_str)):
        print("# " + key_rref_str[k])


    return rank, rank1, key_rref_str, key_space