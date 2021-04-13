# python3
# -*- coding: utf-8 -*-
import re
import getopt
import sys
import os.path

PROG_MATCH = {}
PROG_MATCH['NBA'] = '.+\[PACKETFORWARD\] NBA: .+'
PROG_MATCH['BACKSUPPORT'] = '.+\[BACKSUPPORT\] .+'

if __name__ == '__main__':
    t = 'NBA'
    fp = ''
    f = None
    opts,args = getopt.getopt(sys.argv[1:],'t:f:')
    for opt,arg in opts:
        if '-t' == opt:
            arg = arg.upper()
            t = arg
        elif '-f' == opt:
            fp = arg
    if not os.path.exists(fp) or t not in PROG_MATCH.keys():
        print('\npython3 parse.py [-t NBA | NBM] -f log_file_path\n')
        sys.exit(0)
    nm,ext = os.path.splitext(fp)
    rfp = nm + '-' + t + ext
    f2 = open(rfp, 'w', encoding='UTF-8')
    with open(fp, 'r', encoding='UTF-8') as f:
        prog = re.compile(PROG_MATCH[t])
        line = f.readline()
        while line is not None and line != '':
            result = prog.match(line)
            if result:
                f2.write(line)
            line = f.readline()
    f2.close()