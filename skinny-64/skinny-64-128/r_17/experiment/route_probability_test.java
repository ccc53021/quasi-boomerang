package quasidifferential.boomerang.skinny_64.skinny_64_128.experiment;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;
import java.util.concurrent.ThreadLocalRandom;

import quasidifferential.boomerang.skinny_64.skinny_64_128.experiment.round_key_generating;

public class route_probability_test2 {

	public static void main(String[] args) {
		// TODO Auto-generated method stub

		long start = System.currentTimeMillis();

		int[] sbox_inverse = get_inverse_box(sbox, n, m);
		int[] lbox_inverse = get_inverse_box(lbox, n, m);

		System.out.println("-------------------- begining -----------------------");

		int number = 4;

		int encrypt_round = 17;

		int upper_round_upper = 7;
		int[] upper_input_difference = get_a_characteristic_1d_by_str("0x1000000000000000");
		int[] upper_output_difference = get_a_characteristic_1d_by_str("0x0010001000000010");

		int em_begin_round = 7;
		int em_round_upper = 1;
		int em_round_lower = 1;
		int[] em_input_difference = get_a_characteristic_1d_by_str("0x0010001000000010");
		int[] em_output_difference = get_a_characteristic_1d_by_str("0x0300000003000000");

//		int lower_begin_round = 7 + 1 + 1;
//		int lower_round_lower = 8;
//		int[] lower_input_difference = get_a_characteristic_1d_by_str("0x0300000003000000");
//		int[] lower_output_difference = get_a_characteristic_1d_by_str("0xd0060000d0068006");
		int lower_begin_round_r_1_to_4 = 7 + 1 + 1;
		int lower_round_lower_r_1_to_4 = 4;
		int[] lower_input_difference_r_1_to_4 = get_a_characteristic_1d_by_str("0x0300000003000000");
		int[] lower_output_difference_r_1_to_4 = get_a_characteristic_1d_by_str("0x0000000000000000");
		int lower_begin_round_r_5_to_8 = 7 + 1 + 1 + 4;
		int lower_round_lower_r_5_to_8 = 4;
		int[] lower_input_difference_r_5_to_8 = get_a_characteristic_1d_by_str("0x0000000000000000");
		int[] lower_output_difference_r_5_to_8 = get_a_characteristic_1d_by_str("0xd0060000d0068006");

		int[][][] tk_constraints = new int[][][] {
			{{16}, {17, 19}},
	        {{18}, {16, 17}},
	    };
		int[] tk_values = new int[] {1, 1};

		System.out.println("-------------------- generating initial tks --------------------------");
		int[][] tks = get_initial_random_tk1_and_tk2_and_tk3_by_given_constraints(tk_constraints, tk_values);
		int[] tk1_1 = tks[0];
		int[] tk2_1 = tks[1];
		int[] tk3_1 = tks[2];

		System.out.println("-------------------- generating tks --------------------------");
		String difference_tk1_delta_1 = "0x0000000600000000";
		String difference_tk1_delta_2 = "0xe00000000000c000";
		String difference_tk2_delta_1 = "0x0000000900000000";
		String difference_tk2_delta_2 = "0x600000000000a000";
		int[] tk1_2 = get_another_key_by_k_and_difference(get_a_difference_1d(difference_tk1_delta_1), tk1_1);
		int[] tk1_3 = get_another_key_by_k_and_difference(get_a_difference_1d(difference_tk1_delta_2), tk1_1);
		int[] tk1_4 = get_another_key_by_k_and_difference(get_a_difference_by_two_states(get_a_difference_1d(difference_tk1_delta_1), get_a_difference_1d(difference_tk1_delta_2)), tk1_1);
		int[] tk2_2 = get_another_key_by_k_and_difference(get_a_difference_1d(difference_tk2_delta_1), tk2_1);
		int[] tk2_3 = get_another_key_by_k_and_difference(get_a_difference_1d(difference_tk2_delta_2), tk2_1);
		int[] tk2_4 = get_another_key_by_k_and_difference(get_a_difference_by_two_states(get_a_difference_1d(difference_tk2_delta_1), get_a_difference_1d(difference_tk2_delta_2)), tk2_1);

		System.out.println("--------------- generating rks ---------------------");
		int[][][] round_tk1s = get_round_tks_by_initial_tk1_and_tk2(tk1_1, tk2_1, encrypt_round);
		int[][] round_tk1_1 = round_tk1s[0];
		int[][] round_tk2_1 = round_tk1s[1];
		int[][][] round_tk2s = get_round_tks_by_initial_tk1_and_tk2(tk1_2, tk2_2, encrypt_round);
		int[][] round_tk1_2 = round_tk2s[0];
		int[][] round_tk2_2 = round_tk2s[1];
		int[][][] round_tk3s = get_round_tks_by_initial_tk1_and_tk2(tk1_3, tk2_3, encrypt_round);
		int[][] round_tk1_3 = round_tk3s[0];
		int[][] round_tk2_3 = round_tk3s[1];
		int[][][] round_tk4s = get_round_tks_by_initial_tk1_and_tk2(tk1_4, tk2_4, encrypt_round);
		int[][] round_tk1_4 = round_tk4s[0];
		int[][] round_tk2_4 = round_tk4s[1];

		int[][][] round_tk1 = new int[4][][];
		round_tk1[0] = round_tk1_1;
		round_tk1[1] = round_tk1_2;
		round_tk1[2] = round_tk1_3;
		round_tk1[3] = round_tk1_4;
		int[][][] round_tk2 = new int[4][][];
		round_tk2[0] = round_tk2_1;
		round_tk2[1] = round_tk2_2;
		round_tk2[2] = round_tk2_3;
		round_tk2[3] = round_tk2_4;
		int[][][] round_tk3 = new int[4][][];

		System.out.println("------------------------ experiment ------------------");
		// p = 2^-12 * 3 = 0.000732421875 = 2^-10.415037499278844, p_e = 2^-10.43
		int upper_experiment_time = (int) Math.pow(2, 20);
		// p = 2^-2 = 0.25, p_e = 2^-2.00
		int em_experiment_time = (int) Math.pow(2, 20);
		// 1-st: p = 0, p_e = 0;
		// 2-nd: 2^-36.0 * 32 = 4.656612873077393e-10 = 2^-31.0, p_e = 2^-30.79;
		// 3-rd: p = 2^-36.0 * 8 = 1.1641532182693481e-10 = 2^-33.0, p_e = 2^-32.68;
		// 4-th: p = 2^-36.0 * 8 = 1.1641532182693481e-10 = 2^-33.0, p_e = 2^-33.41;
		int lower_experiment_time = (int) Math.pow(2, 25);
		one_experiment_amplified_upper(upper_input_difference, upper_output_difference, number, upper_experiment_time, sbox, sbox_inverse, lbox, lbox_inverse, sr_bits_table, sr_inverse_table, round_tk1, round_tk2, round_tk3, upper_round_upper);
		one_experiment_amplified_em(em_input_difference, em_output_difference, number, em_experiment_time, sbox, sbox_inverse, lbox, lbox_inverse, sr_bits_table, sr_inverse_table, round_tk1, round_tk2, round_tk3, em_begin_round, em_round_upper, em_round_lower);
//		one_experiment_amplified_lower(lower_input_difference, lower_output_difference, number, lower_experiment_time, sbox, sbox_inverse, lbox, lbox_inverse, sr_bits_table, sr_inverse_table, round_tk1, round_tk2, round_tk3, lower_begin_round, lower_round_lower);
		one_experiment_amplified_lower_jointly(lower_input_difference_r_1_to_4, lower_output_difference_r_1_to_4, lower_input_difference_r_5_to_8, lower_output_difference_r_5_to_8, number, lower_experiment_time, sbox, sbox_inverse, lbox, lbox_inverse, sr_bits_table, sr_inverse_table, round_tk1, round_tk2, round_tk3, lower_begin_round_r_1_to_4, lower_round_lower_r_1_to_4, lower_begin_round_r_5_to_8, lower_round_lower_r_5_to_8);


		long end = System.currentTimeMillis();
		System.out.println("run time is : " + (double) (end - start) / 1000 + "s");

	}

	public static int [][][] tk3s_64 = round_key_generating.tk3s_64;

	public static int[] SKINNY_64_SBOX = {0xc, 0x6, 0x9, 0x0, 0x1, 0xa, 0x2, 0xb, 0x3, 0x8, 0x5, 0xd, 0x4, 0xe, 0x7, 0xf};
	public static int n = 4;
	public static int m = 4;
	public static int[] sbox = SKINNY_64_SBOX;
	public static int state_bits = 64;
	public static int state_words = 16;
	public static int sbox_bits = 4;

	public static int[] lbox = new int[] {0, 8, 11, 3, 2, 10, 9, 1, 13, 5, 6, 14, 15, 7, 4, 12};

	public static int tk_number = 2;

	public static int[] rc_6_bits = new int[] {
	                                 0x01, 0x03, 0x07, 0x0F, 0x1F, 0x3E, 0x3D, 0x3B, 0x37, 0x2F, 0x1E, 0x3C, 0x39, 0x33, 0x27, 0x0E,
	                                 0x1D, 0x3A, 0x35, 0x2B, 0x16, 0x2C, 0x18, 0x30, 0x21, 0x02, 0x05, 0x0B, 0x17, 0x2E, 0x1C, 0x38,
	                                 0x31, 0x23, 0x06, 0x0D, 0x1B, 0x36, 0x2D, 0x1A, 0x34, 0x29, 0x12, 0x24, 0x08, 0x11, 0x22, 0x04};



	public static int[] get_inverse_box(int[] box, int n, int m) {
		int[] inverse_box = new int[(int) Math.pow(2, n)];
		for(int i = 0; i < inverse_box.length; i++) {
			inverse_box[box[i]] = i;
		}

		return inverse_box;
	}

	public static List get_sr_table_by_n(int bit_n) {
		List table = new ArrayList<>();
		for(int i = 0; i < 4 * bit_n; i++) {
	        table.add(i);
		}
		for(int i = 7 * bit_n; i < 8 * bit_n; i++) {
			table.add(i);
		}
		for(int i = 4 * bit_n; i < 7 * bit_n; i++) {
			table.add(i);
		}
		for(int i = 10 * bit_n; i < 12 * bit_n; i++) {
			table.add(i);
		}
		for(int i = 8 * bit_n; i < 10 * bit_n; i++) {
			table.add(i);
		}
		for(int i = 13 * bit_n; i < 16 * bit_n; i++) {
			table.add(i);
		}
		for(int i = 12 * bit_n; i < 13 * bit_n; i++) {
			table.add(i);
		}

		return table;
	}

	public static List sr_bits_table = get_sr_table_by_n(sbox_bits);

	public static List get_inverse_sr_table_by_n(int bit_n) {
		int[] tt = new int[] {0, 1, 2, 3, 5, 6, 7, 4, 10, 11, 8, 9, 15, 12, 13, 14};
		List table = new ArrayList<>();
		for(int iii = 0; iii < tt.length; iii++) {
			int ii = tt[iii];
			for(int i = ii * bit_n; i < (ii + 1) * bit_n; i++) {
				table.add(i);
			}
		}

		return table;
	}

	public static List sr_inverse_table = get_inverse_sr_table_by_n(sbox_bits);

	public static List get_pn_table_by_n(int bit_n) {
		int[] tt = new int[] {9, 15, 8, 13, 10, 14, 12, 11, 0, 1, 2, 3, 4, 5, 6, 7};
		List table = new ArrayList<>();
		for(int iii = 0; iii < tt.length; iii++) {
			int ii = tt[iii];
			for(int i = ii * bit_n; i < (ii + 1) * bit_n; i++) {
				table.add(i);
			}
		}

		return table;
	}

	public static List pn_bits_table = get_pn_table_by_n(sbox_bits);

	public static List get_inverse_pn_table_by_n(int bit_n) {
		int[] tt = new int[] {8, 9, 10, 11, 12, 13, 14, 15, 2, 0, 4, 7, 6, 3, 5, 1};
		List table = new ArrayList<>();
		for(int iii = 0; iii < tt.length; iii++) {
			int ii = tt[iii];
			for(int i = ii * bit_n; i < (ii + 1) * bit_n; i++) {
				table.add(i);
			}
		}

		return table;
	}

	public static List pn_inverse_table = get_inverse_pn_table_by_n(sbox_bits);


	public static int[] permute_bits_by_table(int[] x, List table) {
		int[] y = new int[state_bits];
		for(int i = 0; i < state_bits; i++) {
			y[i] = x[(int) table.get(i)];
		}

		return y;
	}

	public static int[] sbox_layer_by_table(int[] x, int[] table) {
		int[] y = new int[state_bits];
		for(int i = 0; i < state_bits; i += sbox_bits) {
			String sbox_input_str = "";
			for(int j = 0; j < sbox_bits; j++) {
				sbox_input_str = x[i + j] + sbox_input_str;
			}
			int sbox_input = Integer.parseInt(sbox_input_str, 2);
			int sbox_output = table[sbox_input];
			for(int j = 0; j < sbox_bits; j++) {
				y[i + j] = (sbox_output >> j) & 0x1;
 			}
		}

		return y;
	}

	public static int[] lbox_layer_by_table(int[] x, int[] table) {
		int[] y = new int[state_bits];
		for(int i = 0; i < state_words; i++) {
			String sbox_input_str = "";
			for(int j = 0; j < sbox_bits; j++) {
				sbox_input_str = sbox_input_str + x[i + j * 4 * sbox_bits];
			}
			int sbox_input = Integer.parseInt(sbox_input_str, 2);
			int sbox_output = table[sbox_input];
			for(int j = 0; j < sbox_bits; j++) {
				y[i + j * 4 * sbox_bits] = (sbox_output >> (sbox_bits - 1 - j)) & 0x1;
 			}
		}

		return y;
	}

	public static int[] xor_rc(int[] x, int rcs) {
		int[]y = new int[x.length];
		for(int i = 0; i < x.length; i++) {
			y[i] = x[i];
		}
		int c0 = rcs & 0xf;
		int c1 = (rcs >> 4) & 0x3;
		int c2 = 0xc2;
		for(int i = 0; i < sbox_bits; i++) {
			y[i] ^= (c0 >> i) & 0x1;
		}
		for(int i = 4 * sbox_bits; i < 5 * sbox_bits; i++) {
			y[i] ^= (c1 >> i) & 0x1;
		}
		for(int i = 8 * sbox_bits; i < 9 * sbox_bits; i++) {
			y[i] ^= (c2 >> i) & 0x1;
		}

		return y;
 	}

	public static int[] xor_tk1(int[] x, int[] tk) {
		int[] y = new int[x.length];
		for(int i = 0; i < x.length; i++) {
			y[i] = x[i];
		}
		for(int i = 0; i < state_bits / 2; i++) {
			y[i] ^= tk[i];
		}

		return y;
	}

	public static int[] xor_tk1_and_tk2(int[] x, int[] tk1, int[] tk2) {
		int[] y = new int[x.length];
		for(int i = 0; i < x.length; i++) {
			y[i] = x[i];
		}
		for(int i = 0; i < state_bits / 2; i++) {
			y[i] ^= tk1[i];
			y[i] ^= tk2[i];
		}

		return y;
	}

	public static int[] xor_tk1_and_tk2_and_tk3(int[] x, int[] tk1, int[] tk2, int[] tk3) {
		int[] y = new int[x.length];
		for(int i = 0; i < x.length; i++) {
			y[i] = x[i];
		}
		for(int i = 0; i < state_bits / 2; i++) {
			y[i] ^= tk1[i];
			y[i] ^= tk2[i];
			y[i] ^= tk3[i];
		}

		return y;
	}

	public static int[][] get_initial_random_tk1_and_tk2_and_tk3() {
		int[] initial_tk1 = new int[state_bits];
		int[] initial_tk2 = new int[state_bits];
		int[] initial_tk3 = new int[state_bits];
		Random rd = new Random();
		for(int i = 0; i < state_bits; i++) {
			initial_tk1[i] = rd.nextInt(2);
			initial_tk2[i] = rd.nextInt(2);
			initial_tk3[i] = rd.nextInt(2);
		}

		int[][] initial_tks = new int[3][];
		initial_tks[0] = initial_tk1;
		initial_tks[1] = initial_tk2;
		initial_tks[2] = initial_tk3;

		return initial_tks;
	}

	public static int[][] get_initial_random_tk1_and_tk2_and_tk3_by_given_constraints(int[][][] constraints, int[] values) {
		int[] initial_tk1 = new int[state_bits];
		int[] initial_tk2 = new int[state_bits];
		int[] initial_tk3 = new int[state_bits];

		Random rd = new Random();

		int flag_t = 0;
		while (flag_t == 0) {

			for(int i = 0; i < state_bits; i++) {
				initial_tk1[i] = rd.nextInt(2);
				initial_tk2[i] = rd.nextInt(2);
				initial_tk3[i] = rd.nextInt(2);
			}

			int count_t = 0;
			if (tk_number == 1) {
				for(int i = 0; i < constraints.length; i++) {
					int[] one_constraint_tk1 = constraints[i][0];
					int one_value = values[i];
					int temp = 0;
					for(int ii = 0; ii < one_constraint_tk1.length; ii++) {
						int tkk1 = one_constraint_tk1[ii];
						temp ^= initial_tk1[tkk1];
					}
					if (temp == one_value) {
						count_t += 1;
					}
				}
			} else if (tk_number == 2) {
				for(int i = 0; i < constraints.length; i++) {
					int[] one_constraint_tk1 = constraints[i][0];
					int[] one_constraint_tk2 = constraints[i][1];
					int one_value = values[i];
					int temp = 0;
					for(int ii = 0; ii < one_constraint_tk1.length; ii++) {
						int tkk1 = one_constraint_tk1[ii];
						temp ^= initial_tk1[tkk1];
					}
					for(int ii = 0; ii < one_constraint_tk2.length; ii++) {
						int tkk2 = one_constraint_tk2[ii];
						temp ^= initial_tk2[tkk2];
					}
					if (temp == one_value) {
						count_t += 1;
					}
				}
			} else if (tk_number == 3) {
				for(int i = 0; i < constraints.length; i++) {
					int[] one_constraint_tk1 = constraints[i][0];
					int[] one_constraint_tk2 = constraints[i][1];
					int[] one_constraint_tk3 = constraints[i][2];
					int one_value = values[i];
					int temp = 0;
					for(int ii = 0; ii < one_constraint_tk1.length; ii++) {
						int tkk1 = one_constraint_tk1[ii];
						temp ^= initial_tk1[tkk1];
					}
					for(int ii = 0; ii < one_constraint_tk2.length; ii++) {
						int tkk2 = one_constraint_tk2[ii];
						temp ^= initial_tk2[tkk2];
					}
					for(int ii = 0; ii < one_constraint_tk3.length; ii++) {
						int tkk3 = one_constraint_tk3[ii];
						temp ^= initial_tk3[tkk3];
					}
					if (temp == one_value) {
						count_t += 1;
					}
				}
			}

			if (count_t == constraints.length) {
				flag_t = 1;
			}

		}

		int[][] initial_tks = new int[3][];
		initial_tks[0] = initial_tk1;
		initial_tks[1] = initial_tk2;
		initial_tks[2] = initial_tk3;

		return initial_tks;
	}

	public static int[][][] get_round_tks_by_initial_tk1_and_tk2(int[] initial_tk1, int[] initial_tk2, int round) {
		int[][] round_tk1s = new int[round][];
		int[][] round_tk2s = new int[round][];

		for(int r = 0; r < round; r++) {
			if (tk_number == 1) {
				int[][] bits_tk1 = tk1s_64[r];
				int[] rk1 = new int[bits_tk1.length];
				for(int i = 0; i < bits_tk1.length; i++) {
					int temp = 0;
					int[] one_i = bits_tk1[i];
					for(int ii = 0; ii < one_i.length; ii++) {
						int kk1 = one_i[ii];
						temp ^= initial_tk1[kk1];
					}
					rk1[i] = temp;
				}
				round_tk1s[r] = rk1;
			} else if (tk_number == 2) {
				int[][] bits_tk1 = tk1s_64[r];
				int[] rk1 = new int[bits_tk1.length];
				for(int i = 0; i < bits_tk1.length; i++) {
					int temp = 0;
					int[] one_i = bits_tk1[i];
					for(int ii = 0; ii < one_i.length; ii++) {
						int kk1 = one_i[ii];
						temp ^= initial_tk1[kk1];
					}
					rk1[i] = temp;
				}
				round_tk1s[r] = rk1;

				int[][] bits_tk2 = tk2s_64[r];
				int[] rk2 = new int[bits_tk2.length];
				for(int i = 0; i < bits_tk2.length; i++) {
					int temp = 0;
					int[] one_i = bits_tk2[i];
					for(int ii = 0; ii < one_i.length; ii++) {
						int kk2 = one_i[ii];
						temp ^= initial_tk2[kk2];
					}
					rk2[i] = temp;
				}
				round_tk2s[r] = rk2;
			}
		}

		int[][][] round_tks = new int[2][][];
		round_tks[0] = round_tk1s;
		round_tks[1] = round_tk2s;

		return round_tks;

	}

	public static int[][] get_an_random_plaintext_and_another_by_difference(int[] input_difference) {
		int[] x = new int[state_bits];
		int[] x1 = new int[state_bits];
		ThreadLocalRandom random = ThreadLocalRandom.current();
		for(int i = 0; i < state_bits; i++) {
			x[i] = random.nextInt(2);
			x1[i] = x[i] ^ input_difference[i];
		}

		int[][] x_and_x1 = new int[2][];
		x_and_x1[0] = x;
		x_and_x1[1] = x1;

		return x_and_x1;
	}

	public static int[] get_another_key_by_k_and_difference(int[] input_difference, int[] one_key) {

		int[] k1 = new int[state_bits];
		for(int i = 0; i < state_bits; i++) {
			k1[i] = one_key[i] ^ input_difference[i];
		}

		return k1;
	}

	public static int[] get_a_characteristic_1d_by_str(String difference) {
		int[] diff_1d = new int[state_bits];
		String one_d_str = difference;
		one_d_str = one_d_str.substring(2);
		for(int j = 0; j < state_words; j++) {
			String one_s_str = one_d_str.substring(state_words - j - 1, state_words - j);
			int one_s = Integer.parseInt(one_s_str, 16);
			for(int k = 0; k < sbox_bits; k++) {
				diff_1d[k + j * sbox_bits] = (one_s >> k) & 0x1;
			}
		}

		return diff_1d;
	}

	public static int[] get_a_difference_1d(String difference) {
		String one_d_str = difference.substring(2);
		int[] differnce_1d = new int[state_bits];
		for(int j = 0; j < state_words; j++) {
			String one_s_str = one_d_str.substring(state_words - j - 1, state_words - j);
			int one_s = Integer.parseInt(one_s_str, 16);
			for(int k = 0; k < sbox_bits; k++) {
				differnce_1d[k + j * sbox_bits] = (one_s >> k) & 0x1;
			}
		}

		return differnce_1d;
	}

	public static int[] get_a_difference_by_two_states(int[] x, int[] x1) {
		int[] diff = new int[state_bits];
		for(int i = 0; i < state_bits; i++) {
			diff[i] = x[i] ^ x1[i];
		}

		return diff;
	}

	public static void one_experiment_amplified_upper(int[] input_difference, int[] output_difference, int number, int experiment_time, int[] sbox, int[] sbox_inverse, int[] lbox, int[] lbox_inverse, List sr_bits_table, List sr_inverse_table, int[][][] round_tk1, int[][][] round_tk2, int[][][] round_tk3, int round_upper) {
		int count_rp = 0;
		for(int et = 0; et < experiment_time; et++) {
			int[][] x_and_x1 = get_an_random_plaintext_and_another_by_difference(input_difference);
			int[] x = x_and_x1[0];
			int[] x1 = x_and_x1[1];

			int[][] x2_and_x3 = get_an_random_plaintext_and_another_by_difference(input_difference);
			int[] x2 = x2_and_x3[0];
			int[] x3 = x2_and_x3[1];

			int[] y = new int[x.length];
			int[] y1 = new int[x1.length];
			int[] y2 = new int[x2.length];
			int[] y3 = new int[x3.length];
			for(int i = 0; i < x.length; i++) {
				y[i] = x[i];
				y1[i] = x1[i];
				y2[i] = x2[i];
				y3[i] = x3[i];
			}

			int flag_rp = 1;
			for(int i = 0; i < round_upper; i++) {
				// sb
				y = sbox_layer_by_table(y, sbox);
				y1 = sbox_layer_by_table(y1, sbox);
				y2 = sbox_layer_by_table(y2, sbox);
				y3 = sbox_layer_by_table(y3, sbox);

				int[] diff_y_11 = get_a_difference_by_two_states(y,  y1);
				int[] diff_y_22 = get_a_difference_by_two_states(y2,  y3);
				if (Arrays.equals(diff_y_11, diff_y_22)) {
					// ac
					y = xor_rc(y, rc_6_bits[i]);
					y1 = xor_rc(y1, rc_6_bits[i]);
					y2 = xor_rc(y2, rc_6_bits[i]);
					y3 = xor_rc(y3, rc_6_bits[i]);

					// art
					if (tk_number == 1) {
						int[][] round_tk1_1 = round_tk1[0];
						int[][] round_tk1_2 = round_tk1[1];
						int[][] round_tk1_3 = round_tk1[2];
						int[][] round_tk1_4 = round_tk1[3];
						y = xor_tk1(y, round_tk1_1[i]);
						y1 = xor_tk1(y1, round_tk1_2[i]);
						y2 = xor_tk1(y2, round_tk1_3[i]);
						y3 = xor_tk1(y3, round_tk1_4[i]);
					} else if (tk_number == 2) {
						int[][] round_tk1_1 = round_tk1[0];
						int[][] round_tk1_2 = round_tk1[1];
						int[][] round_tk1_3 = round_tk1[2];
						int[][] round_tk1_4 = round_tk1[3];
						int[][] round_tk2_1 = round_tk2[0];
						int[][] round_tk2_2 = round_tk2[1];
						int[][] round_tk2_3 = round_tk2[2];
						int[][] round_tk2_4 = round_tk2[3];
						y = xor_tk1_and_tk2(y, round_tk1_1[i], round_tk2_1[i]);
						y1 = xor_tk1_and_tk2(y1, round_tk1_2[i], round_tk2_2[i]);
						y2 = xor_tk1_and_tk2(y2, round_tk1_3[i], round_tk2_3[i]);
						y3 = xor_tk1_and_tk2(y3, round_tk1_4[i], round_tk2_4[i]);
					} else if (tk_number == 3) {
						int[][] round_tk1_1 = round_tk1[0];
						int[][] round_tk1_2 = round_tk1[1];
						int[][] round_tk1_3 = round_tk1[2];
						int[][] round_tk1_4 = round_tk1[3];
						int[][] round_tk2_1 = round_tk2[0];
						int[][] round_tk2_2 = round_tk2[1];
						int[][] round_tk2_3 = round_tk2[2];
						int[][] round_tk2_4 = round_tk2[3];
						int[][] round_tk3_1 = round_tk3[0];
						int[][] round_tk3_2 = round_tk3[1];
						int[][] round_tk3_3 = round_tk3[2];
						int[][] round_tk3_4 = round_tk3[3];
						y = xor_tk1_and_tk2_and_tk3(y, round_tk1_1[i], round_tk2_1[i], round_tk3_1[i]);
						y1 = xor_tk1_and_tk2_and_tk3(y1, round_tk1_2[i], round_tk2_2[i], round_tk3_2[i]);
						y2 = xor_tk1_and_tk2_and_tk3(y2, round_tk1_3[i], round_tk2_3[i], round_tk3_3[i]);
						y3 = xor_tk1_and_tk2_and_tk3(y3, round_tk1_4[i], round_tk2_4[i], round_tk3_4[i]);
					}

					// sr
					y = permute_bits_by_table(y, sr_bits_table);
					y1 = permute_bits_by_table(y1, sr_bits_table);
					y2 = permute_bits_by_table(y2, sr_bits_table);
					y3 = permute_bits_by_table(y3, sr_bits_table);

					// mc
					y = lbox_layer_by_table(y, lbox);
					y1 = lbox_layer_by_table(y1, lbox);
					y2 = lbox_layer_by_table(y2, lbox);
					y3 = lbox_layer_by_table(y3, lbox);
				} else {
					flag_rp = 0;
					break;
				}
			}

			int[] diff_y_1 = get_a_difference_by_two_states(y, y1);
			int[] diff_y_2 = get_a_difference_by_two_states(y2, y3);
			int[] diff_r = output_difference;
			if (Arrays.equals(diff_y_1, diff_r) && Arrays.equals(diff_y_2, diff_r)) {
				flag_rp = 1;
			} else {
				flag_rp = 0;
			}

			count_rp += flag_rp;
		}

		System.out.println();
		System.out.println("upper: ");
		double index = Math.log10((double) count_rp / experiment_time) / Math.log10(2);;
		System.out.println("time " + experiment_time + ", right pairs : " + count_rp + ", p = " + (double) count_rp / experiment_time + " = 2^-" + -index);

	}

	public static void one_experiment_amplified_em(int[] input_difference, int[] output_difference, int number, int experiment_time, int[] sbox, int[] sbox_inverse, int[] lbox, int[] lbox_inverse, List sr_bits_table, List sr_inverse_table, int[][][] round_tk1, int[][][] round_tk2, int[][][] round_tk3, int begin_round, int round_upper, int round_lower) {
		int count_rp = 0;
		for(int et = 0; et < experiment_time; et++) {
			int[][] x_and_x1 = get_an_random_plaintext_and_another_by_difference(input_difference);
			int[] x = x_and_x1[0];
			int[] x1 = x_and_x1[1];

			int[] y = new int[x.length];
			int[] y1 = new int[x1.length];
			for(int i = 0; i < x.length; i++) {
				y[i] = x[i];
				y1[i] = x1[i];
			}

			int flag_rp = 1;
			for(int i = 0; i < round_upper + round_lower; i++) {
				// sb
				y = sbox_layer_by_table(y, sbox);
				y1 = sbox_layer_by_table(y1, sbox);

				// ac
				y = xor_rc(y, rc_6_bits[i + begin_round]);
				y1 = xor_rc(y1, rc_6_bits[i + begin_round]);

				// art
				if (tk_number == 1) {
					int[][] round_tk1_1 = round_tk1[0];
					int[][] round_tk1_2 = round_tk1[1];
					y = xor_tk1(y, round_tk1_1[i + begin_round]);
					y1 = xor_tk1(y1, round_tk1_2[i + begin_round]);
				} else if (tk_number == 2) {
					int[][] round_tk1_1 = round_tk1[0];
					int[][] round_tk1_2 = round_tk1[1];
					int[][] round_tk2_1 = round_tk2[0];
					int[][] round_tk2_2 = round_tk2[1];
					y = xor_tk1_and_tk2(y, round_tk1_1[i + begin_round], round_tk2_1[i + begin_round]);
					y1 = xor_tk1_and_tk2(y1, round_tk1_2[i + begin_round], round_tk2_2[i + begin_round]);
				} else if (tk_number == 3) {
					int[][] round_tk1_1 = round_tk1[0];
					int[][] round_tk1_2 = round_tk1[1];
					int[][] round_tk2_1 = round_tk2[0];
					int[][] round_tk2_2 = round_tk2[1];
					int[][] round_tk3_1 = round_tk2[0];
					int[][] round_tk3_2 = round_tk2[1];
					y = xor_tk1_and_tk2_and_tk3(y, round_tk1_1[i + begin_round], round_tk2_1[i + begin_round], round_tk3_1[i + begin_round]);
					y1 = xor_tk1_and_tk2_and_tk3(y1, round_tk1_2[i + begin_round], round_tk2_2[i + begin_round], round_tk3_2[i + begin_round]);
				}

				// sr
				y = permute_bits_by_table(y, sr_bits_table);
				y1 = permute_bits_by_table(y1, sr_bits_table);

				// mc
				y = lbox_layer_by_table(y, lbox);
				y1 = lbox_layer_by_table(y1, lbox);
			}

			int[] y2 = new int[state_bits];
			int[] y3 = new int[state_bits];
			for(int iii = 0; iii < state_bits; iii++) {
				y2[iii] = y[iii];
				y3[iii] = y1[iii];
			}
			y2 = get_another_key_by_k_and_difference(output_difference, y2);
			y3 = get_another_key_by_k_and_difference(output_difference, y3);


			for(int i = round_upper + round_lower - 1; i > - 1; i--) {
				// mc-1
				y2 = lbox_layer_by_table(y2, lbox_inverse);
				y3 = lbox_layer_by_table(y3, lbox_inverse);

				// sr-1
				y2 = permute_bits_by_table(y2, sr_inverse_table);
				y3 = permute_bits_by_table(y3, sr_inverse_table);

				// art
				if (tk_number == 1) {
					int[][] round_tk1_3 = round_tk1[2];
					int[][] round_tk1_4 = round_tk1[3];
					y2 = xor_tk1(y2, round_tk1_3[i + begin_round]);
					y3 = xor_tk1(y3, round_tk1_4[i + begin_round]);
				} else if (tk_number == 2) {
					int[][] round_tk1_3 = round_tk1[2];
					int[][] round_tk1_4 = round_tk1[3];
					int[][] round_tk2_3 = round_tk2[2];
					int[][] round_tk2_4 = round_tk2[3];
					y2 = xor_tk1_and_tk2(y2, round_tk1_3[i + begin_round], round_tk2_3[i + begin_round]);
					y3 = xor_tk1_and_tk2(y3, round_tk1_4[i + begin_round], round_tk2_4[i + begin_round]);
				} else if (tk_number == 3) {
					int[][] round_tk1_3 = round_tk1[2];
					int[][] round_tk1_4 = round_tk1[3];
					int[][] round_tk2_3 = round_tk2[2];
					int[][] round_tk2_4 = round_tk2[3];
					int[][] round_tk3_3 = round_tk3[2];
					int[][] round_tk3_4 = round_tk3[3];
					y2 = xor_tk1_and_tk2_and_tk3(y2, round_tk1_3[i + begin_round], round_tk2_3[i + begin_round], round_tk3_3[i + begin_round]);
					y3 = xor_tk1_and_tk2_and_tk3(y3, round_tk1_4[i + begin_round], round_tk2_4[i + begin_round], round_tk3_4[i + begin_round]);
				}

				// ac
				y2 = xor_rc(y2, rc_6_bits[i + begin_round]);
				y3 = xor_rc(y3, rc_6_bits[i + begin_round]);

				// sb-1
				y2 = sbox_layer_by_table(y2, sbox_inverse);
				y3 = sbox_layer_by_table(y3, sbox_inverse);
			}

			int[] diff_y = get_a_difference_by_two_states(y2, y3);
			int[] diff_r = input_difference;
			if (!Arrays.equals(diff_y, diff_r)) {
				flag_rp = 0;
			} else {
				flag_rp = 1;
			}

			count_rp += flag_rp;
		}

		System.out.println();
		System.out.println("em: ");
		double index = Math.log10((double) count_rp / experiment_time) / Math.log10(2);;
		System.out.println("time " + experiment_time + ", right pairs : " + count_rp + ", p = " + (double) count_rp / experiment_time + " = 2^-" + -index);

	}

	public static int one_experiment_amplified_lower(int[] input_difference, int[] output_difference, int number, int experiment_time, int[] sbox, int[] sbox_inverse, int[] lbox, int[] lbox_inverse, List sr_bits_table, List sr_inverse_table, int[][][] round_tk1, int[][][] round_tk2, int[][][] round_tk3, int begin_round, int round_lower) {
		int count_rp = 0;
		for(int et = 0; et < experiment_time; et++) {
			int[][] x_and_x1 = get_an_random_plaintext_and_another_by_difference(input_difference);
			int[] x = x_and_x1[0];
			int[] x1 = x_and_x1[1];
			int[][] x2_and_x3 = get_an_random_plaintext_and_another_by_difference(input_difference);
			int[] x2 = x2_and_x3[0];
			int[] x3 = x2_and_x3[1];

			int[] y = new int[x.length];
			int[] y1 = new int[x1.length];
			int[] y2 = new int[x2.length];
			int[] y3 = new int[x3.length];
			for(int i = 0; i < x.length; i++) {
				y[i] = x[i];
				y1[i] = x1[i];
				y2[i] = x2[i];
				y3[i] = x3[i];
			}

			int flag_rp = 1;
			for(int i = 0; i < round_lower; i++) {
				// sb
				y = sbox_layer_by_table(y, sbox);
				y1 = sbox_layer_by_table(y1, sbox);
				y2 = sbox_layer_by_table(y2, sbox);
				y3 = sbox_layer_by_table(y3, sbox);

				int[] diff_y_11 = get_a_difference_by_two_states(y, y1);
				int[] diff_y_22 = get_a_difference_by_two_states(y2, y3);

				if(Arrays.equals(diff_y_11, diff_y_22)) {
					// ac
					y = xor_rc(y, rc_6_bits[i + begin_round]);
					y1 = xor_rc(y1, rc_6_bits[i + begin_round]);
					y2 = xor_rc(y2, rc_6_bits[i + begin_round]);
					y3 = xor_rc(y3, rc_6_bits[i + begin_round]);

					// art
					if (tk_number == 1) {
						int[][] round_tk1_1 = round_tk1[0];
						int[][] round_tk1_3 = round_tk1[2];
						y = xor_tk1(y, round_tk1_1[i + begin_round]);
						y1 = xor_tk1(y1, round_tk1_3[i + begin_round]);
						int[][] round_tk1_2 = round_tk1[1];
						int[][] round_tk1_4 = round_tk1[3];
						y2 = xor_tk1(y2, round_tk1_2[i + begin_round]);
						y3 = xor_tk1(y3, round_tk1_4[i + begin_round]);
					} else if (tk_number == 2) {
						int[][] round_tk1_1 = round_tk1[0];
						int[][] round_tk1_3 = round_tk1[2];
						int[][] round_tk2_1 = round_tk2[0];
						int[][] round_tk2_3 = round_tk2[2];
						y = xor_tk1_and_tk2(y, round_tk1_1[i + begin_round], round_tk2_1[i + begin_round]);
						y1 = xor_tk1_and_tk2(y1, round_tk1_3[i + begin_round], round_tk2_3[i + begin_round]);
						int[][] round_tk1_2 = round_tk1[1];
						int[][] round_tk1_4 = round_tk1[3];
						int[][] round_tk2_2 = round_tk2[1];
						int[][] round_tk2_4 = round_tk2[3];
						y2 = xor_tk1_and_tk2(y2, round_tk1_2[i + begin_round], round_tk2_2[i + begin_round]);
						y3 = xor_tk1_and_tk2(y3, round_tk1_4[i + begin_round], round_tk2_4[i + begin_round]);
					} else if (tk_number == 3) {
						int[][] round_tk1_1 = round_tk1[0];
						int[][] round_tk1_3 = round_tk1[2];
						int[][] round_tk2_1 = round_tk2[0];
						int[][] round_tk2_3 = round_tk2[2];
						int[][] round_tk3_1 = round_tk3[0];
						int[][] round_tk3_3 = round_tk3[2];
						y = xor_tk1_and_tk2_and_tk3(y, round_tk1_1[i + begin_round], round_tk2_1[i + begin_round], round_tk3_1[i + begin_round]);
						y1 = xor_tk1_and_tk2_and_tk3(y1, round_tk1_3[i + begin_round], round_tk2_3[i + begin_round], round_tk3_3[i + begin_round]);
						int[][] round_tk1_2 = round_tk1[1];
						int[][] round_tk1_4 = round_tk1[3];
						int[][] round_tk2_2 = round_tk2[1];
						int[][] round_tk2_4 = round_tk2[3];
						int[][] round_tk3_2 = round_tk3[1];
						int[][] round_tk3_4 = round_tk3[3];
						y2 = xor_tk1_and_tk2_and_tk3(y2, round_tk1_2[i + begin_round], round_tk2_2[i + begin_round], round_tk3_2[i + begin_round]);
						y3 = xor_tk1_and_tk2_and_tk3(y3, round_tk1_4[i + begin_round], round_tk2_4[i + begin_round], round_tk3_4[i + begin_round]);
					}

					// sr
					y = permute_bits_by_table(y, sr_bits_table);
					y1 = permute_bits_by_table(y1, sr_bits_table);
					y2 = permute_bits_by_table(y2, sr_bits_table);
					y3 = permute_bits_by_table(y3, sr_bits_table);

					// mc
					y = lbox_layer_by_table(y, lbox);
					y1 = lbox_layer_by_table(y1, lbox);
					y2 = lbox_layer_by_table(y2, lbox);
					y3 = lbox_layer_by_table(y3, lbox);
				} else {
					flag_rp = 0;
					break;
				}
			}

			int[] diff_y_1 = get_a_difference_by_two_states(y, y1);
			int[] diff_y_2 = get_a_difference_by_two_states(y2, y3);
			int[] diff_r = output_difference;
			if (Arrays.equals(diff_y_1, diff_r) && Arrays.equals(diff_y_2, diff_r)) {
				flag_rp = 1;
			} else {
				flag_rp = 0;
			}

			count_rp += flag_rp;
		}

		return count_rp;

	}

	public static void one_experiment_amplified_lower_jointly(int[] input_difference_1, int[] output_difference_1, int[] input_difference_2, int[] output_difference_2, int number, int experiment_time, int[] sbox, int[] sbox_inverse, int[] lbox, int[] lbox_inverse, List sr_bits_table, List sr_inverse_table, int[][][] round_tk1, int[][][] round_tk2, int[][][] round_tk3, int begin_round_1, int round_lower_1, int begin_round_2, int round_lower_2) {
		int count_rp_1 = one_experiment_amplified_lower(input_difference_1, output_difference_1, number, experiment_time, sbox, sbox_inverse, lbox, lbox_inverse, sr_bits_table, sr_inverse_table, round_tk1, round_tk2, round_tk3, begin_round_1, round_lower_1);
		int count_rp_2 = one_experiment_amplified_lower(input_difference_2, output_difference_2, number, experiment_time, sbox, sbox_inverse, lbox, lbox_inverse, sr_bits_table, sr_inverse_table, round_tk1, round_tk2, round_tk3, begin_round_2, round_lower_2);

		System.out.println();
		System.out.println("lower: ");
		double index_1 = Math.log10((double) count_rp_1 / experiment_time) / Math.log10(2);
		double index_2 = Math.log10((double) count_rp_2 / experiment_time) / Math.log10(2);
		System.out.println(count_rp_1);
		System.out.println(count_rp_2);
		System.out.println("time " + experiment_time + ", right pairs : " + count_rp_1 * count_rp_2 + ", p = " + (double) (count_rp_1 * count_rp_2) / (experiment_time * experiment_time) + " = 2^-" + -(index_1 + index_2));

	}


	public static int[][][] tk1s_64 = new int[][][] {
		// round 0
        {{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}, {16}, {17}, {18}, {19}, {20},
         {21}, {22}, {23}, {24}, {25}, {26}, {27}, {28}, {29}, {30}, {31}},
        // round 1
        {{36}, {37}, {38}, {39}, {60}, {61}, {62}, {63}, {32}, {33}, {34}, {35}, {52}, {53}, {54}, {55}, {40}, {41}, {42},
         {43}, {56}, {57}, {58}, {59}, {48}, {49}, {50}, {51}, {44}, {45}, {46}, {47}},
        // round 2
        {{4}, {5}, {6}, {7}, {28}, {29}, {30}, {31}, {0}, {1}, {2}, {3}, {20}, {21}, {22}, {23}, {8}, {9}, {10}, {11}, {24},
         {25}, {26}, {27}, {16}, {17}, {18}, {19}, {12}, {13}, {14}, {15}},
        // round 3
        {{60}, {61}, {62}, {63}, {44}, {45}, {46}, {47}, {36}, {37}, {38}, {39}, {56}, {57}, {58}, {59}, {32}, {33}, {34},
         {35}, {48}, {49}, {50}, {51}, {40}, {41}, {42}, {43}, {52}, {53}, {54}, {55}},
        // round 4
        {{28}, {29}, {30}, {31}, {12}, {13}, {14}, {15}, {4}, {5}, {6}, {7}, {24}, {25}, {26}, {27}, {0}, {1}, {2}, {3},
         {16}, {17}, {18}, {19}, {8}, {9}, {10}, {11}, {20}, {21}, {22}, {23}},
        // round 5
        {{44}, {45}, {46}, {47}, {52}, {53}, {54}, {55}, {60}, {61}, {62}, {63}, {48}, {49}, {50}, {51}, {36}, {37}, {38},
         {39}, {40}, {41}, {42}, {43}, {32}, {33}, {34}, {35}, {56}, {57}, {58}, {59}},
        // round 6
        {{12}, {13}, {14}, {15}, {20}, {21}, {22}, {23}, {28}, {29}, {30}, {31}, {16}, {17}, {18}, {19}, {4}, {5}, {6}, {7},
         {8}, {9}, {10}, {11}, {0}, {1}, {2}, {3}, {24}, {25}, {26}, {27}},
        // round 7
        {{52}, {53}, {54}, {55}, {56}, {57}, {58}, {59}, {44}, {45}, {46}, {47}, {40}, {41}, {42}, {43}, {60}, {61}, {62},
         {63}, {32}, {33}, {34}, {35}, {36}, {37}, {38}, {39}, {48}, {49}, {50}, {51}},
        // round 8
        {{20}, {21}, {22}, {23}, {24}, {25}, {26}, {27}, {12}, {13}, {14}, {15}, {8}, {9}, {10}, {11}, {28}, {29}, {30},
         {31}, {0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {16}, {17}, {18}, {19}},
        // round 9
        {{56}, {57}, {58}, {59}, {48}, {49}, {50}, {51}, {52}, {53}, {54}, {55}, {32}, {33}, {34}, {35}, {44}, {45}, {46}, {47}, {36}, {37}, {38}, {39}, {60}, {61}, {62}, {63}, {40}, {41}, {42}, {43}},
        // round 10
        {{24}, {25}, {26}, {27}, {16}, {17}, {18}, {19}, {20}, {21}, {22}, {23}, {0}, {1}, {2}, {3}, {12}, {13}, {14}, {15}, {4}, {5}, {6}, {7}, {28}, {29}, {30}, {31}, {8}, {9}, {10}, {11}},
        // round 11
        {{48}, {49}, {50}, {51}, {40}, {41}, {42}, {43}, {56}, {57}, {58}, {59}, {36}, {37}, {38}, {39}, {52}, {53}, {54}, {55}, {60}, {61}, {62}, {63}, {44}, {45}, {46}, {47}, {32}, {33}, {34}, {35}},
        // round 12
        {{16}, {17}, {18}, {19}, {8}, {9}, {10}, {11}, {24}, {25}, {26}, {27}, {4}, {5}, {6}, {7}, {20}, {21}, {22}, {23}, {28}, {29}, {30}, {31}, {12}, {13}, {14}, {15}, {0}, {1}, {2}, {3}},
        // round 13
        {{40}, {41}, {42}, {43}, {32}, {33}, {34}, {35}, {48}, {49}, {50}, {51}, {60}, {61}, {62}, {63}, {56}, {57}, {58}, {59}, {44}, {45}, {46}, {47}, {52}, {53}, {54}, {55}, {36}, {37}, {38}, {39}},
        // round 14
        {{8}, {9}, {10}, {11}, {0}, {1}, {2}, {3}, {16}, {17}, {18}, {19}, {28}, {29}, {30}, {31}, {24}, {25}, {26}, {27}, {12}, {13}, {14}, {15}, {20}, {21}, {22}, {23}, {4}, {5}, {6}, {7}},
        // round 15
        {{32}, {33}, {34}, {35}, {36}, {37}, {38}, {39}, {40}, {41}, {42}, {43}, {44}, {45}, {46}, {47}, {48}, {49}, {50}, {51}, {52}, {53}, {54}, {55}, {56}, {57}, {58}, {59}, {60}, {61}, {62}, {63}},
        // round 16
        {{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}, {16}, {17}, {18}, {19}, {20}, {21}, {22}, {23}, {24}, {25}, {26}, {27}, {28}, {29}, {30}, {31}},
        // round 17
        {{36}, {37}, {38}, {39}, {60}, {61}, {62}, {63}, {32}, {33}, {34}, {35}, {52}, {53}, {54}, {55}, {40}, {41}, {42}, {43}, {56}, {57}, {58}, {59}, {48}, {49}, {50}, {51}, {44}, {45}, {46}, {47}},
        // round 18
        {{4}, {5}, {6}, {7}, {28}, {29}, {30}, {31}, {0}, {1}, {2}, {3}, {20}, {21}, {22}, {23}, {8}, {9}, {10}, {11}, {24}, {25}, {26}, {27}, {16}, {17}, {18}, {19}, {12}, {13}, {14}, {15}},
        // round 19
        {{60}, {61}, {62}, {63}, {44}, {45}, {46}, {47}, {36}, {37}, {38}, {39}, {56}, {57}, {58}, {59}, {32}, {33}, {34}, {35}, {48}, {49}, {50}, {51}, {40}, {41}, {42}, {43}, {52}, {53}, {54}, {55}},
        // round 20
        {{28}, {29}, {30}, {31}, {12}, {13}, {14}, {15}, {4}, {5}, {6}, {7}, {24}, {25}, {26}, {27}, {0}, {1}, {2}, {3}, {16}, {17}, {18}, {19}, {8}, {9}, {10}, {11}, {20}, {21}, {22}, {23}},
        // round 21
        {{44}, {45}, {46}, {47}, {52}, {53}, {54}, {55}, {60}, {61}, {62}, {63}, {48}, {49}, {50}, {51}, {36}, {37}, {38}, {39}, {40}, {41}, {42}, {43}, {32}, {33}, {34}, {35}, {56}, {57}, {58}, {59}},
        // round 22
        {{12}, {13}, {14}, {15}, {20}, {21}, {22}, {23}, {28}, {29}, {30}, {31}, {16}, {17}, {18}, {19}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {0}, {1}, {2}, {3}, {24}, {25}, {26}, {27}},


	};

	public static int[][][] tk2s_64 = new int[][][] {
		// round 0
        {{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}, {16}, {17}, {18}, {19}, {20},
         {21}, {22}, {23}, {24}, {25}, {26}, {27}, {28}, {29}, {30}, {31}},
        // round 1
        {{38, 39}, {36}, {37}, {38}, {62, 63}, {60}, {61}, {62}, {34, 35}, {32}, {33}, {34}, {54, 55}, {52}, {53}, {54},
         {42, 43}, {40}, {41}, {42}, {58, 59}, {56}, {57}, {58}, {50, 51}, {48}, {49}, {50}, {46, 47}, {44}, {45}, {46}},
        // round 2
        {{6, 7}, {4}, {5}, {6}, {30, 31}, {28}, {29}, {30}, {2, 3}, {0}, {1}, {2}, {22, 23}, {20}, {21}, {22}, {10, 11},
         {8}, {9}, {10}, {26, 27}, {24}, {25}, {26}, {18, 19}, {16}, {17}, {18}, {14, 15}, {12}, {13}, {14}},
        // round 3
        {{61, 62}, {62, 63}, {60}, {61}, {45, 46}, {46, 47}, {44}, {45}, {37, 38}, {38, 39}, {36}, {37}, {57, 58}, {58, 59},
         {56}, {57}, {33, 34}, {34, 35}, {32}, {33}, {49, 50}, {50, 51}, {48}, {49}, {41, 42}, {42, 43}, {40}, {41},
         {53, 54}, {54, 55}, {52}, {53}},
        // round 4
        {{29, 30}, {30, 31}, {28}, {29}, {13, 14}, {14, 15}, {12}, {13}, {5, 6}, {6, 7}, {4}, {5}, {25, 26}, {26, 27}, {24},
         {25}, {1, 2}, {2, 3}, {0}, {1}, {17, 18}, {18, 19}, {16}, {17}, {9, 10}, {10, 11}, {8}, {9}, {21, 22}, {22, 23},
         {20}, {21}},
        // round 5
        {{44, 45}, {45, 46}, {46, 47}, {44}, {52, 53}, {53, 54}, {54, 55}, {52}, {60, 61}, {61, 62}, {62, 63}, {60},
         {48, 49}, {49, 50}, {50, 51}, {48}, {36, 37}, {37, 38}, {38, 39}, {36}, {40, 41}, {41, 42}, {42, 43}, {40},
         {32, 33}, {33, 34}, {34, 35}, {32}, {56, 57}, {57, 58}, {58, 59}, {56}},
        // round 6
        {{12, 13}, {13, 14}, {14, 15}, {12}, {20, 21}, {21, 22}, {22, 23}, {20}, {28, 29}, {29, 30}, {30, 31}, {28},
         {16, 17}, {17, 18}, {18, 19}, {16}, {4, 5}, {5, 6}, {6, 7}, {4}, {8, 9}, {9, 10}, {10, 11}, {8}, {0, 1}, {1, 2},
         {2, 3}, {0}, {24, 25}, {25, 26}, {26, 27}, {24}},
        // round 7
        {{54, 55, 52}, {52, 53}, {53, 54}, {54, 55}, {58, 59, 56}, {56, 57}, {57, 58}, {58, 59}, {46, 47, 44}, {44, 45},
         {45, 46}, {46, 47}, {42, 43, 40}, {40, 41}, {41, 42}, {42, 43}, {62, 63, 60}, {60, 61}, {61, 62}, {62, 63},
         {34, 35, 32}, {32, 33}, {33, 34}, {34, 35}, {38, 39, 36}, {36, 37}, {37, 38}, {38, 39}, {50, 51, 48}, {48, 49},
         {49, 50}, {50, 51}},
        // round 8
        {{22, 23, 20}, {20, 21}, {21, 22}, {22, 23}, {26, 27, 24}, {24, 25}, {25, 26}, {26, 27}, {14, 15, 12}, {12, 13},
         {13, 14}, {14, 15}, {10, 11, 8}, {8, 9}, {9, 10}, {10, 11}, {30, 31, 28}, {28, 29}, {29, 30}, {30, 31}, {2, 3, 0},
         {0, 1}, {1, 2}, {2, 3}, {6, 7, 4}, {4, 5}, {5, 6}, {6, 7}, {18, 19, 16}, {16, 17}, {17, 18}, {18, 19}},
        // round 9
        {{57, 58, 58, 59}, {58, 59, 56}, {56, 57}, {57, 58}, {49, 50, 50, 51}, {50, 51, 48}, {48, 49}, {49, 50}, {53, 54, 54, 55}, {54, 55, 52}, {52, 53}, {53, 54}, {33, 34, 34, 35}, {34, 35, 32}, {32, 33}, {33, 34}, {45, 46, 46, 47}, {46, 47, 44}, {44, 45}, {45, 46}, {37, 38, 38, 39}, {38, 39, 36}, {36, 37}, {37, 38}, {61, 62, 62, 63}, {62, 63, 60}, {60, 61}, {61, 62}, {41, 42, 42, 43}, {42, 43, 40}, {40, 41}, {41, 42}},
        // round 10
        {{25, 26, 26, 27}, {26, 27, 24}, {24, 25}, {25, 26}, {17, 18, 18, 19}, {18, 19, 16}, {16, 17}, {17, 18}, {21, 22, 22, 23}, {22, 23, 20}, {20, 21}, {21, 22}, {1, 2, 2, 3}, {2, 3, 0}, {0, 1}, {1, 2}, {13, 14, 14, 15}, {14, 15, 12}, {12, 13}, {13, 14}, {5, 6, 6, 7}, {6, 7, 4}, {4, 5}, {5, 6}, {29, 30, 30, 31}, {30, 31, 28}, {28, 29}, {29, 30}, {9, 10, 10, 11}, {10, 11, 8}, {8, 9}, {9, 10}},
        // round 11
        {{48, 49, 49, 50}, {49, 50, 50, 51}, {50, 51, 48}, {48, 49}, {40, 41, 41, 42}, {41, 42, 42, 43}, {42, 43, 40}, {40, 41}, {56, 57, 57, 58}, {57, 58, 58, 59}, {58, 59, 56}, {56, 57}, {36, 37, 37, 38}, {37, 38, 38, 39}, {38, 39, 36}, {36, 37}, {52, 53, 53, 54}, {53, 54, 54, 55}, {54, 55, 52}, {52, 53}, {60, 61, 61, 62}, {61, 62, 62, 63}, {62, 63, 60}, {60, 61}, {44, 45, 45, 46}, {45, 46, 46, 47}, {46, 47, 44}, {44, 45}, {32, 33, 33, 34}, {33, 34, 34, 35}, {34, 35, 32}, {32, 33}},
        // round 12
        {{16, 17, 17, 18}, {17, 18, 18, 19}, {18, 19, 16}, {16, 17}, {8, 9, 9, 10}, {9, 10, 10, 11}, {10, 11, 8}, {8, 9},{24, 25, 25, 26}, {25, 26, 26, 27}, {26, 27, 24}, {24, 25}, {4, 5, 5, 6}, {5, 6, 6, 7}, {6, 7, 4}, {4, 5},{20, 21, 21, 22}, {21, 22, 22, 23}, {22, 23, 20}, {20, 21}, {28, 29, 29, 30}, {29, 30, 30, 31}, {30, 31, 28},{28, 29}, {12, 13, 13, 14}, {13, 14, 14, 15}, {14, 15, 12}, {12, 13}, {0, 1, 1, 2}, {1, 2, 2, 3}, {2, 3, 0},{0, 1}},
        // round 13
        {{42, 43, 40, 40, 41}, {40, 41, 41, 42}, {41, 42, 42, 43}, {42, 43, 40}, {34, 35, 32, 32, 33}, {32, 33, 33, 34},{33, 34, 34, 35}, {34, 35, 32}, {50, 51, 48, 48, 49}, {48, 49, 49, 50}, {49, 50, 50, 51}, {50, 51, 48},{62, 63, 60, 60, 61}, {60, 61, 61, 62}, {61, 62, 62, 63}, {62, 63, 60}, {58, 59, 56, 56, 57}, {56, 57, 57, 58},{57, 58, 58, 59}, {58, 59, 56}, {46, 47, 44, 44, 45}, {44, 45, 45, 46}, {45, 46, 46, 47}, {46, 47, 44},{54, 55, 52, 52, 53}, {52, 53, 53, 54}, {53, 54, 54, 55}, {54, 55, 52}, {38, 39, 36, 36, 37}, {36, 37, 37, 38},{37, 38, 38, 39}, {38, 39, 36}},
        // round 14
        {{10, 11, 8, 8, 9}, {8, 9, 9, 10}, {9, 10, 10, 11}, {10, 11, 8}, {2, 3, 0, 0, 1}, {0, 1, 1, 2}, {1, 2, 2, 3},{2, 3, 0}, {18, 19, 16, 16, 17}, {16, 17, 17, 18}, {17, 18, 18, 19}, {18, 19, 16}, {30, 31, 28, 28, 29},{28, 29, 29, 30}, {29, 30, 30, 31}, {30, 31, 28}, {26, 27, 24, 24, 25}, {24, 25, 25, 26}, {25, 26, 26, 27},{26, 27, 24}, {14, 15, 12, 12, 13}, {12, 13, 13, 14}, {13, 14, 14, 15}, {14, 15, 12}, {22, 23, 20, 20, 21},{20, 21, 21, 22}, {21, 22, 22, 23}, {22, 23, 20}, {6, 7, 4, 4, 5}, {4, 5, 5, 6}, {5, 6, 6, 7}, {6, 7, 4}},
        // round 15
        {{33, 34, 34, 35, 34, 35, 32}, {34, 35, 32, 32, 33}, {32, 33, 33, 34}, {33, 34, 34, 35},{37, 38, 38, 39, 38, 39, 36}, {38, 39, 36, 36, 37}, {36, 37, 37, 38}, {37, 38, 38, 39},{41, 42, 42, 43, 42, 43, 40}, {42, 43, 40, 40, 41}, {40, 41, 41, 42}, {41, 42, 42, 43},{45, 46, 46, 47, 46, 47, 44}, {46, 47, 44, 44, 45}, {44, 45, 45, 46}, {45, 46, 46, 47},{49, 50, 50, 51, 50, 51, 48}, {50, 51, 48, 48, 49}, {48, 49, 49, 50}, {49, 50, 50, 51},{53, 54, 54, 55, 54, 55, 52}, {54, 55, 52, 52, 53}, {52, 53, 53, 54}, {53, 54, 54, 55},{57, 58, 58, 59, 58, 59, 56}, {58, 59, 56, 56, 57}, {56, 57, 57, 58}, {57, 58, 58, 59},{61, 62, 62, 63, 62, 63, 60}, {62, 63, 60, 60, 61}, {60, 61, 61, 62}, {61, 62, 62, 63}},
        // round 16
        {{1, 2, 2, 3, 2, 3, 0}, {2, 3, 0, 0, 1}, {0, 1, 1, 2}, {1, 2, 2, 3}, {5, 6, 6, 7, 6, 7, 4}, {6, 7, 4, 4, 5},{4, 5, 5, 6}, {5, 6, 6, 7}, {9, 10, 10, 11, 10, 11, 8}, {10, 11, 8, 8, 9}, {8, 9, 9, 10}, {9, 10, 10, 11},{13, 14, 14, 15, 14, 15, 12}, {14, 15, 12, 12, 13}, {12, 13, 13, 14}, {13, 14, 14, 15},{17, 18, 18, 19, 18, 19, 16}, {18, 19, 16, 16, 17}, {16, 17, 17, 18}, {17, 18, 18, 19},{21, 22, 22, 23, 22, 23, 20}, {22, 23, 20, 20, 21}, {20, 21, 21, 22}, {21, 22, 22, 23},{25, 26, 26, 27, 26, 27, 24}, {26, 27, 24, 24, 25}, {24, 25, 25, 26}, {25, 26, 26, 27},{29, 30, 30, 31, 30, 31, 28}, {30, 31, 28, 28, 29}, {28, 29, 29, 30}, {29, 30, 30, 31}},
        // round 17
        {{36, 37, 37, 38, 37, 38, 38, 39}, {37, 38, 38, 39, 38, 39, 36}, {38, 39, 36, 36, 37}, {36, 37, 37, 38},{60, 61, 61, 62, 61, 62, 62, 63}, {61, 62, 62, 63, 62, 63, 60}, {62, 63, 60, 60, 61}, {60, 61, 61, 62},{32, 33, 33, 34, 33, 34, 34, 35}, {33, 34, 34, 35, 34, 35, 32}, {34, 35, 32, 32, 33}, {32, 33, 33, 34},{52, 53, 53, 54, 53, 54, 54, 55}, {53, 54, 54, 55, 54, 55, 52}, {54, 55, 52, 52, 53}, {52, 53, 53, 54},{40, 41, 41, 42, 41, 42, 42, 43}, {41, 42, 42, 43, 42, 43, 40}, {42, 43, 40, 40, 41}, {40, 41, 41, 42},{56, 57, 57, 58, 57, 58, 58, 59}, {57, 58, 58, 59, 58, 59, 56}, {58, 59, 56, 56, 57}, {56, 57, 57, 58},{48, 49, 49, 50, 49, 50, 50, 51}, {49, 50, 50, 51, 50, 51, 48}, {50, 51, 48, 48, 49}, {48, 49, 49, 50},{44, 45, 45, 46, 45, 46, 46, 47}, {45, 46, 46, 47, 46, 47, 44}, {46, 47, 44, 44, 45}, {44, 45, 45, 46}},
        // round 18
        {{4, 5, 5, 6, 5, 6, 6, 7}, {5, 6, 6, 7, 6, 7, 4}, {6, 7, 4, 4, 5}, {4, 5, 5, 6}, {28, 29, 29, 30, 29, 30, 30, 31},{29, 30, 30, 31, 30, 31, 28}, {30, 31, 28, 28, 29}, {28, 29, 29, 30}, {0, 1, 1, 2, 1, 2, 2, 3},{1, 2, 2, 3, 2, 3, 0}, {2, 3, 0, 0, 1}, {0, 1, 1, 2}, {20, 21, 21, 22, 21, 22, 22, 23},{21, 22, 22, 23, 22, 23, 20}, {22, 23, 20, 20, 21}, {20, 21, 21, 22}, {8, 9, 9, 10, 9, 10, 10, 11},{9, 10, 10, 11, 10, 11, 8}, {10, 11, 8, 8, 9}, {8, 9, 9, 10}, {24, 25, 25, 26, 25, 26, 26, 27},{25, 26, 26, 27, 26, 27, 24}, {26, 27, 24, 24, 25}, {24, 25, 25, 26}, {16, 17, 17, 18, 17, 18, 18, 19},{17, 18, 18, 19, 18, 19, 16}, {18, 19, 16, 16, 17}, {16, 17, 17, 18}, {12, 13, 13, 14, 13, 14, 14, 15},{13, 14, 14, 15, 14, 15, 12}, {14, 15, 12, 12, 13}, {12, 13, 13, 14}},
        // round 19
        {{62, 63, 60, 60, 61, 60, 61, 61, 62}, {60, 61, 61, 62, 61, 62, 62, 63}, {61, 62, 62, 63, 62, 63, 60},{62, 63, 60, 60, 61}, {46, 47, 44, 44, 45, 44, 45, 45, 46}, {44, 45, 45, 46, 45, 46, 46, 47},{45, 46, 46, 47, 46, 47, 44}, {46, 47, 44, 44, 45}, {38, 39, 36, 36, 37, 36, 37, 37, 38},{36, 37, 37, 38, 37, 38, 38, 39}, {37, 38, 38, 39, 38, 39, 36}, {38, 39, 36, 36, 37},{58, 59, 56, 56, 57, 56, 57, 57, 58}, {56, 57, 57, 58, 57, 58, 58, 59}, {57, 58, 58, 59, 58, 59, 56},{58, 59, 56, 56, 57}, {34, 35, 32, 32, 33, 32, 33, 33, 34}, {32, 33, 33, 34, 33, 34, 34, 35},{33, 34, 34, 35, 34, 35, 32}, {34, 35, 32, 32, 33}, {50, 51, 48, 48, 49, 48, 49, 49, 50},{48, 49, 49, 50, 49, 50, 50, 51}, {49, 50, 50, 51, 50, 51, 48}, {50, 51, 48, 48, 49},{42, 43, 40, 40, 41, 40, 41, 41, 42}, {40, 41, 41, 42, 41, 42, 42, 43}, {41, 42, 42, 43, 42, 43, 40},{42, 43, 40, 40, 41}, {54, 55, 52, 52, 53, 52, 53, 53, 54}, {52, 53, 53, 54, 53, 54, 54, 55},{53, 54, 54, 55, 54, 55, 52}, {54, 55, 52, 52, 53}},
        // round 20
        {{30, 31, 28, 28, 29, 28, 29, 29, 30}, {28, 29, 29, 30, 29, 30, 30, 31}, {29, 30, 30, 31, 30, 31, 28},{30, 31, 28, 28, 29}, {14, 15, 12, 12, 13, 12, 13, 13, 14}, {12, 13, 13, 14, 13, 14, 14, 15},{13, 14, 14, 15, 14, 15, 12}, {14, 15, 12, 12, 13}, {6, 7, 4, 4, 5, 4, 5, 5, 6}, {4, 5, 5, 6, 5, 6, 6, 7},{5, 6, 6, 7, 6, 7, 4}, {6, 7, 4, 4, 5}, {26, 27, 24, 24, 25, 24, 25, 25, 26}, {24, 25, 25, 26, 25, 26, 26, 27},{25, 26, 26, 27, 26, 27, 24}, {26, 27, 24, 24, 25}, {2, 3, 0, 0, 1, 0, 1, 1, 2}, {0, 1, 1, 2, 1, 2, 2, 3},{1, 2, 2, 3, 2, 3, 0}, {2, 3, 0, 0, 1}, {18, 19, 16, 16, 17, 16, 17, 17, 18}, {16, 17, 17, 18, 17, 18, 18, 19},{17, 18, 18, 19, 18, 19, 16}, {18, 19, 16, 16, 17}, {10, 11, 8, 8, 9, 8, 9, 9, 10}, {8, 9, 9, 10, 9, 10, 10, 11},{9, 10, 10, 11, 10, 11, 8}, {10, 11, 8, 8, 9}, {22, 23, 20, 20, 21, 20, 21, 21, 22},{20, 21, 21, 22, 21, 22, 22, 23}, {21, 22, 22, 23, 22, 23, 20}, {22, 23, 20, 20, 21}},
        // round 21
        {{45, 46, 46, 47, 46, 47, 44, 46, 47, 44, 44, 45}, {46, 47, 44, 44, 45, 44, 45, 45, 46},{44, 45, 45, 46, 45, 46, 46, 47}, {45, 46, 46, 47, 46, 47, 44}, {53, 54, 54, 55, 54, 55, 52, 54, 55, 52, 52, 53},{54, 55, 52, 52, 53, 52, 53, 53, 54}, {52, 53, 53, 54, 53, 54, 54, 55}, {53, 54, 54, 55, 54, 55, 52},{61, 62, 62, 63, 62, 63, 60, 62, 63, 60, 60, 61}, {62, 63, 60, 60, 61, 60, 61, 61, 62},{60, 61, 61, 62, 61, 62, 62, 63}, {61, 62, 62, 63, 62, 63, 60}, {49, 50, 50, 51, 50, 51, 48, 50, 51, 48, 48, 49},{50, 51, 48, 48, 49, 48, 49, 49, 50}, {48, 49, 49, 50, 49, 50, 50, 51}, {49, 50, 50, 51, 50, 51, 48},{37, 38, 38, 39, 38, 39, 36, 38, 39, 36, 36, 37}, {38, 39, 36, 36, 37, 36, 37, 37, 38},{36, 37, 37, 38, 37, 38, 38, 39}, {37, 38, 38, 39, 38, 39, 36}, {41, 42, 42, 43, 42, 43, 40, 42, 43, 40, 40, 41},{42, 43, 40, 40, 41, 40, 41, 41, 42}, {40, 41, 41, 42, 41, 42, 42, 43}, {41, 42, 42, 43, 42, 43, 40},{33, 34, 34, 35, 34, 35, 32, 34, 35, 32, 32, 33}, {34, 35, 32, 32, 33, 32, 33, 33, 34},{32, 33, 33, 34, 33, 34, 34, 35}, {33, 34, 34, 35, 34, 35, 32}, {57, 58, 58, 59, 58, 59, 56, 58, 59, 56, 56, 57},{58, 59, 56, 56, 57, 56, 57, 57, 58}, {56, 57, 57, 58, 57, 58, 58, 59}, {57, 58, 58, 59, 58, 59, 56}},
        // round 22
        {{13, 14, 14, 15, 14, 15, 12, 14, 15, 12, 12, 13}, {14, 15, 12, 12, 13, 12, 13, 13, 14},{12, 13, 13, 14, 13, 14, 14, 15}, {13, 14, 14, 15, 14, 15, 12}, {21, 22, 22, 23, 22, 23, 20, 22, 23, 20, 20, 21},{22, 23, 20, 20, 21, 20, 21, 21, 22}, {20, 21, 21, 22, 21, 22, 22, 23}, {21, 22, 22, 23, 22, 23, 20},{29, 30, 30, 31, 30, 31, 28, 30, 31, 28, 28, 29}, {30, 31, 28, 28, 29, 28, 29, 29, 30},{28, 29, 29, 30, 29, 30, 30, 31}, {29, 30, 30, 31, 30, 31, 28}, {17, 18, 18, 19, 18, 19, 16, 18, 19, 16, 16, 17},{18, 19, 16, 16, 17, 16, 17, 17, 18}, {16, 17, 17, 18, 17, 18, 18, 19}, {17, 18, 18, 19, 18, 19, 16},{5, 6, 6, 7, 6, 7, 4, 6, 7, 4, 4, 5}, {6, 7, 4, 4, 5, 4, 5, 5, 6}, {4, 5, 5, 6, 5, 6, 6, 7}, {5, 6, 6, 7, 6, 7, 4},{9, 10, 10, 11, 10, 11, 8, 10, 11, 8, 8, 9}, {10, 11, 8, 8, 9, 8, 9, 9, 10}, {8, 9, 9, 10, 9, 10, 10, 11},{9, 10, 10, 11, 10, 11, 8}, {1, 2, 2, 3, 2, 3, 0, 2, 3, 0, 0, 1}, {2, 3, 0, 0, 1, 0, 1, 1, 2},{0, 1, 1, 2, 1, 2, 2, 3}, {1, 2, 2, 3, 2, 3, 0}, {25, 26, 26, 27, 26, 27, 24, 26, 27, 24, 24, 25},{26, 27, 24, 24, 25, 24, 25, 25, 26}, {24, 25, 25, 26, 25, 26, 26, 27}, {25, 26, 26, 27, 26, 27, 24}},


	};
	
}
