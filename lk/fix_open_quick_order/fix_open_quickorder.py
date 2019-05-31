# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 14:06:53 2018

@author: user
"""

import sys 
import os
sys.path.append(os.path.abspath(r'../restique'))
import getopt
import re
import json
import restique

class fix_open_quickorder:
    
    '''
    oper_type： 处理方式： delItem: 删除最后增加的条目； addPay: 增加payment
    '''
    def __init__(self, dbname, db_idx, oid, qid, oper_type = None, user = None, opt_code = None):
        self.dbname = dbname
        self.db_idx = db_idx
        self.oid = oid
        self.qid = qid
        self.oper_type = oper_type
        self.user = user
        self.opt_code = opt_code
 
    def check_order(self):
        if None == self.oid:
            print(u'openapi订单ID为空（一般为看板订单）')
            return False
        if None == self.qid:
            print('纯收银订单ID为空')
        
        sql = 'select id,order_type,shop_id,order_sub_src,total,remark from orders where id in ("' + self.oid + '","' + self.qid + '");'
        rep = restique.req_restique(self.dbname, self.db_idx, sql, self.user, self.opt_code)
        if None == rep or len(rep) <= 0 or rep == 'null':
            print('connect to restique failed!')
            return False
        try:
            data = json.loads(rep)
        except Exception:
            print(rep)
            return False
        total_o = None
        total_q = None
        for jDIter in data:
            if jDIter['id'] == self.oid:
                if u'纯收银' in jDIter['remark']:
                    print(u'openapi订单可能是纯收银订单')
                    return False
                total_o = (float)(jDIter['total'])
            elif jDIter['id'] == self.qid:
                if u'纯收银' in jDIter['remark']:
                    print(u'纯收银订单ID可能错误')
                    return False
                total_q = (float)(jDIter['total'])
        if None == total_o or None == total_q:
            print(u'没有找到订单')
            return False
        fDiff = total_q - total_o
        if 0 != fDiff:
            print(u'两个订单差额(order.total):' + str(fDiff))
        payment_q = self.get_payment(self.qid)
        if None == payment_q or len(payment_q) != 1:
            print(u'')
            return False
        pay_eaq = True
        del_
        if float(payment_q['paid']) != total_o:
            if 'delItem' == self.oper_type:
                pay_eaq = False
                lastItem = self.get_latItem(self.oid)
                if None != lastItem:
                    if total_o - float(lastItem['price']) == total_q:
                        
                    
        
    def get_payment(self, oid):
        sql = 'select id,paid from payment where id in (select payment_id from order_payment where one_order_id in (select id from one_order where order_id="' + oid + '"));'
        rep = restique.req_restique(self.dbname, self.db_idx, sql)
        if None == rep or len(rep) <= 0 or rep == 'null':
            return None
        try:
            data = json.loads(rep)
        except Exception:
            print(rep)
            return None
        return data
  
    def get_latItem(self, oid):
        sql = 'select id,(price*counts) as price from order_item where one_order_id in (select id from one_order where order_id="' + oid + '") order by created desc limit 1;'
        rep = restique.req_restique(self.dbname, self.db_idx, sql)
        if None == rep or len(rep) <= 0 or rep == 'null':
            return None
        try:
            data = json.loads(rep)
            return data[0]
        except Exception:
            print(rep)
            return None
         
    
def help():
    print(u"\nusage: python fix_open_quickorder.py -d ali_1 -o orderId_open -q orderId_quick [-u ljfang -c 12345678]\n\n  -d [ali|uc]_dbIndx\n  -o 看板订单\n  -q 纯收银订单\n")    
        
        
if __name__ == '__main__':
    user = None
    opt_code = None
    db = None
    oid = None
    qid = None
    try:
        if len(sys.argv) > 1:
            opts,args = getopt.getopt(sys.argv[1:], "d:o:q:u:c:")
            for opt,arg in opts:
                if opt == '-u':
                    user = arg
                elif opt == '-c':
                    opt_code = arg
                elif opt == '-d':
                    db = arg
                elif opt == '-o':
                    oid = arg
                elif opt == '-q':
                    qid = arg                    
    except getopt.GetoptError:
        help()
        exit(2)
    if None == db or None == oid or None == qid:
        help()
        exit(2)
    db_idx = 1
    if '_' in db or '-' in db:
        mat = re.search('[_-]+', db)
        if None != mat:
            i = mat.start()
            db_idx = int(db[i+1:])
            db = db[0:i]
    if db != 'ali' and db != 'uc':
        print('db muse be ali or uc')
        exit(2)
    p = fix_open_quickorder( db, db_idx, oid, qid, user, opt_code)
    p.check_order()