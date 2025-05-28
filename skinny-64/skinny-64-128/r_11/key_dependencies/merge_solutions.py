# -*- coding: utf-8 -*-

output_file = "quasi_bcs_all.py"
with open(output_file, 'w') as f_out:
    f_out.write("routes = [" + '\n')

    numbers = 384
    for route_number in range(numbers):
        input_file = "u0_v0_zeros/result/quasibc_search_upper_5_lower_6_w_0_to_50_route_{}.txt".format(route_number)
        with open(input_file, 'r') as f_in:
            next(f_in)
            next(f_in)
            f_out.write("# route {}".format(route_number) + '\n')
            f_out.write("[" + '\n')
            for line in f_in:
                f_out.write(line)

    f_out.write("]" + '\n')