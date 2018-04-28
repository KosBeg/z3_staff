from z3_staff import * # https://github.com/KosBeg/z3_staff

x = create_vars(21, size=8) # create and return 21 BitVecs with size 8
s = solver() # create and return solver
set_ranges() # set ASCII ranges(printable chars) for all vars created by create_vars

set_known_bytes('MCA{*}', type='ff') # set known flag format, or we can use without ", type='ff'" like "set_known_bytes('MCA{' + '*'*16 + '}')"

# add all known equations
add_eq( x[19] + x[8] - x[13] + x[9] == 104 )            # check_0
add_eq( x[16] - x[8] - x[9] * x[1] - x[19] == -4464 )   # check_1
add_eq( x[14] * x[15] == 2912 )                         # check_2
add_eq( x[2] * x[13] + x[6] == 4541 )                   # check_3
add_eq( x[7] + x[4] * x[7] * x[2] == 211300 )           # check_4
add_eq( x[15] * (x[12] + 1) + x[14] == 3748 )           # check_5
add_eq( x[19] * x[18] - x[20] * x[4] - x[13] == -5332 ) # check_6
add_eq( x[3] * x[0] * x[5] == 454608 )                  # check_7
add_eq( x[3] * x[9] - x[8] == 8064 )                    # check_8
add_eq( x[1] - x[5] * x[9] - x[5] + x[1] == -3082 )     # check_9
add_eq( x[11] * x[4] + x[9] == 3511 )                   # check_10
add_eq( x[14] * x[19] + x[3] == 3091 )                  # check_11
add_eq( x[16] * x[0] * x[4] * x[18] == 17567550 )       # check_12
add_eq( x[17] + x[16] * x[19] + x[13] * x[7] == 6950 )  # check_13
add_eq( x[14] + x[4] * x[7] - x[8] == 3252 )            # check_14
add_eq( x[17] + x[0] * x[10] * x[11] == 212267 )        # check_15
add_eq( x[17] + x[16] - x[15] + x[12] == 138 )          # check_16
add_eq( x[8] + x[5] * x[14] == 2742 )                   # check_17
add_eq( x[5] * x[2] == 3120 )                           # check_18
add_eq( x[20] - x[8] + x[1] * x[12] - x[12] == 4691 )   # check_19
add_eq( x[5] + x[6] + x[9] == 170 )                     # check_20

i = 0
start_time = time.time()
if s.check() == sat: # https://stackoverflow.com/questions/13395391/z3-finding-all-satisfying-models
  founded = prepare_founded_values() # return founded values as array
  print ''.join( chr(j) for j in founded ) # print flag as string
  iterate_all() # prepare to next iteration, anticollision
  i += 1
print('--- %.2f second(s) && %d answer(s) ---' % ((time.time() - start_time), i) )
