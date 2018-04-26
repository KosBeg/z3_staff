from z3_staff import *

create_vars(18, size=17)
solver()
init_vars(globals())
set_ranges()

# add_eq( x0 > 29 ) # we have flagFormat - {x0...x4, x17}, so we can skip it
# add_eq( x1 <= 120 )
# add_eq( pw == z3_pow((x1 ^ x0), 4919.0) )
# add_eq( fmd == x1 * fmod(pw, 500.0) )
# add_eq( z3_pow(fmd, 2.0) - (282000 * x0 * x1 + 4900000) == 10663648 )
# add_eq( x4 * (x3 ^ x2) - x2 == 641 )
# add_eq( x2 * x2 / x4 + x3 == 179 )
add_eq( x5 + (x7 ^ x6) % 4 == 113 )
add_eq( x6 * x7 / x5 == 117 )
add_eq( x7 > 49 )
add_eq( (2 * x9 ^ x8 * x11) == 8983 )
add_eq( x11 * x8 - (x9 ^ x8 * x11) == 116 )
add_eq( ((311 - x12) ^ x10 * x13) == 9819 )
add_eq( x12 + 3 * x10 - 2 * x13 * x10 == -19332 )
add_eq( 202 * (x16 * x14 + x15) - x15 * (x14 ^ x16) == 1998612 )
add_eq( ((x16 + x17) * x16 * x17 ^ 0x1337) - (x16 - (x17 ^ x16) + x16) == 2816180 )

set_known_bytes('Flag{*}', type='ff')

i = 0
start_time = time.time()
while s.check() == sat:
  prepare_founded_values()
  print prepare_key()
  iterate_all()
  i += 1
print('--- %.2f second(s) && %d answer(s) ---' % ((time.time() - start_time), i) )
