# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 11:14:31 2018

@author: ljfang
"""

import sys 
import os
sys.path.append(os.path.abspath(r'G:\Programs\python\restique'))
import getopt
import json
import codecs
import restique

def get_param_time(item):
    v = float(item['amt_param'])
    d = int(item['created'][2:4] + item['created'][5:7] + item['created'][8:10])
    return v * 1000000 - d

class parse_canceled:
    
    def __init__(self, user = None, opt_code = None):
        self.user = user
        self.opt_code = opt_code

    def parse_canceld_busi(self, file):
        jD = None
        with open(file, 'r', encoding="utf-8") as f:
            d = f.read()
            try:
                jD = json.loads(d)
            except Exception:
                print("json loaded error")
        if None == jD:
            print('data json data')
            return
        for db_iter in jD:
            dd = db_iter['data']
            id_hash = {}
            dd_n = []
            for dd_it in dd:
                if dd_it['id'] in id_hash:
                    continue
                id_hash[dd_it['id']] = False
                dd_n.append(dd_it)
            dd_n.sort( key=get_param_time, reverse = False)
            db_iter['data'] = dd_n
            db_iter['total'] = len(dd_n)
        with codecs.open(file, 'w', encoding='utf-8') as f:
            f.write(json.dumps(jD, indent=4, ensure_ascii=False))
        #restique.req_restique(6, 'select count(1) from member;', self.user, self.opt_code)
        
        
if __name__ == '__main__':
    user = None
    opt_code = None
    try:
        if len(sys.argv) > 1:
            opts,args = getopt.getopt(sys.argv[1:], "u:c:")
            for opt,arg in opts:
                if opt == '-u':
                    user = arg
                elif opt == '-c':
                    opt_code = arg
    except getopt.GetoptError:
        print('python parse_canceled.py -u *** -c ********')
        exit(2)
        
    fp = r'G:\Programs\python\check_member\canceld_busi.txt'
    p = parse_canceled(user, opt_code)
    p.parse_canceld_busi(fp)
