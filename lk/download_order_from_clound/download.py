# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 18:15:14 2018

@author: user
"""

import sys 
import os
sys.path.append(os.path.abspath(r'G:\Programs\python\restique'))
import getopt
import json
import restique
import sqlite3

class Download_Data_From_Clound:
    
    def __init__(self, db_id, shop_id, sqlite_filepath, user = None, opt_code = None):
        self.db_id = db_id
        self.shop_Id = shop_id
        self.sqlite_filepath = sqlite_filepath
        self.restique_user = user
        self.restique_optcode = opt_code
        try:
            self.sqlite_conn = sqlite3.connect(sqlite_filepath)
            self.init_tables()
        except Exception:
            print('init sqlite database fail')
    
    def __del__(self):
        try:
            self.sqlite_conn.close()
        except Exception:
            print('close sqlite connection failed')
    
    def init_tables(self):
        cursor = self.sqlite_conn.cursor()
        cursor.execute('create table if not exists orders(id char(16) primary key, \
                                                          shop_id int default 0, \
                                                          order_type int default 0, \
                                                          order_src int default 0, \
                                                          order_sub_src varchar(64), \
                                                          order_num varchar(64), \
                                                          serial_num varchar(64), \
                                                          ext_order_num varchar(64), \
                                                          status int default 0, \
                                                          amount double default 0, \
                                                          total double default 0, \
                                                          create_time int default 0, \
                                                          order_date int default 0, \
                                                          close_time int default 0 \
                                                          );')
        cursor.execute('create index if not exists orders_shop_createtime on orders(shop_id,create_time)')
        cursor.close()
        self.sqlite_conn.commit()

    def ins_itmes(self, tbl_name, item):
        sql = 'insert into `' + tbl_name + '`('
        v_a = []
        i = 0
        for k,v in item.items():
            if 0 == i:
                sql += '`' + k + '`'
            else:
                sql += ',`' + k + '`'
            i = i + 1
            v_a.append(v)
        sql += ') values(?' + ',?' * (len(item) - 1) + ');'
        #print(sql)
        #print(v_a)
        cursor = self.sqlite_conn.cursor()
        cursor.execute(sql, v_a)
        cursor.close()
    
    def down_orders(self, begin_order_date):
        if None == self.db_id or int(self.db_id) <= 0 :
            print('Invalid database id')
            return
        if None == self.sqlite_filepath:
            print('Invalid local sqlite file path')
            return
        sql = 'select id,shop_id,order_type,order_src,order_sub_src,order_num,serial_num,ext_order_num,status,\
        amount,total,create_time,order_date,close_time from orders where shop_id=' + str(self.shop_Id) + \
        ' and order_date>=' + begin_order_date
        rep = restique.req_restique(self.db_id, sql, self.restique_user, self.restique_optcode)
        if None == rep or len(rep) == 0 :
            print('No data from clound')
            return
        jd = json.loads(rep)
        if None != jd:
            for item in jd:
                self.ins_itmes('orders', item)
            self.sqlite_conn.commit()
        
        
        
        
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
    
    sqlite_fp = r'G:\Programs\python\check_print\liph.db'
    p = Download_Data_From_Clound(1, 100991,sqlite_fp,user, opt_code)
    p.down_orders('1523980800')        