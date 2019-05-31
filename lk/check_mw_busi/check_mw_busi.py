o# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 21:03:45 2018

@author: user
"""

import sys 
import os
import xlrd
from functools import cmp_to_key

def sort_busi_by_time(a, b):
    print(a)
    print(b)
    return a['time'] < b['time']

class ReadMeiweiPay:
    def __init__(self, fp):
        self.fp = fp
        
    def readExcel(self):
        if os.path.exists(self.fp) == False:
            print('no excel file')
            return
        res = []
        data = xlrd.open_workbook(self.fp)
        table = data.sheets()[0]
        nrows = table.nrows
        order_total = 0
        pay_total = 0
        for row in range(1,nrows):
            #busiTime = xlrd.xldate_as_tuple(table.cell(row,2).value, 0)
            busiTime = xlrd.xldate.xldate_as_datetime(table.cell(row,2).value, 0)
            ordAmt = table.cell(row,9).value
            realPay = table.cell(row,10).value
            busi = {}
            busi['time'] = busiTime
            busi['amt'] = ordAmt
            busi['pay'] = realPay
            if ordAmt != realPay:
                print(busi)
            res.append(busi)
            order_total += float(ordAmt)
            pay_total += float(realPay)
        res.sort(key=lambda busi : busi['time'])
        #res.sort( sort_busi_by_time)
        #sorted(res, cmp = sort_busi_by_time)
        #print(res)
        print( 'order:' + str(order_total))
        print( 'pay:' + str(pay_total))
        return
        with open('./result.txt', 'w', encoding="utf-8") as f:
            for busi in res:
                #f.write( str(busi['time']) + '    ' + str(busi['amt']) + '\n')
                line = "%.2f" %(float(busi['amt']))
                f.write(line + "\n")
                
                
if __name__ == '__main__':
    p = ReadMeiweiPay('./mw.xls')
    p.readExcel()