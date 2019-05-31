# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 15:26:04 2018

@author: user
"""

import sys 
import os
import time
sys.path.append(os.path.abspath(r'G:\Programs\python\restique'))
import getopt
import json
import codecs
import xlwt
import xlrd
import restique

class ExportMemberUntilSomeDay:
    
    def __init__(self, db_id, memberType_id, date_time, user = None, opt_code = None):
        self.db_id = db_id
        self.memberType_id = memberType_id
        self.date_time = date_time
        self.restique_user = user
        self.restique_optcode = opt_code
    
    def export(self):
        self.export_member()
        self.export_amt_someday()
        
    def export_member(self):
        if None == self.db_id or int(self.db_id) <= 0 :
            print('Invalid database id')
            return
        if None == self.memberType_id or len(self.memberType_id) != 16 :
            print('Invalid member type id')
            return
        sDate = time.strftime('%Y-%m-%d', time.localtime(self.date_time))
        sql = 'select id,shop_id,number,identity,pledge,amount,reward_amt,cumu_score,member_name,\
        member_mobile,state from member where member_type_id=\'' + self.memberType_id + \
        '\' and left(create_time,10)<\'' + sDate + '\' and deleted=0;'
        rep = restique.req_restique(self.db_id, sql, self.restique_user, self.restique_optcode)
        if None == rep or len(rep) == 0 or rep == 'null':
            print('No data from clound')
            return
        jd = json.loads(rep)
        self.save_file('member_someday', jd)    
    
    def export_amt_someday(self):
        if os.path.exists('member_someday') == False:
            print('no file:member_someday')
            return
        result = []
        fp = 'member_someday'
        with open(fp, 'r', encoding="utf-8") as f:
            d = f.read()
            if None == d or len(d) == 0 :
                print('read no data from member_someday')
                return
            jD = json.loads(d)
            for db_iter in jD:
                mb_id = db_iter['id']
                curMb = {}
                curMb['id'] = mb_id
                curMb['number'] = db_iter['number']
                curMb['member_name'] = db_iter['member_name']
                curMb['member_mobile'] = db_iter['member_mobile']
                curMb['state'] = db_iter['state']
                curMb['amount'] = 0
                curMb['reward_amt'] = 0
                sql = 'select prev_amt,prev_amt_reward,prev_score from member_busi_log where member_id=\'' + mb_id + \
                '\' order by busi_time limit 1;'
                rep = restique.req_restique(self.db_id, sql)
                if None == rep or len(rep) == 0 or rep.startswith('null'):
                    curMb['amount'] = db_iter['amount']
                    curMb['reward_amt'] = db_iter['reward_amt']
                    result.append(curMb)
                    continue
                jd_busi = json.loads(rep)
                if None == jd_busi or len(jd_busi) != 1 or None == jd_busi[0] or None == jd_busi[0]['prev_amt']:
                    curMb['amount'] = db_iter['amount']
                    curMb['reward_amt'] = db_iter['reward_amt']
                    result.append(curMb)
                    continue
                curMb['amount'] = (float)(jd_busi[0]['prev_amt'])
                curMb['reward_amt'] = (float)(jd_busi[0]['prev_amt_reward'])
                
                sql = 'select sum(var_amt) as a, sum(var_amt_reward+amt_reward) as r from member_busi_log where member_id=\'' + mb_id + \
                '\' and state in (0,2) and busi_time<' + str(self.date_time) + ';'
                rep = restique.req_restique(self.db_id, sql)
                if None == rep or len(rep) == 0 or rep.startswith('null'):
                    print('get sum(var) failed')
                    return
                jd_busi = json.loads(rep)
                if None == jd_busi or len(jd_busi) != 1 or None == jd_busi[0] or None == jd_busi[0]['a']:
                    curMb['amount'] = db_iter['amount']
                    curMb['reward_amt'] = db_iter['reward_amt']
                    result.append(curMb)
                    continue                    
                var_a = (float)(jd_busi[0]['a'])
                var_r = (float)(jd_busi[0]['r'])
                
                sql = 'select sum(amt_reward) as r from member_busi_log where member_id=\'' + mb_id + \
                '\' and state=1 and busi_time<' + str(self.date_time) + ';'
                rep = restique.req_restique(self.db_id, sql)
                if None != rep and len(rep) > 0 and rep.startswith('null') == False:
                    jd_busi = json.loads(rep)
                    if None != jd_busi and len(jd_busi) > 0 and None != jd_busi[0] and None != jd_busi[0]['r']:
                        var_r -= (float)(jd_busi[0]['r'])
                    
                curMb['amount'] += var_a
                curMb['reward_amt'] += var_r
                result.append(curMb)
        self.write_excel(result)
    

    def save_file(self, file_name, jD):
        with codecs.open(file_name, 'w', encoding='utf-8') as f:
            f.write(json.dumps(jD, indent=4, ensure_ascii=False))

    def write_excel(self, jd):
        if None == jd:
            return
        wk = xlwt.Workbook(encoding = 'ascii')
        ws = wk.add_sheet(u'会员')
        ws.write(0, 0, u'卡号')
        ws.write(0, 1, u'开卡姓名')
        ws.write(0, 2, u'会员手机')
        ws.write(0, 3, u'剩余本金')
        ws.write(0, 4, u'剩余增金')
        ws.write(0, 5, u'剩余总金额')
        ws.write(0, 6, u'状态')
        
        row = 1
        for item in jd:
            state = (int)(item['state'])
            member_name = item['member_name']
            number = item['number']
            member_mobile = item['member_mobile']
            amount = "%.2f" %(float)(item['amount'])
            reward_amt = "%.2f" %(float)(item['reward_amt'])
            amt_all = "%.2f" %((float)(amount) + (float)(reward_amt))
            
            if -1 == state:
                state = u'开卡非活跃'
            elif 0 == state:
                state = u'活跃'
            elif 1 == state or 3 == state:
                state = u'已销卡'
            else:
                state = u'冻结'
        
            ws.write(row, 0, number)
            ws.write(row, 1, member_name)
            ws.write(row, 2, member_mobile)
            ws.write(row, 3, amount)
            ws.write(row, 4, reward_amt)
            ws.write(row, 5, amt_all)
            ws.write(row, 6, state)
            row += 1
        wk.save(str(self.memberType_id) + '_member_someday.xls')            

    def check(self):
        fp = str(self.memberType_id) + '_member_someday.xls'
        if os.path.exists(fp) == False:
            print('no file: member_someday')
            return
        data = xlrd.open_workbook(fp)
        table = data.sheets()[0]
        nrows = table.nrows
        for row in range(1,nrows):
            for col in range(3,6):
                v = (float)(table.cell(row,col).value)
                if v < 0 :
                    print('invalid value row:' + str(row) + " col:" + str(col))
         
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
        print('python export_member.py -u *** -c ********')
        exit(2)
    
    p = ExportMemberUntilSomeDay(19, '7F8irgwuMG1pqgUV', 1527782400, user, opt_code)
    #p.export()
    p.check()           
    