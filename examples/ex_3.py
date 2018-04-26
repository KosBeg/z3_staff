from z3_staff import *
import string

digs = string.digits + string.letters
def int2base(x, base = 30):
  if x < 0:
    sign = -1
  elif x == 0:
    return digs[0]
  else:
    sign = 1
  x *= sign
  digits = []
  while x:
    digits.append(digs[x % base])
    x /= base
  if sign < 0:
    digits.append('-')
  digits.reverse()
  return ''.join(digits)

create_vars(4, size=32, prefix='k')
solver()
init_vars(globals())
set_ranges(27000, 809999, prefix='k') # 27000 is 1000 in 30 base, the least digit with 4 symbols
                                        # 809999 is TTTT in 30 base, the largest digit with 4 symbols

add_eq( k0 ^ k1 ^ k2 ^ k3 == 0x1AE33 )

# for a bit of fun :D
add_eq( k0 == 583574 ) # LICE in 30 base
add_eq( k1 == 646635 ) # NSEF in 30 base
add_eq( k2 == 672974 ) # ORME in 30 base

i = 0
start_time = time.time()
while s.check() == sat:
  ans = prepare_founded_values(prefix='k')
  _str = ''
  for j in ans:
    _str += int2base(j)
  print _str
  iterate_all(prefix='k')
  i += 1
print('--- %.2f second(s) && %d answer(s) ---' % ((time.time() - start_time), i) )
