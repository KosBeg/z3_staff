from z3 import *
from re import compile
import time

num_vars = 0
is_bitvecs = 0

gDE_BUG = 0

def clean_str(*args, **kwargs):
	"""Remove all characters that match regexes. """
	num_strs = len(args)
	assert num_strs > 0, 'need at least one string to clean'
	texts = [ str(i) for i in args ]
	rules = kwargs['rules'] if 'rules' in kwargs else [', $', ' $']
	ret = []
	for text in texts:
		t = text
		for rule in rules:
			t = compile(rule).sub('', t)

		ret += [t]

	if num_strs == 1:
		return ret[0]
	return ret


def create_vars(num=0, start=0, step=1, type='BitVecs', size=64, prefix='x', g=globals()):
	"""Create Z3 variables. """
	global is_bitvecs
	global num_vars
	num = num if num != 0 else num_vars
	assert num > 0, 'num must be > 0'
	is_bitvecs = 0
	start = start if start != 0 else num_vars
	type = clean_str(type.lower(), rules=['s$'])
	if type != 'int' and type != 'real':
		type = 'BitVec'
		is_bitvecs = 1
	else:
		type = type.title()
	type = type + 's' if num > 1 else type
	t0, t1 = ('', '')
	for i in range(start, start + num):
		var_name = '%s%d' % (prefix, i * step)
		t0 += 'g["%s"], ' % var_name
		t1 += '%s ' % var_name

	t0, t1 = clean_str(t0, t1)
	exe_str = '%s = %s( "%s", %d )' % (t0, type, t1, size) if is_bitvecs else '%s = %s( "%s" )' % (t0, type, t1)
	if gDE_BUG:
		print 'create_vars:', clean_str(exe_str, rules=['g\["', '"\]'])
	exec exe_str
	ret = [ eval(var) for var in clean_str(t0, rules=[',']).split(' ') ]
	num_vars += num
	if len(ret) == 1:
		return ret[0]
	return ret


def solver():
	"""Create and return Z3 Solver class. """
	global s
	s = Solver()
	return s


def add_eq(*args, **kwargs):
	"""Add equations to solver, but with optimizations. """
	opt = kwargs['opt'] if 'opt' in kwargs else 2
	for i in args:
		for j in range(opt):
			i = simplify(i)

		s.add(i)


def set_ranges(rstart=32, rend=126, num=0, start=0, step=1, prefix='x'):
	"""Set ranges. By default set ASCII range for all variables. """
	num = num if num != 0 else num_vars
	assert num > 0, 'num must be > 0'
	for i in range(start, start + num):
		eval_str = '%s%d' % (prefix, i * step)
		if gDE_BUG:
			print 'set_ranges:', eval_str
		var_name = eval(eval_str)
		if is_bitvecs:
			add_eq(UGE(var_name, rstart), ULE(var_name, rend))
		else:
			add_eq(var_name >= rstart, var_name <= rend)


def set_known_bytes(known, start=0, step=1, type='*', last_num=0, prefix='x'):
	"""Set known bytes. Useful for known flag formats. """
	last_num = last_num if last_num != 0 else num_vars
	assert last_num > 0, 'last_num must be > 0'
	for i, byte in enumerate(known):
		if byte != '*':
			eval_str = '%s%d' % (prefix, i * step)
			if gDE_BUG:
				print 'set_known_bytes1:', eval_str
			var_name = eval(eval_str)
			add_eq(var_name == ord(byte))
		else:
			if type == 'ff':
				eval_str = '%s%d' % (prefix, (last_num - 1) * step)
				if gDE_BUG:
					print 'set_known_bytes2:', eval_str
				var_name = eval(eval_str)
				byte = known.split('*')[1][-1]
				add_eq(var_name == ord(byte))
				return


def prepare_founded_values(num=0, start=0, step=1, prefix='x', g=globals()):
	"""Prepare and return founded values as array. Must be called after manual call s.check(). """
	num = num if num != 0 else num_vars
	assert num > 0, 'num must be > 0'
	t0, t1 = ('', '')
	exe_str = 'r = s.model()'
	if gDE_BUG:
		print 'prepare_founded_values1:', exe_str
	exec exe_str
	for i in range(start, num):
		var_name = '%s%d' % (prefix, i * step)
		t0 += 'g["_%s"], ' % var_name
		t1 += 'r[%s].as_long(), ' % var_name

	t0, t1 = clean_str(t0, t1)
	exe_str = '%s = %s' % (t0, t1)
	if gDE_BUG:
		print 'prepare_founded_values2:', clean_str(exe_str, rules=['g\["', '"\]', '\.as_long\(\)'])
	exec exe_str
	ret = [ eval(var) for var in clean_str(t0, rules=[',']).split(' ') ]
	if len(ret) == 1:
		return ret[0]
	return ret


def iterate_all(num=0, start=0, step=1, prefix='x'):
	"""Adds constraints to variables for the next iteration. """
	num = num if num != 0 else num_vars
	assert num > 0, 'num must be > 0'
	stri = ''
	for i in range(start, num):
		var_name = '%s%d' % (prefix, i * step)
		stri += '%s != _%s, ' % (var_name, var_name)

	exe_str = 'add_eq( Or( %s ) )' % clean_str(stri)
	if gDE_BUG:
		print 'iterate_all:', exe_str
	exec exe_str


def prepare_key(num=0, start=0, step=1, prefix='x'):
	"""Return founded values of all variables as string. """
	num = num if num != 0 else num_vars
	assert num > 0, 'num must be > 0'
	t0 = ''
	for i in range(start, num):
		var_name = '%s%d' % (prefix, i * step)
		t0 += 'chr( _%s ) + ' % var_name

	t0 = clean_str(t0, rules=[' \+ $'])
	exe_str = 'key = %s' % t0
	if gDE_BUG:
		print 'prepare_key:', clean_str(exe_str, rules=['chr\( ', ' \)'])
	exec exe_str
	return key


def init_vars(g):
	"""Hack. Initialize all variables as global in main script. """
	glb = globals()
	for i, text in enumerate(glb):
		if not text in g:
			g[text] = glb[text]
