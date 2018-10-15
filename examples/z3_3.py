from z3_staff import *


def brute_hash(need_hash):
    fname = 'collisions3'
    open(fname, 'a').write("trying to brute: %d\n" % need_hash)

    for length in range(24, 50):
        staff_clear()

        known = "'A_FLARE_f0r_th3_Dr4m4t1"
        klen = len(known)

        hash = BitVec("hash", 32)
        create_vars(length, size=8)
        s = solver()
        s.reset()

        init_vars(globals())

        set_ranges(0x20, 0x7E, start=klen)
        set_known_bytes(known)

        hash = hash & 0

        # loop
        for i in range(length):
            exec ("hash = ((hash << 5) - hash) + ZeroExt(24, x%d)" % i)

        add_eq(hash == need_hash)

        open(fname, 'a').write("start\n")
        cou = 0
        start_time = time.time()
        while s.check() == sat:
            vals = prepare_founded_values()
            out = ''
            for i in vals:
                out += chr(i)
            open(fname, 'a').write(out + '\n')
            iterate_all(start=klen)
            cou += 1

        open(fname, 'a').write('--- for len %d && %.2f second(s) && %d answer(s) ---\n' %
                               (length, (time.time() - start_time), cou))


brute_hash(1164071950 & 0xFFFFFFFF)
