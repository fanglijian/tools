# -*- coding: utf-8 -*-
"""
Created on Thu May  3 11:01:47 2018

@author: user
"""

import sys 
import os
sys.path.append(os.path.abspath(r'G:\Programs\python\restique'))
import getopt
import json
import restique

class Del_Rela_Items:
    out_file_path = r'./delete.txt'
    out_file = None
    db_id = None
    shop_id = None
    restique_user = None
    restique_optcode = None
    
    def __init__(self, db_id, shop_id, user, optcode):
        self.db_id = int(db_id)
        self.shop_id = shop_id
        self.restique_user = user
        self.restique_optcode = optcode
        self.out_file = open(self.out_file_path, 'w', encoding='utf-8')
        
    def __del__(self):
        self.out_file.close()
        
    def write_del(self, tbl, id):
        self.out_file.write( tbl + '.' + id + "\n    deleted=1\n")

    def write_log(self, info):
        self.out_file.write('\n\n' + info + '\n\n')
    
    def del_payment(self, payment_str):
        if None == self.db_id or None == self.shop_id:
            print('db is or shop_id is empty')
            return
        self.write_log(u'删除店铺' + str(self.shop_id) + u'的payment:' + ','.join(payment_str) )      
        for payment in payment_str:
            ps = payment.split(',')
            for p in ps:
                self.write_del('payment', p)
                sql = 'select id from order_payment where shop_id=' + str(self.shop_id) + ' and payment_id=\'' + p + '\' and deleted=0;'
                rep = restique.req_restique(self.db_id, sql, self.restique_user, self.restique_optcode)
                if None != rep and len(rep) > 0 and rep != 'null':
                    jd = json.loads(rep)
                    if None != jd:
                        for r in jd:
                            self.write_del('order_payment', r['id'])
                sql = 'select id from staff_performance where shop_id=' + str(self.shop_id) + ' and object_id=\'' + p + '\' and deleted=0;'
                rep = restique.req_restique(self.db_id, sql, self.restique_user, self.restique_optcode)
                if None != rep and len(rep) > 0 and rep != 'null':
                    jd = json.loads(rep)
                    if None != jd:
                        for r in jd:
                            self.write_del('staff_performance', r['id'])
    
 
def help():
    print("\nusage: python delete_items.py -u ljfang -c 12345678 -s 100032 -d 1 -t payment abcdef0123456789,abcdef0123456780\n")    
    
if __name__ == '__main__':
    user = None
    opt_code = None
    item_type = None
    args = None
    db_id = None
    shop_id = None
    try:
        if len(sys.argv) > 1:
            opts,args = getopt.getopt(sys.argv[1:], "u:c:s:d:t:")
            for opt,arg in opts:
                if opt == '-u':
                    user = arg
                elif opt == '-c':
                    opt_code = arg
                elif opt == '-t':
                    item_type = arg
                elif opt == '-s':
                    shop_id = arg
                elif opt == '-d':
                    db_id = arg
    except getopt.GetoptError:
        help()
        exit(2)
    
    if None == args or None == db_id or None == shop_id:
        help()
        exit(2)
    p = Del_Rela_Items(db_id, shop_id, user, opt_code)
    if item_type == 'payment':
        p.del_payment(args)
    else:
        help()