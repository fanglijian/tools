# -*- coding: utf-8 -*-
"""
Created on Mon May  7 10:43:23 2018

@author: user
"""

import sys 
import os
sys.path.append(os.path.abspath(r'G:\Programs\python\restique'))
import getopt
import json
import restique
import time

class Check_Shift:
    
    def __init__(self, db_id, shop_id, user, optcode):
        self.db_id = int(db_id)
        self.shop_id = shop_id
        self.restique_user = user
        self.restique_optcode = optcode
        
    def check(self, date):
        shifts = self.get_shift(date)
        orders = self.get_orders(date)
        sz1 = len(shifts)
        sz2 = len(orders)
        for i in range(sz1):
            sh = shifts[i]
            st_time = int(sh['start_time'])
            ed_time = int(sh['shift_time'])
            print(u'开班: pos_owner:' + sh['pos_owner_id'] + ' staff:' + sh['start_staff_name'] + ' ' + \
                  time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(st_time + 28800)) + '\n\n')
            for j in range(sz2):
                o = orders[j]
                if o['pay_time'] >= st_time and o['pay_time'] <= ed_time:
                    print('  ' + o['order_num'] + ' pos_owner:' + o['pos_owner_id'] + ' create_time:' + \
                          time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(int(o['create_time']) + 28800)) + ' close_time:' + \
                          time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(int(o['close_time']) + 28800)) + ' pay_time:' + \
                          time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(int(o['pay_time']) + 28800)) )
            print(u'交班: pos_owner:' + sh['pos_owner_id'] + ' staff:' + sh['shift_staff_name'] + ' ' + \
                  time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(ed_time + 28800)) + '\n\n')
            
        
    def get_shift(self, date):
        end_date = date +  86400
        sql = 'select id,start_staff_name,start_time,shift_staff_name,shift_time,pos_owner_id from `shift` where shop_id=' + str(self.shop_id) \
        + ' and deleted=0 and ((start_time>=' + str(date) + ' and start_time<' + str(end_date) + ') or (shift_time>=' \
        + str(date) + ' and shift_time<' + str(end_date) + ')) order by start_time,shift_time;'
        #print(sql)
        rep = restique.req_restique(self.db_id, sql, self.restique_user, self.restique_optcode)
        if None == rep or len(rep) <= 0 or rep == 'null':
            print('No shift info\n')
            return
        #print(rep)
        pos_shift_time_hash = {}
        data = json.loads(rep)
        sz = len(data)
        for i in range(sz):
            d = data[i]
            st_time = int(d['start_time'])
            ed_time = int(d['shift_time'])
            if ed_time < st_time:
                if ed_time != 0 or i != sz - 1:
                    print('error shift recard: id->' + d['id'] + ' start_time:' + str(st_time) + ' shift_time:' + str(ed_time) + '\n' )
            if d['pos_owner_id'] not in pos_shift_time_hash:
                pos_shift_time_hash[d['pos_owner_id']] = ed_time
            elif pos_shift_time_hash[d['pos_owner_id']] >= st_time:
                print('error shift recard: id->' + d['id'] + ' start_time:' + str(st_time) + ' shift_time:' + str(ed_time) + '\n' )
            else:
                pos_shift_time_hash[d['pos_owner_id']] = ed_time
        return data
   
    def get_orders(self, date):
        date_bef = date -  86400
        end_date = date + 86400
        sql = 'select id,order_type,order_num,amount,total,create_time,close_time,status,pos_owner_id from orders where shop_id=' + str(self.shop_id) \
        + ' and order_date>=' + str(date_bef) + ' and deleted=0 and create_time>=' + str(date_bef) + ' and create_time<' + str(end_date) \
        + ' order by create_time;';
        rep = restique.req_restique(self.db_id, sql, self.restique_user, self.restique_optcode)
        if None == rep or len(rep) <= 0 or rep == 'null':
            print('No orders\n')
        datas = json.loads(rep)
        for i in range(len(datas)):
            d = datas[i]
            sql = 'select create_time,payment_method_name from payment where id in (select payment_id from order_payment where one_order_id in (select id from ' \
            + ' one_order where order_id=\'' + d['id'] + '\' and deleted=0) and deleted=0) and deleted=0 order by create_time limit 1;'
            pRep = restique.req_restique(self.db_id, sql, self.restique_user, self.restique_optcode)
            pay_time = 0
            if None != pRep and len(pRep) > 0 and pRep != 'null':
                payments = json.loads(pRep)
                if None != payments and len(payments) > 0:
                    pay_time = int(payments[0]['create_time'])
                    datas[i]['pay_time'] = pay_time
        return datas
        
    
def help():
    print("\nusage: python check_shift.py -u ljfang -c 12345678 -s 100032 -d 1 20180504\n")    
    
if __name__ == '__main__':
    user = None
    opt_code = None
    args = None
    db_id = None
    shop_id = None
    try:
        if len(sys.argv) > 1:
            opts,args = getopt.getopt(sys.argv[1:], "u:c:s:d:")
            for opt,arg in opts:
                if opt == '-u':
                    user = arg
                elif opt == '-c':
                    opt_code = arg
                elif opt == '-s':
                    shop_id = arg
                elif opt == '-d':
                    db_id = arg
    except getopt.GetoptError:
        help()
        exit(2)
    
    if None == args or len(args) != 1 or None == db_id or None == shop_id:
        help()
        exit(2)
    t = int(time.mktime(time.strptime(args[0], "%Y%m%d")))
    if t <= 0:
        help()
        exit(2)
    p = Check_Shift(db_id, shop_id, user, opt_code)
    p.check(t)
