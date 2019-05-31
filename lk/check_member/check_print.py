# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 20:24:31 2018

@author: user
"""

import sqlite3
import time


def formatTime(iTime):
    st = time.localtime(iTime)
    return time.strftime('%Y-%m-%d %H:%M:%S', st)
    
class Check_Print:
    
    def __init__(self, sqlite_filepath):
        try:
            self.sqlite_conn = sqlite3.connect(sqlite_filepath)
        except Exception:
            print('init sqlite database fail')

    def __del__(self):
        try:
            self.sqlite_conn.close()
        except Exception:
            print('close sqlite connection failed')

    def check_waimai_print(self, create_time):
        
        cursor = self.sqlite_conn.cursor()
        cursor.execute('select id,order_num,serial_num,order_sub_src,create_time from orders where order_type=12 and order_src=12 and create_time>=' \
                       + str(create_time) + ' order by order_sub_src,create_time' )
        orders = cursor.fetchall()
        cursor.close()
        if None == orders:
            print('No orders')
            return
        cur_subsrc = None
        idx = 1
        for order in orders:
            #print(order)
            if None == cur_subsrc or cur_subsrc != order[3]:
                cur_subsrc = order[3]
                idx = 1
                print( "\n\n------- " + cur_subsrc + ' -------' )
            serial_num = int(order[2])
            #print(serial_num)
            #if serial_num <= 0 or serial_num > 1000:
            #    return
            while idx != serial_num:
                print('missing ' + str(idx))
                idx = idx + 1
                #if idx <= 0 or idx > 400:
                #    return
            order_time = int(order[4]) * 1000
            cursor = self.sqlite_conn.cursor()
            cursor.execute('select status,retry,title,created from print_queue where title like \'' +  order[1] + '%\';')
            printdata = cursor.fetchall()
            print_count = 0
            status = 1
            retry = 0
            title = None
            print_time = 0
            if None != printdata:
                print_count = len(printdata)
                for pd in printdata:
                    curStatus = int(pd[0])
                    curRetry = int(pd[1])
                    if curStatus != 1:
                        status = curStatus
                    if curRetry > retry:
                        retry = curRetry
                    if None == title:
                        title = pd[2]
                    else:
                        title = title + ' ' + pd[2]
                    print_time = int(pd[3])
            cursor.close()
            print( str(idx) + '  status:' + str(status) + '  retry:' + str(retry) + '  print_count:' + str(print_count) \
                  + "  time_diff:" + str(print_time-order_time) + '  order_time:' + formatTime(order[4]) + '  ' + str(title) )
            idx = idx + 1
        
    
    

if __name__ == '__main__':
    sqlite_fp = r'G:\Programs\python\check_print\liph.db'
    p = Check_Print(sqlite_fp)
    p.check_waimai_print(1524067200)