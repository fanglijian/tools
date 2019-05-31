# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 18:05:50 2018

@author: user
"""

import os
import xlrd

class FindSameValInExcel:
    
    def __init__(self, fp):
        self.fp = fp
        
    def findSame(self, col_idx):
        if os.path.exists(self.fp) == False:
            print('No File:' + self.fp)
            return
        print(self.fp)
        data = xlrd.open_workbook(self.fp)
        table = data.sheets()[0]
        nrows = table.nrows
        val_array = []
        for row in range(0,nrows):
            v = (str)(table.cell(row,col_idx).value)
            if v in val_array:
                print('Duplicate:' + v + '(row:' + str(row) + ')')
            val_array.append(v)            

if __name__ == '__main__':
    p = FindSameValInExcel(r'G:\Programs\python\import_member\2.xls')
    p.findSame(0)