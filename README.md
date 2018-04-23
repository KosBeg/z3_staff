# z3_staff

My small script with useful functions for typical Z3-rev CTF tasks.

## Examples

[34C3_CTF - arm_stage4](https://github.com/KosBeg/ctf-writeups/tree/master/34C3_CTF/arm_stage4/README.md)

[EasyCTF IV - ez_rev](https://github.com/KosBeg/ctf-writeups/blob/master/EasyCTF_IV/ez_rev/README.md)

[EasyCTF IV - LicenseCheck](https://github.com/KosBeg/ctf-writeups/blob/master/EasyCTF_IV/LicenseCheck/README.md)

[VolgaCTF 2018 Quals - You Shall Not Pass](https://ctftime.org/writeup/9390)

[Securinets CTF Quals 2018 - Solver](https://ctftime.org/writeup/9392)

## API

* `def create_vars(num = 0, start = 0, step = 1, type = 'BitVecs', size = 64, prefix = 'x', g = globals()):`

Create and return `num` z3 variables:
```python
from z3_staff import *
t = create_vars(1)
print t, len(t), t[0].size() # [x0] 1 64
t = create_vars(3)
print t, len(t), t[0].size() # [x0, x1, x2] 3 64
t = create_vars(3, size = 1337)
print t, len(t), t[0].size() # [x0, x1, x2] 3 1337
t = create_vars(3, start = 3)
print t, len(t), t[0].size() # [x3, x4, x5] 3 64
t = create_vars(3, type = 'int')
print t, len(t), is_int(t[0]) # [x0, x1, x2] 3 True
t = create_vars(3, prefix = 'y')
print t, len(t), t[0].size() # [y0, y1, y2] 3 64
t = create_vars(start = 3, num = 3, step = 8, type = 'BitVecs', size = 8, prefix = 'k')
print t, len(t), t[0].size() # [k3, k11, k19] 3 8
```

* `def init_vars(g):`

Hack for use created variables as global. Due the creating z3 variables by exec. Must be called before first using of vars.

* `def solver(g = globals()):`

Create and return z3 `Solver()` class:
```python
from z3_staff import *
create_vars(2)
solver()
init_vars(globals()) # hack
print s # []
s.add( x0 ^ x1  =  =  31337, x0 > 3133, x1 > 1337, x0 ! =  x1 )
print s # [x0 ^ x1  =  =  31337, x0 > 3133, x1 > 1337, x0 ! =  x1]
print s.check()  =  =  sat # True
print s.model() # [x1 = 30551, x0 = 3390]
```

* `def set_ranges(num = 0, start = 0, step = 1, rstart = 32, rend = 126, prefix = 'x', g = globals()):`

By default set printable ASCII range. But you can set your ranges.
```python
from z3_staff import *
create_vars(start = 3, num = 3, step = 8, type = 'BitVecs', size = 8, prefix = 'k')
s = solver()
init_vars(globals())
set_ranges(start = 3, num = 3, step = 8, prefix = 'k')
print s # [UGE(k3, 32), ULE(k3, 126), UGE(k11, 32), ULE(k11, 126), UGE(k19, 32), ULE(k19, 126)]
create_vars(2, prefix = 'l')
s = solver()
init_vars(globals())
set_ranges(2, rstart = 1337, rend = 31337, prefix = 'l')
print s # [UGE(l0, 1337), ULE(l0, 31337), UGE(l1, 1337), ULE(l1, 31337)]
create_vars(2, prefix = 'm', type = 'int')
s = solver()
init_vars(globals())
set_ranges(2, rstart = 1337, rend = 31337, prefix = 'm')
print s # [m0 > =  1337, m0 < =  31337, m1 > =  1337, m1 < =  31337]
```

* `def add_eq(*args, **kwargs):`

Like s.add(eq), but with optimizations.
```python
from z3_staff import *
create_vars(2)
s = solver()
init_vars(globals())
s.add(( (x0 ^ x1) ^ (x1 ^ x0)) + x1 % 2*x0 + x1 & x0   =  =  31337 )
print s # [(x0 ^ x1 ^ x1 ^ x0) + (x1%2)*x0 + x1 & x0  =  =  31337]
s.reset()
add_eq( ((x0 ^ x1) ^ (x1 ^ x0)) + x1 % 2*x0 + x1 & x0   =  =  31337 )
print s # [~(~(x0*bvsmod_i(x1, 2) + x1) | ~x0)  =  =  31337]
```

* `def set_known_bytes(known, num = 0, start = 0, step = 1, type = 'flagFormat', prefix = 'x', g = globals()):`

Selfdocumented name.
```
set_known_bytes('VolgaCTF{*}', var_num) # * - is unknown body of flag
set_known_bytes('34C3_', var_num, type = 'start')
```

* `def prepare_founded_values(num = 0, start = 0, step = 1, prefix = 'x', g = globals()):`

Return founded values of vars after s.check() as array

* `def iterate_all(num = 0, start = 0, step = 1, prefix = 'x', g = globals()):`

Prepare solver to next iteration.

* `def prepare_key(num = 0, start = 0, step = 1, type = 'string', prefix = 'x', g = globals()):`

Return founded values as string.
