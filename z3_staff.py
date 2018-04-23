from z3 import * # BitVecs, Ints, Reals, Solver, UGE, ULE, simplify, sat, Or, And
from re import compile
import time

def clean_str(*strs, **kwargs):
	lens = len(strs)
	assert lens > 0, 'need at least one text arg'
	if 'rules' in kwargs:
		rules = kwargs['rules']
	else:
		rules = [', $', ' $']
	ret = []
	for _str in strs:
		t = _str
		for rule in rules:
			t = compile(rule).sub('', t)

		ret += [t]

	if lens == 1:
		return ret[0]
	return ret

def create_vars(num = 0, start = 0, step = 1, type = 'BitVecs', size = 64, prefix = 'x', g = globals()):
	assert num > 0, 'num must be > 0'
	g['bit_vecs'] = 0
	type = clean_str(type.lower(), rules = ['s$'])
	if type != 'int' and type != 'real':
		type = 'BitVec'
		g['bit_vecs'] = 1
	else:
		type = type.title()
	if num > 1:
		type += 's'
	p0, p1 = '', ''
	for i in range(start, start+(num*step), step):
		var_name = '%s%d' % (prefix, i)
		p0 += 'g["%s"], ' % var_name
		p1 += var_name + ' '

	p0, p1 = clean_str(p0, p1)
	if g['bit_vecs']:
		stri = '%s = %s( "%s", %d )' % (p0, type, p1, size)
	else:
		stri = '%s = %s( "%s" )' % (p0, type, p1)
	exec stri
	ret = [ eval(var) for var in clean_str(p0, rules = [',']).split(' ') ]
	if len(ret) == 1:
		return ret[0]
	return ret

def solver(g = globals()):
	g['s'] = Solver()
	return g['s']

def add_eq(*args, **kwargs):
	if 'opt' in kwargs:
		opt = kwargs['opt']
	else:
		opt = 2
	for i in args:
		for j in range(opt):
			i = simplify(i)
		s.add(i)

def set_ranges(num = 0, start = 0, step = 1, rstart = 32, rend = 126, prefix = 'x', g = globals()):
	assert num > 0, 'num must be > 0'
	for i in range(start, start+(num*step), step):
		var_name = eval('g["%s%d"]' % (prefix, i))
		if g['bit_vecs']:
			add_eq(UGE(var_name, rstart), ULE(var_name, rend))
		else:
			add_eq(var_name > = rstart, var_name < = rend)

def set_known_bytes(known, num = 0, start = 0, step = 1, type = 'flagFormat', prefix = 'x', g = globals()):
	assert num > 0, 'num must be > 0'
	type = type.lower()
	if type == 'flagformat' or type == 'ff':
		p0, p1 = known.split('*')
		for i in range(start, len(p0)):
			var_name = eval('%s%d' % (prefix, i*step))
			add_eq(var_name == ord(p0[i]))

		assert p1 == '}', 'last flagFormat char must be "}"???'
		var_name = eval('%s%d' % (prefix, num - 1))
		add_eq(var_name == ord(p1))
	elif type == 'start':
		for i in range(start, len(known)):
			var_name = eval('%s%d' % (prefix, i*step))
			add_eq(var_name == ord(known[i]))

def prepare_founded_values(num = 0, start = 0, step = 1, prefix = 'x', g = globals()):
	assert num > 0, 'num must be > 0'
	p0, p1 = '', ''
	exec 'g["r"] = g["s"].model()'
	for i in range(start, num, step):
		var_name = '%s%d' % (prefix, i)
		p0 += 'g["_%s"], ' % var_name
		p1 += 'r[%s].as_long(), ' % var_name

	p0, p1 = clean_str(p0, p1)
	stri = '%s = %s' % (p0, p1)
	exec stri
	return [ eval(var) for var in clean_str(p0, rules = [',']).split(' ') ]

def iterate_all(num = 0, start = 0, step = 1, prefix = 'x', g = globals()):
	assert num > 0, 'num must be > 0'
	stri = ''
	for i in range(start, num, step):
		var_name = '%s%d' % (prefix, i)
		stri += '%s != _%s, ' % (var_name, var_name)

	stri = 'add_eq( Or( %s ) )' % clean_str(stri)
	exec stri

def prepare_key(num = 0, start = 0, step = 1, type = 'string', prefix = 'x', g = globals()):
	assert num > 0, 'num must be > 0'
	type = type.lower()
	if type == 'string':
		p0 = ''
		for i in range(start, num, step):
			var_name = '%s%d' % (prefix, i)
			p0 += 'chr( g["_%s"] ) + ' % var_name

		p0 = clean_str(p0, rules = [' \+ $'])
		stri = 'key = %s' % p0
		exec stri
		return key

def z3_pow(a, n, g = globals()):
	if n == 2:
		return a * a
	n = int(round(n))
	res = 1
	while n:
		if n & 1:
			res *= a
		a *= a
		n >>= 1

	return res

def init_vars(g):
	glb = globals()
	for i, text in enumerate(glb):
		g[text] = glb[text]
