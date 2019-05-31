# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 11:36:27 2018

@author: user
"""

import sys 
import os
sys.path.append(os.path.abspath(r'G:\Programs\python\restique'))
import getopt
import json
import codecs
import xlwt
import restique

class Export_Member:
    
    def __init__(self, env, db_id, shop_id, user = None, opt_code = None):
        self.env = env
        self.db_id = db_id
        self.shop_Id = shop_id
        self.restique_user = user
        self.restique_optcode = opt_code
        
    def export(self):
        if None == self.db_id or int(self.db_id) <= 0 :
            print('Invalid database id')
            return
        if None == self.shop_Id or int(self.shop_Id) <= 0 :
            print('Invalid shop_id')
            return
        sql = 'select id,shop_id,number,identity,pledge,amount,reward_amt,cumu_score,create_time,expiry_date,member_type_id,member_name,\
        member_mobile,member_dob,member_sex,member_address,member_company,remark,state from member where shop_id=' + str(self.shop_Id) + \
        ' and deleted=0;'
        rep = restique.req_restique(self.env,self.db_id, sql, self.restique_user, self.restique_optcode)
        if None == rep or len(rep) == 0 or rep == 'null':
            print('No data from clound')
            return
        mb_type_hash = {}
        mb_type_shop_hash = {}
        jd = json.loads(rep)
        self.save_file('member', jd)        
        if None != jd:
            for i in range(len(jd)):
                mb_id = jd[i]['id']
                mbtype_id = jd[i]['member_type_id']
                mbtype_name = ''
                mbtype_shopid = jd[i]['shop_id']
                if mbtype_id in mb_type_hash:
                    mbtype_name = mb_type_hash[mbtype_id]
                    mbtype_shopid = mb_type_shop_hash[mbtype_id]
                else:
                    sql = 'select name,shop_id from member_type where id=\'' + mbtype_id + '\';';
                    rep = restique.req_restique(self.env, self.db_id, sql)
                    if None != rep and len(rep) > 4:
                        jMbType = json.loads(rep)
                        if None != jMbType and len(jMbType) > 0:
                            mbtype_name = jMbType[0]['name']
                            mbtype_shopid = jMbType[0]['shop_id']
                            mb_type_hash[mbtype_id] = mbtype_name
                            mb_type_shop_hash[mbtype_id] = mbtype_shopid
                jd[i]['member_type_name'] = mbtype_name
                jd[i]['member_type_shopid'] = mbtype_shopid
                
                mb_score = 0
                sql = 'select sum(score) as sc from member_score where member_id=\'' + mb_id + '\' and deleted=0 and (expiry_date=\'0000-00-00\' or \
                expiry_date>=\'2018-06-21\' or expiry_date is null);'
                rep = restique.req_restique(self.env, self.db_id, sql)
                if None != rep and len(rep) > 4:
                    jSc = json.loads(rep)
                    if None != jSc and len(jSc) > 0 and None != jSc[0]['sc']:
                        mb_score += float(jSc[0]['sc'])
                jd[i]['useable_score'] = mb_score
        self.write_excel(jd)


    def save_file(self, file_name, jD):
        with codecs.open(file_name, 'w', encoding='utf-8') as f:
            f.write(json.dumps(jD, indent=4, ensure_ascii=False))

    def write_excel(self, jd):
        if None == jd:
            return
        wk = xlwt.Workbook(encoding = 'ascii')
        ws = wk.add_sheet(u'会员')
        ws.write(0, 0, u'开卡店铺')
        ws.write(0, 1, u'会员类型所属店铺')
        ws.write(0, 2, u'会员类型')
        ws.write(0, 3, u'状态')
        ws.write(0, 4, u'姓名')
        ws.write(0, 5, u'卡号')
        ws.write(0, 6, u'手机号')
        ws.write(0, 7, u'物理卡ID')
        ws.write(0, 8, u'押金')
        ws.write(0, 9, u'本金余额')
        ws.write(0, 10, u'增金余额')
        ws.write(0, 11, u'可用积分')
        ws.write(0, 12, u'累计积分')
        ws.write(0, 13, u'开卡时间')
        ws.write(0, 14, u'过期日')
        ws.write(0, 15, u'性别')
        ws.write(0, 16, u'生日')
        ws.write(0, 17, u'地址')
        ws.write(0, 18, u'公司')
        ws.write(0, 19, u'备注')
        
        row = 1
        for item in jd:
            shop_id = item['shop_id']
            member_type_shopid = item['member_type_shopid']
            type_name = item['member_type_name']
            state = (int)(item['state'])
            member_name = item['member_name']
            number = item['number']
            member_mobile = item['member_mobile']
            identity = item['identity']
            pledge = item['pledge']
            amount = item['amount']
            reward_amt = item['reward_amt']
            useable_score = item['useable_score']
            cumu_score = item['cumu_score']
            create_time = item['create_time']
            expiry_date = item['expiry_date']
            member_sex = (int)(item['member_sex'])
            member_dob = item['member_dob']
            member_address = item['member_address']
            member_company = item['member_company']
            remark = item['remark']
            
            if -1 == state:
                state = u'开卡非活跃'
            elif 0 == state:
                state = u'活跃'
            elif 1 == state or 3 == state:
                state = u'已销卡'
            else:
                state = u'冻结'
            
            if 0 == member_sex:
                member_sex = u'男'
            elif 1 == member_sex:
                member_sex = u'女'
            else:
                member_sex=u'未知'
                
            if '0000-00-00' == expiry_date:
                expiry_date=''
            if '0000-00-00' == member_dob:
                member_dob=''               
            ws.write(row, 0, shop_id)
            ws.write(row, 1, member_type_shopid)
            ws.write(row, 2, type_name)
            ws.write(row, 3, state)
            ws.write(row, 4, member_name)
            ws.write(row, 5, number)
            ws.write(row, 6, member_mobile)
            ws.write(row, 7, identity)
            ws.write(row, 8, pledge)
            ws.write(row, 9, amount)
            ws.write(row, 10, reward_amt)
            ws.write(row, 11, useable_score)
            ws.write(row, 12, cumu_score)
            ws.write(row, 13, create_time)
            ws.write(row, 14, expiry_date)
            ws.write(row, 15, member_sex)
            ws.write(row, 16, member_dob)
            ws.write(row, 17, member_address)
            ws.write(row, 18, member_company)
            ws.write(row, 19, remark)
            row += 1
        wk.save(str(self.shop_Id) + '_member.xls')            
            
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
    
    p = Export_Member('uc', 19, 105036, user, opt_code)
    p.export()                     