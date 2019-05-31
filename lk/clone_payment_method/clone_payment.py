#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 23 13:56:48 2018

@author: lijianfang
"""

import sys,os
import re
import random
import time
import datetime


class ClonePaymethod():

    def __init__(self, shop_id):
        self.shop_id= shop_id
        dt = datetime.datetime.now()
        self.cur_time = dt.strftime('%Y-%m-%d %H:%M:%S.%f')
    
    uuid_counter = 0
    shop_id = 0
    cur_time = 0
    id_hash = {}

    def uuid(self):
        self.uuid_counter += 1
        random.seed( time.time() + self.uuid_counter)
        self.uuid_counter += 1234
        s = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        l = len(s) - 1
        uuid = s[random.randint(0, l)]
        for i in range(1,16):
            uuid += s[random.randint(0, l)]
        return uuid

    def find_uuid(self, line):
        re_uuid = '\'([a-zA-Z0-9]{16,16})\''
        for m in re.finditer(re_uuid, line):
            i = m.group(1)
            if i in self.id_hash:
                continue
            self.id_hash[i] = self.uuid()
            

    def replace(self,line): 
        res = re.sub(str(100032), str(self.shop_id), line)
        res = re.sub(str(31), str(78), res)
        res = re.sub(str(32), str(79), res)
        res = re.sub(str(33), str(80), res)
        res = re.sub(u'会员', u'美味会员储值', res)
        res = re.sub(u'会员积分', u'美味会员积分', res)
        res = re.sub(u'会员赠金', u'美味会员赠金', res)
        res = re.sub('\\d{4,4}\\-\\d{2,2}\\-\\d{2,2}\\s+\\d{2,2}:\\d{2,2}:\\d{2,2}\\.\\d{6,6}', self.cur_time, res)
        '''replace id'''
        for k,v in self.id_hash.items():
            res = re.sub(k, v, res)
        return res            
    
    def clone(self,fp):
        f = open(fp, 'r')
        fo = open( './' + str(self.shop_id) + '_mw_paymethod.sql', 'w')
        resLines = []
        try:
            while True:
                line = f.readline()
                if line:
                    self.find_uuid(line)
                    resLines.append(line)
                else:
                    break
            if len(resLines) > 0:
                for i in range(len(resLines)):
                    resLines[i] = self.replace(resLines[i])
                fo.writelines(resLines)
        except Exception as e:
            print('exception: ' + repr(e))
        finally:
            f.close()
            fo.close()
        return    
    
if __name__ == '__main__':
    p = ClonePaymethod(100281)
    p.clone(r'./pay_method.sql')