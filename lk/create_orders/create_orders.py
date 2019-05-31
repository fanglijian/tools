#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 17:11:10 2019

@author: lijianfang
"""

import random
import datetime
import time
import pymysql.cursors


class CreateOrders:
    
    def __init__(self, db_server, db_name, user_name, pwd, shop_id):
        self.db_server = db_server
        self.db_name = db_name
        self.user_name = user_name
        self.pwd = pwd
        self.shop_id = shop_id
        
        random.seed(time.time())
        self.id_hash = {}
        
        try:
            self.db = pymysql.connect(host=self.db_server, user=self.user_name, password=self.pwd, db=self.db_name, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
            self.cursor = self.db.cursor()
        except Exception:
            print('connect database exception')

    def __del__(self):
        self.db.close()
    
    def uuid(self):
        s = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        l = len(s) - 1
        #uuid = s[random.randint(0, l)]
        uuid = 'FFF'
        for i in range(3,16):
            uuid += s[random.randint(0, l)]
        return uuid

    def randomSrcDispatchOrder(self, given_orderId_set):
        sql = 'select count(distinct(order_id)) as c from one_order where id in (select one_order_id from order_item where id in \
        (select object_id from staff_performance where shop_id=' + str(self.shop_id) + ' and type=36 and deleted=0) \
        and deleted=0)'
        if None != given_orderId_set:
            sql += ' and order_id in (' + given_orderId_set + ')';
        sql += ' and order_id not like \'FFF%\' and deleted=0;'
        c = 0
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchone()
            c = int(data['c'])
        except Exception:
            print('query exception: orders\' counts')
            return
        if c < 1:
            print('No Order')
            return None
        
        order_id = None
        oft = random.randint(0, c -1)
        sql = 'select oid from (select distinct(order_id) as oid from one_order where id in (select one_order_id from order_item where id in \
        (select object_id from staff_performance where shop_id=' + str(self.shop_id) + ' and type=36 and deleted=0) \
        and deleted=0)'
        if None != given_orderId_set:
            sql += ' and order_id in (' + given_orderId_set + ')';
        sql += ' and order_id not like \'FFF%\' and deleted=0) as t limit ' + str(oft) + ',1;'      
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchone()
            order_id = data['oid']
        except Exception:
            print('query exception: select order_id failed. sql:' + sql)
            return None
        
        if None == order_id or len(order_id) != 16:
            print('Invalid order_id')
            return None
        #print('order_id:' + order_id)
        return order_id

    def cloneOrders(self, order_id, prefix_num, serianl_num):
        data = self.cloneRecord('orders', order_id)
        if None == data:
            return None
        data['serial_num'] = serianl_num
        data['order_num'] = "%s%04d" %(prefix_num, serianl_num)
        curTimeStamp = int(datetime.datetime.now().timestamp())
        data['create_time'] = data['order_date'] = data['close_time'] = curTimeStamp
        return data
        
    def cloneOneOrder(self,order_id):
        sql = 'select id from one_order where order_id=\'' + order_id + '\';'
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
        except Exception:
            print('query exception: cloneOneOrder failed. ' + ' order_id:' + order_id)
            return None,None
        curTimeStamp = int(datetime.datetime.now().timestamp())
        one_order = []
        ooIds = None
        for d in data:
            if None == ooIds:
                ooIds = '\'' + d['id'] + '\''
            else:
                ooIds += ',\'' + d['id'] + '\''            
            oo = self.cloneRecord('one_order', d['id'])
            if oo == None:
                return None,None
            oo['create_time'] = curTimeStamp
            one_order.append(oo)

        replace_id_props = ['order_id']
        for i in range(len(one_order)):
            self.replace_id(one_order, i, replace_id_props)
        return ooIds,one_order
  
    def cloneOrderItem(self, one_order_ids):
        sql = 'select id from order_item where one_order_id in (' + one_order_ids + ');'
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
        except Exception:
            print('query exception: cloneOrderItem failed. ' + ' one_order_ids:' + one_order_ids)
            return None, None
        order_item = []
        oiIds = None
        for d in data:
            if None == oiIds:
                oiIds = '\'' + d['id'] + '\''
            else:
                oiIds += ',\'' + d['id'] + '\''  
                
            oi = self.cloneRecord('order_item', d['id'])
            if oi == None:
                return None, None
            order_item.append(oi)          
            
        replace_id_props = ['one_order_id', 'parent_id']
        for i in range(len(order_item)):
            self.replace_id(order_item, i, replace_id_props)
        return oiIds, order_item     
 
    def cloneStaffPerformances(self, all_ids):
        sql = 'select id from staff_performance where object_id in (' + all_ids + ');'
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
        except Exception:
            print('query exception: cloneStaffPerformances failed. ' + ' all_ids:' + all_ids)
            return None, None
        curTimeStamp = int(datetime.datetime.now().timestamp())
        staff_performances = []
        for d in data:                
            sp = self.cloneRecord('staff_performance', d['id'])
            if sp == None:
                return None, None
            sp['op_time'] = curTimeStamp
            if 36 == int(sp['type']):
                sp['status'] = 0;
            staff_performances.append(sp)          
        
        replace_id_props = ['object_id']
        for i in range(len(staff_performances)):
            self.replace_id(staff_performances, i, replace_id_props)    
        return staff_performances      
    
    
    def cloneRecord(self, tbl, ID):
        sql = 'select * from ' + tbl + ' where id=\'' + ID + '\';'
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchone()
        except Exception:
            print('query exception: cloneRecord failed,table:' + tbl + ' id:' + ID)
            return None
        id2 = self.uuid()
        self.id_hash[ID] = id2
        data['id'] = id2;
        return data
    
    def replace_id(self, data_array, idx, replace_id_props):
        if None != replace_id_props:
            for prop in replace_id_props:
                if data_array[idx][prop] in self.id_hash:
                    data_array[idx][prop] = self.id_hash[data_array[idx][prop]]
                
    def getStartSerialNo(self):
        y = datetime.datetime.now().year
        m = datetime.datetime.now().month
        d = datetime.datetime.now().day
        dt = datetime.datetime(y, m, d, 0, 0, 0)
        curTimeStamp = int(dt.timestamp())
        prefix_num = dt.strftime('%y%m%d')
        sql = 'select order_num from orders where shop_id=' + str(self.shop_id) + ' and create_time>=' + str(curTimeStamp) + \
        ' and order_num like \'' + prefix_num + '%\' order by order_num desc limit 1'
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchone()
        except Exception:
            print('query exception: getStartSerialNo')
            return None,None
        serial_num = 0
        if None != data:
            serial_num = int(data['order_num']) % 10000;
        return prefix_num,serial_num

    def insItems(self, tbl, data):
        prop = None
        values = None
        for k,v in data.items():
            if 'created' == k or 'updated' == k or None == v:
                continue
            if None == prop:
                prop = '`' + k + '`'
                values = '\'' + str(v) + '\''
            else:
                prop += ',`' + k + '`'
                values += ',\'' + str(v) + '\''
        sql = 'insert into ' + tbl + '(' + prop + ') values(' + values + ');'
        #print(sql)
        try:
            self.cursor.execute(sql)
        except Exception:
            print('insert failed; table:' + tbl)
            print(data)
            return False
        return True               

    def given_order_id_set(self, sql):
        given_orderId_set = None
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
        except Exception:
            print('query failed; given_order_id_set. sql:' + sql)
        if None != data and len(data) > 0 :
            for d in data:
                if None == given_orderId_set:
                    given_orderId_set = '\'' + d['id'] + '\''
                else:
                    given_orderId_set += ',\'' + d['id'] + '\''
        return given_orderId_set

    def createDispatchOrders(self, counts):
        prefix_num,serial_num = self.getStartSerialNo()
        if None == prefix_num:
            return
        given_order_id_set = self.given_order_id_set('select id from orders where shop_id=' + str(self.shop_id) + ' and order_date>=1550764800 and order_date<1550851200 and deleted=0;')
        orders = []
        one_order = []
        order_item = []
        staff_performance = []
        for i in range(counts):
            oid = self.randomSrcDispatchOrder(given_order_id_set)
            if None == oid:
                return
            serial_num += 1
            o = self.cloneOrders(oid, prefix_num, serial_num)
            if None == o:
                continue
            orders.append(o)
            
            ooIds,oos = self.cloneOneOrder(oid)
            if None == oos:
                continue
            for oo in oos:
                one_order.append(oo)
                
            oiIds, ois = self.cloneOrderItem(ooIds)
            if None == oiIds:
                continue
            for oi in ois:
                order_item.append(oi)
            
            allIds = '\'' + oid + '\',' + ooIds + ',' + oiIds
            sps = self.cloneStaffPerformances(allIds)
            if None == sps:
                continue
            for sp in sps:
                staff_performance.append(sp)
        
        #print(orders)
        #print("\n")
        #print(one_order)
        #print("\n")
        #print(order_item)
        #print("\n")
        #print(staff_performance)
        #print("\n")    
        
        runOk = True
        for o in orders:
            if False == self.insItems('orders', o):
                runOk = False
                break
        if runOk:
            for o in one_order:
                if False == self.insItems('one_order', o):
                    runOk = False
                    break
        if runOk:
            for o in order_item:
                if False == self.insItems('order_item', o):
                    runOk = False
                    break
        if runOk:
            for o in staff_performance:
                if False == self.insItems('staff_performance', o):
                    runOk = False
                    break                    
            
        try:
            if runOk:
                self.db.commit()
            else:
                print('rollback')
                self.db.rollback()
        except Exception:
            print('commit or rollback failed')
            
        
if __name__ == '__main__':
    p = CreateOrders('10.0.19.175', 'shop-01', 'admin', 'e1HpM4jpLDsI6HLi', 5000093)
    p.createDispatchOrders(50)