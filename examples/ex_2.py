from z3_staff import *

create_vars(5, type='int')
solver()
init_vars(globals())
set_ranges()

add_eq(x3 + 4 == 0x6F)
add_eq(x2 + 3 == 0x7D)
add_eq(x0 + 1 == x4 + 5 - 10)
add_eq(x1 + 2 == 0x35)
add_eq(x4 + 5 == x3 + 4 + 3)

i = 0
start_time = time.time()
while s.check() == sat:
  prepare_founded_values()
  print prepare_key()
  iterate_all()
  i += 1
print('--- %.2f second(s) && %d answer(s) ---' % ((time.time() - start_time), i) )
