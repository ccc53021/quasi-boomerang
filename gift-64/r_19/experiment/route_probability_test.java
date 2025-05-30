package quasidifferential.boomerang.gift_64.experiment;

import java.util.Arrays;
import java.util.Random;

public class route_probability_test2 {

	public static void main(String[] args) {
		// TODO Auto-generated method stub

		long start = System.currentTimeMillis();

		int[] sbox_inverse = get_inverse_box(sbox, n, m);

		System.out.println("-------------------- begining -----------------------");

		int number = 3;

		int encrypt_round = 19;

		int upper_round_upper = 9;
		int[] upper_input_difference = get_a_characteristic_1d_by_str("0x000000a000006000");
		int[] upper_output_difference = get_a_characteristic_1d_by_str("0x0100000001020200");

		int em_begin_round = 9;
		int em_round_upper = 1;
		int em_round_lower = 1;
		int[] em_input_difference = get_a_characteristic_1d_by_str("0x0100000001020200");
		int[] em_output_difference = get_a_characteristic_1d_by_str("0x0a00000000000000");

		int lower_begin_round = 9 + 1 + 1;
		int lower_round_lower = 8;
		int[] lower_input_difference = get_a_characteristic_1d_by_str("0x0a00000000000000");
		int[] lower_output_difference = get_a_characteristic_1d_by_str("0x0800000000000010");

		int[][][][] k_constraints = new int[][][][] {};
		int[] k_values = new int[] {};

		System.out.println("-------------------- generating initial tks --------------------------");
		int[][] k_1 = get_initial_random_k_by_given_constraints(k_constraints, k_values);

		System.out.println("-------------------- generating tks --------------------------");
		String difference_k_delta_1 = "0x00000000000000020000000001004000";
		String difference_k_delta_2 = "0x00000008000000020000010000000000";
//		String difference_k_delta_1 = "0x01000010000000000200000000000000";
//		String difference_k_delta_2 = "0x04000000200000000000000000100000";
		int[][] k_2 = get_a_random_master_key_2d(get_another_key_by_k_and_difference_128(get_a_key_difference_1d_128(difference_k_delta_1), get_a_random_master_key_1d(k_1)));
		int[][] k_3 = get_a_random_master_key_2d(get_another_key_by_k_and_difference_128(get_a_key_difference_1d_128(difference_k_delta_2), get_a_random_master_key_1d(k_1)));
		int[][] k_4 = get_a_random_master_key_2d(get_another_key_by_k_and_difference_128(get_a_difference_by_two_states(get_a_key_difference_1d_128(difference_k_delta_1), get_a_key_difference_1d_128(difference_k_delta_2)), get_a_random_master_key_1d(k_1)));

		System.out.println("--------------- generating rks ---------------------");
		int[][][] round_keys_1 = key_algorithm_64(k_1, encrypt_round);
		int[][][] round_keys_2 = key_algorithm_64(k_2, encrypt_round);
		int[][][] round_keys_3 = key_algorithm_64(k_3, encrypt_round);
		int[][][] round_keys_4 = key_algorithm_64(k_4, encrypt_round);

		int[][][][] round_keys = new int[4][][][];
		round_keys[0] = round_keys_1;
		round_keys[1] = round_keys_2;
		round_keys[2] = round_keys_3;
		round_keys[3] = round_keys_4;

		System.out.println("------------------------ experiment ------------------");
		// p = 2^-28.0 * 1 = 2^-28.0, p_e = 2^-28.02
		int upper_experiment_time = (int) Math.pow(2, 30);
		// p = 0.0546875 = 2^-4.192645077942396, p_e = 2^-3.43
		int em_experiment_time = (int) Math.pow(2, 16);
		// p = 2^-22.0 * 1 = 2^-22.0, p_e = 2^-21.94
		int lower_experiment_time = (int) Math.pow(2, 25);
		one_experiment_amplified_upper(upper_input_difference, upper_output_difference, number, upper_experiment_time, sbox, sbox_inverse, round_keys, upper_round_upper);
		one_experiment_amplified_em(em_input_difference, em_output_difference, number, em_experiment_time, sbox, sbox_inverse, round_keys, em_begin_round, em_round_upper, em_round_lower);
		one_experiment_amplified_lower(lower_input_difference, lower_output_difference, number, lower_experiment_time, sbox, sbox_inverse, round_keys, lower_begin_round, lower_round_lower);

		long end = System.currentTimeMillis();
		System.out.println("run time is : " + (double) (end - start) / 1000 + "s");

	}

	public static int[] GIFT_64_SBOX = {0x1, 0xa, 0x4, 0xc, 0x6, 0xf, 0x3, 0x9, 0x2, 0xd, 0xb, 0x7, 0x5, 0x0, 0x8, 0xe};
	public static int n = 4;
	public static int m = 4;
	public static int[] sbox = GIFT_64_SBOX;
	public static int state_bits = 64;
	public static int state_words = 16;
	public static int sbox_bits = 4;

	public static int [] round_constants = {0x01, 0x03, 0x07, 0x0F, 0x1F, 0x3E, 0x3D, 0x3B, 0x37, 0x2F, 0x1E, 0x3C, 0x39, 0x33, 0x27, 0x0E, 0x1D, 0x3A, 0x35, 0x2B, 0x16, 0x2C, 0x18, 0x30, 0x21, 0x02, 0x05, 0x0B, 0x17, 0x2E, 0x1C, 0x38};
	public static int[] round_constant_positions = {3, 7, 11, 15, 19, 23};

	public static int[] permutation_bits_table_64 = {
		    0, 5, 10, 15, 16, 21, 26, 31, 32, 37, 42, 47, 48, 53, 58, 63,
		    12, 1, 6, 11, 28, 17, 22, 27, 44, 33, 38, 43, 60, 49, 54, 59,
		    8, 13, 2, 7, 24, 29, 18, 23, 40, 45, 34, 39, 56, 61, 50, 55,
		    4, 9, 14, 3, 20, 25, 30, 19, 36, 41, 46, 35, 52, 57, 62, 51
		};

	public static int[] get_inverse_box(int[] box, int n, int m) {
		int[] inverse_box = new int[(int) Math.pow(2, n)];
		for(int i = 0; i < inverse_box.length; i++) {
			inverse_box[box[i]] = i;
		}

		return inverse_box;
	}

	public static int[] permute_bits(int[] x) {
	    int[] y = new int[x.length];
	    for (int i = 0; i < state_bits; i++) {
	        y[i] = x[permutation_bits_table_64[i]];
	    }

	    return y;
	}

	public static int[] permute_bits_inverse(int[] x) {
	    int[] y = new int[x.length];
	    for (int i = 0; i < state_bits; i++) {
	        y[permutation_bits_table_64[i]] = x[i];
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

	public static int[] add_round_constants(int[] x, int c) {
	    int[] y = new int[x.length];
	    for (int i = 0; i < x.length; i++) {
	    	y[i] = x[i];
	    }
	    y[state_bits - 1] ^= 1;
	    for (int i = 0; i < 6; i++) {
	        y[round_constant_positions[i]] = y[round_constant_positions[i]] ^ ((c >> i) & 0x1);
	    }

	    return y;
	}

	public static int[] add_round_key_64(int[] x, int[][] rk) {
		int[] y = new int[x.length];
	    for (int i = 0; i < x.length; i++) {
	    	y[i] = x[i];
	    }
	    int ii = rk[0].length;
	    // print(ii)
	    for (int i = 0; i < ii; i++) {
	        y[4 * i + 1] = y[4 * i + 1] ^ rk[1][i];
	        y[4 * i] = y[4 * i] ^ rk[0][i];
	    }

	    return y;
	}

	public static int[][] get_initial_random_k_by_given_constraints(int[][][][] constraints, int[] values) {
		int[][] initial_k = new int[8][16];

		Random rd = new Random();

		int flag_t = 0;
		while (flag_t == 0) {

			for(int i = 0; i < 8; i++) {
				for(int j = 0; j < 16; j++) {
					initial_k[i][j] = rd.nextInt(2);
				}
			}

			int count_t = 0;
			for(int i = 0; i < constraints.length; i++) {
				int[][] one_constraint_k = constraints[i][0];
				int one_value = values[i];
				int temp = 0;
				for(int ii = 0; ii < one_constraint_k.length; ii++) {
					int[] kk = one_constraint_k[ii];
					temp ^= initial_k[kk[0]][kk[1]];
				}
				if (temp == one_value) {
					count_t += 1;
				}
			}

			if (count_t == constraints.length) {
				flag_t = 1;
			}

		}

		return initial_k;
	}

	public static int[][] get_a_random_master_key() {
		Random rd = new Random();
	    int[][] master_key = new int[8][];
	    for (int i = 0; i < 8; i++) {
	        int[] l = new int[16];
	        for (int j = 0; j < 16; j++) {
	            l[j] = rd.nextInt(2);
	        }
	        master_key[i] = l;
	    }

	    return master_key;
	}

	public static int[] get_a_random_master_key_1d(int[][] mk) {
	    int[] master_key = new int[128];
	    for (int i = 0; i < 8; i++) {
	        for (int j = 0; j < 16; j++) {
	            master_key[16 * i + j] = mk[i][j];
	        }
	    }

	    return master_key;
	}

	public static int[] get_another_key_by_k_and_difference_128(int[] input_difference_1d, int[] one_key_1d) {
		int[] k1 = new int[128];
		for(int i = 0; i < 128; i++) {
			k1[i] = one_key_1d[i] ^ input_difference_1d[i];
		}

		return k1;
	};

	public static int[][] get_a_random_master_key_2d(int[] mk) {
		int[][] master_key = new int[8][];
	    for (int i = 0; i < 8; i++) {
	        int[] l = new int[16];
	        for (int j = 0; j < 16; j++) {
	            l[j] = mk[i * 16 + j];
	        }
	        master_key[i] = l;
	    }

	    return master_key;
	};

	public static int[][][] key_algorithm_64(int[][] master_key, int round) {
	    int[][][] keys = new int[round][8][16];
	    keys[0] = master_key;
	    for (int r = 1; r < round; r++) {
	        int[][] last_key = keys[r - 1];
	        int[][] new_key = new int[8][16];
	        new_key[0] = last_key[2];
	        new_key[1] = last_key[3];
	        new_key[2] = last_key[4];
	        new_key[3] = last_key[5];
	        new_key[4] = last_key[6];
	        new_key[5] = last_key[7];
	        int[] k0_rot_r_12 = new int[16];
	        for (int p = 12; p < 16; p++) {
	        	k0_rot_r_12[p - 12] = last_key[0][p];
	        }
	        for(int p = 0; p < 12; p++) {
	        	k0_rot_r_12[p + 4] = last_key[0][p];
	        }
	        new_key[6] = k0_rot_r_12;
	        int[] k1_rot_r_2 = new int[16];
	        for(int p = 2; p < 16; p++) {
	        	k1_rot_r_2[p - 2] = last_key[1][p];
	        }
	        for(int p = 0; p < 2; p++) {
	        	k1_rot_r_2[p + 14] = last_key[1][p];
	        }
	        new_key[7] = k1_rot_r_2;
	        keys[r] = new_key;
	    }

	    int[][][] round_keys = new int[round][2][16];
	    for (int r = 0; r < round; r++) {
	        int[][] one_round_key = new int[2][16];
	        one_round_key[0] = keys[r][0];
	        one_round_key[1] = keys[r][1];
	        round_keys[r] = one_round_key;
	    }

	    return round_keys;
	}

	public static int[][] get_an_random_plaintext_and_another_by_difference(int[] input_difference) {
		int[] x = new int[input_difference.length];
		int[] x1 = new int[input_difference.length];
		Random rd = new Random();
		for(int i = 0; i < input_difference.length; i++) {
			x[i] = rd.nextInt(2);
			x1[i] = x[i] ^ input_difference[i];
		}

		int[][] x_and_x1 = new int[2][];
		x_and_x1[0] = x;
		x_and_x1[1] = x1;

		return x_and_x1;
	}

	public static int[] get_another_key_by_k_and_difference(int[] input_difference, int[] one_key) {

		int[] k1 = new int[input_difference.length];
		for(int i = 0; i < input_difference.length; i++) {
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

	public static int[] get_a_key_difference_1d_128(String difference) {
		int[] diff_1d = new int[128];
		String one_d_str = difference;
		one_d_str = one_d_str.substring(2);
		for(int j = 0; j < 32; j++) {
			String one_s_str = one_d_str.substring(32 - j - 1, 32 - j);
			int one_s = Integer.parseInt(one_s_str, 16);
			for(int k = 0; k < sbox_bits; k++) {
				diff_1d[k + j * sbox_bits] = (one_s >> k) & 0x1;
			}
		}

		return diff_1d;
	}

	public static int[] get_a_difference_by_two_states(int[] x, int[] x1) {
		int[] diff = new int[x.length];
		for(int i = 0; i < x.length; i++) {
			diff[i] = x[i] ^ x1[i];
		}

		return diff;
	}

	public static void one_experiment_amplified_upper(int[] input_difference, int[] output_difference, int number, int experiment_time, int[] sbox, int[] sbox_inverse, int[][][][] rks, int round_upper) {
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

				int[] diff_y_11 = get_a_difference_by_two_states(y, y1);
				int[] diff_y_22 = get_a_difference_by_two_states(y2, y3);

				if (Arrays.equals(diff_y_11, diff_y_22)) {
					// p
					y = permute_bits(y);
		            y1 = permute_bits(y1);
		            y2 = permute_bits(y2);
		            y3 = permute_bits(y3);

		            // k
		            int[][][] rk_1 = rks[0];
		            int[][][] rk_2 = rks[1];
		            y = add_round_key_64(y, rk_1[i]);
		            y1 = add_round_key_64(y1, rk_2[i]);
		            int[][][] rk_3 = rks[2];
		            int[][][] rk_4 = rks[3];
		            y2 = add_round_key_64(y2, rk_3[i]);
		            y3 = add_round_key_64(y3, rk_4[i]);

		            // ac
		            int c = round_constants[i];
		            y = add_round_constants(y, c);
		            y1 = add_round_constants(y1, c);
		            y2 = add_round_constants(y2, c);
		            y3 = add_round_constants(y3, c);
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

	public static void one_experiment_amplified_em(int[] input_difference, int[] output_difference, int number, int experiment_time, int[] sbox, int[] sbox_inverse, int[][][][] rks, int begin_round, int round_upper, int round_lower) {
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

				// p
				y = permute_bits(y);
	            y1 = permute_bits(y1);

	            // k
	            int[][][] rk_1 = rks[0];
	            int[][][] rk_2 = rks[1];
	            y = add_round_key_64(y, rk_1[i + begin_round]);
	            y1 = add_round_key_64(y1, rk_2[i + begin_round]);

	            // ac
	            int c = round_constants[i + begin_round];
	            y = add_round_constants(y, c);
	            y1 = add_round_constants(y1, c);
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
				// ac-1
	            int c = round_constants[i + begin_round];
	            y2 = add_round_constants(y2, c);
	            y3 = add_round_constants(y3, c);

	            // k-1
	            int[][][] rk_3 = rks[2];
	            int[][][] rk_4 = rks[3];
	            y2 = add_round_key_64(y2, rk_3[i + begin_round]);
	            y3 = add_round_key_64(y3, rk_4[i + begin_round]);

	            // p-1
	            y2 = permute_bits_inverse(y2);
	            y3 = permute_bits_inverse(y3);

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

	public static void one_experiment_amplified_lower(int[] input_difference, int[] output_difference, int number, int experiment_time, int[] sbox, int[] sbox_inverse, int[][][][] rks, int begin_round, int round_lower) {
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
					// p
					y = permute_bits(y);
		            y1 = permute_bits(y1);
		            y2 = permute_bits(y2);
		            y3 = permute_bits(y3);

		            // k
		            int[][][] rk_1 = rks[0];
		            int[][][] rk_3 = rks[2];
		            y = add_round_key_64(y, rk_1[i + begin_round]);
		            y1 = add_round_key_64(y1, rk_3[i + begin_round]);
		            int[][][] rk_2 = rks[1];
		            int[][][] rk_4 = rks[3];
		            y2 = add_round_key_64(y2, rk_2[i + begin_round]);
		            y3 = add_round_key_64(y3, rk_4[i + begin_round]);

		            // ac
		            int c = round_constants[i + begin_round];
		            y = add_round_constants(y, c);
		            y1 = add_round_constants(y1, c);
		            y2 = add_round_constants(y2, c);
		            y3 = add_round_constants(y3, c);
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
		System.out.println("lower: ");
		double index = Math.log10((double) count_rp / experiment_time) / Math.log10(2);;
		System.out.println("time " + experiment_time + ", right pairs : " + count_rp + ", p = " + (double) count_rp / experiment_time + " = 2^-" + -index);
		
	}
	
}
