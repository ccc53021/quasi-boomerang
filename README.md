# quasi-boomerang

===================================================================

**## 1. Overview**

**Paper:** **Mix-Basis Geometric Approach to Boomerang Distinguishers. ToSC 2025, Issue 3.**

**Authors:** **Chengcheng Chang, Hosein Hadipour, Kai Hu, Muzhou Li, and Meiqin Wang**

The codes of 'search for BCs/quasi-BCs', 'derive key dependencies', 'compute the probability of boomerang distinguisher in fixed-key spaces', and 'implement the experiments to test boomerang's probability' are in the directories of each distinguisher, respectively.

===================================================================

**## 2. Requirements**

**Hardware:** 10 GB RAM

**Software:** Python 3.8+, PyBoolector, sagemath, java

**Estimated time:** 1- 4 hours (if there are too many routes, the time needs to be appropriately extended, or the time can be reduced by enabling multi-threading)

===================================================================

**## 3. Environment Installation**

We use the SMT-based solver 'pyboolector' to search for the BCs/quasi-BCs of the boomerang distinguishers using Python3. Thus, the 'pyboolector' needs to be installed before running the code of 'search for BCs/quasi-BCs'.

When performing the code in 'derive key dependencies' using Python3, 'sagemath' needs to be installed.

In order to experiment with the probability of the boomerang distinguisher, we use Python3.

The environment installation can execute the following commands (**Ubuntu**):

    pip install pyboolector, sagemath

Some experiments were conducted using java, so java needs to be installed. You can download the Java Development Kit (JDK) from the official Oracle website or use OpenJDK.

- **Official Download**: [Oracle JDK](https://www.oracle.com/java/technologies/downloads/)

- **OpenJDK Source Code**: [OpenJDK GitHub Repository](https://github.com/openjdk/jdk)

===================================================================

**## 4. Usage and Experiments**

Take the $E_m$ part of the 19-round boomerang distinguisher of GIFT-64 (the usage of other distinguishers, e.g. SKINNY, is the same) as an example to perform the basic test:

  In the directory 'gift-64/r_19/em', there are four modules, the parts $E_0$ (in the directory 'gift-64/r_19/upper') and $E_1$ (in the directory 'gift-64/r_19/lower') are identical. The order and functions are as follows:

1. 'differential_clustering' is a search for all BCs using the fixed input difference, output difference, key difference of the upper trail, and key difference of the lower trail. The results of BCs are in the file 'routes_clustering.py'.
   
   First, perform the command:
   
       python3 em_bc_search_r_2.py
   
   to get the routes of all BCs, we give them in the file 'routes_clustering.py' in the directories 'u0_v0_solutions' and 'u0_v0_zeros', respectively.

2. For each BC in the file 'routes_clustering.py', the 'u0_v0_solutions' module will conduct the first step of the two-step analysis when searching for quasi-BCs.
   
   Run the command:
   
       mkdir result
       python3 dim_2_quasibc_search_upper_1_lower_1_solutions_all.py
   
   We use multiprocessing in Python. The initial setting of pool size is 40, which can be modified based on the number of BCs, memory, and CPU threads. The 576 BCs of the $E_m$ part can be divided into 16 times to perform by modifying the parameter 'begin_i' (0, 40, 80, ... 560).

3. After implementing the module 'u0_v0_solutions' to confirm that all BCs are key-independent, the 'u0_v0_zeros' module will conduct the second step of the two-step analysis to search all quasi-BCs when setting $u_0$ = 0.
   
   Run the command:
   
       mkdir result
       python3 quasibc_search_upper_1_lower_1.py
   
   We also use multiprocessing in Python, and the initial pool size is 40.

4. The module 'key_dependencies' will derive the key conditions from all quasi-BCs.
   
   Collate all the quasi-BCs obtained in steps 3, and use the following command to merge them together to get the result file 'quasi_bcs_all.py'.
   
       python3 merge_solutions.py
   
   Then run the following command to get the output of the conditions of the key.
   
       python3 get_key_conditions_by_trails.py

5. In addition, the experiments are in the directory 'experiment'.
   
   Run the following command to perform the experiment.
   
       java route_probability_test.java

===================================================================

**## 5. Lisense**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

===================================================================

**## 6. Citation**

[Chengcheng Chang, Hosein. Hadipour, Kai Hu, Muzhou Li, and Meiqin Wang]. "Mix-Basis Geometric Approach to Boomerang Distinguishers." ToSC 2025, issue 3.
Artifact: [ccc53021/quasi-boomerang](https://github.com/ccc53021/quasi-boomerang)

===================================================================

**## 7. Contact**

For questions about this artifact: [[chengcheng.chang@mail.sdu.edu.cn](mailto:chengcheng.chang@mail.sdu.edu.cn)]

===================================================================
