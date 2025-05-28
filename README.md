# quasi-boomerang

The codes of 'search for BCs/quasi-BCs', 'derive key dependencies', 'compute the probability of boomerang distinguisher in fixed-key spaces', and 'implement the experiments to test boomerang's probability' are in the directories of each distinguisher, respectively.

Take the $E_m$ part of the 19-round boomerang distinguisher of GIFT-64 as an example:

  In the directory 'gift-64/r_19/em', there are four modules. The order and functions are as follows:
  
  1. 'differential_clustering' is a search for all BCs using the fixed input difference, output difference, key difference of the upper trail, and key difference of the lower trail. The results of BCs are in the file 'routes_clustering.py'.
  2. For each BC in the file 'routes_clustering.py', the 'u0_v0_solutions' module will conduct the first step of the two-step analysis when searching for quasi-BCs.
  3. After implementing the module 'u0_v0_solutions' to confirm that all BCs are key-independent, the 'u0_v0_zeros' module will conduct the second step of the two-step analysis to search all quasi-BCs when setting $u_0$ = 0.
  4. The module 'key_dependencies' will derive the key conditions from all quasi-BCs.

  In addition, the experiments are in the directory 'experiment'.
