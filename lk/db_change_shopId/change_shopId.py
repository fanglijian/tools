# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 18:15:14 2018

@author: user
"""

import sys 
import os
import sqlite3

class Change_ShopId:
    
    def __init__(self, file_path, dst_shopId):
        self.file_path = file_path
        self.dst_shopId = dst_shopId
        try:
            self.sqlite_conn = sqlite3.connect(self.file_path)
        except Exception:
            print('init sqlite database fail')
    
    def __del__(self):
        try:
            self.sqlite_conn.close()
        except Exception:
            print('close sqlite connection failed')

    def getTables(self):
        sql = 'select name from sqlite_master where type=\'table\';'
        cursor = self.sqlite_conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        tables = []
        for row in rows:
            tables.append(row[0])
        return tables
    
    def getLikeTables(self):
        lk_tbls = []
        tables = self.getTables()
        for tbl in tables:
            b = True
            try:
                sql = 'select shop_id from `' + tbl + '` limit 1;'
                cursor = self.sqlite_conn.cursor()
                cursor.execute(sql)
                cursor.fetchall()
            except Exception:
                b = False
            finally:
                cursor.close()
            if b:
                lk_tbls.append(tbl)
        return lk_tbls
    
    def updShopId(self):
        lk_tbls = self.getLikeTables()
        for tbl in lk_tbls:
            sql = 'update `' + tbl + '` set shop_id=' + str(self.dst_shopId) + ';'
            try:
                cursor = self.sqlite_conn.cursor()
                cursor.execute(sql)
            except Exception:
                print('update failed:' + tbl)
            finally:
                self.sqlite_conn.commit()
                cursor.close()
    
        
if __name__ == '__main__':
    p = Change_ShopId(r'G:\Programs\python\db_change_shopId\main.db', 2000054)
    p.updShopId()