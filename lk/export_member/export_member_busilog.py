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

class Export_MemberBusiLog:
    
    def __init__(self, env, db_id, strShopIds, user = None, opt_code = None):
        self.env = env
        self.db_id = db_id
        self.strShopIds = strShopIds
        self.restique_user = user
        self.restique_optcode = opt_code
        self.shopNameMap = {}

    def getMemberTypeIds(self):
        sql = 'select id,shop_id,name,`range`,lan_mode from member_type where shop_id in (' + str(self.strShopIds) + ');'
        rep = restique.req_restique(self.env,self.db_id, sql, self.restique_user, self.restique_optcode)
        if None == rep or len(rep) == 0 or rep == 'null':
            print('No member_type from clound')
            return None
        jd = json.loads(rep)
        return jd
    
    def getChildShopIds(self, shop_id):
        sql = 'select distinct(child) as shop_id from shop_tree where parent=' + str(shop_id) + ';'
        rep = restique.req_restique(self.env,'main', sql, self.restique_user, self.restique_optcode)
        if None == rep or len(rep) == 0 or rep == 'null':
            print('None ShopTree')
            return None
        jd = json.loads(rep)
        strResult = None
        for item in jd:
            if None == strResult:
                strResult = str(item['shop_id'])
            else:
                strResult += ',' + str(item['shop_id'])
        return strResult
    
    def getShopName(self, shop_id):
        sid = (int)(shop_id)
        if sid in self.shopNameMap:
            return self.shopNameMap[sid]
        else:
            sql = 'select name from shop where id=' + str(sid) + ';'
            rep = restique.req_restique(self.env,'main', sql, self.restique_user, self.restique_optcode)
            if None == rep or len(rep) == 0 or rep == 'null':
                return str(sid)
            else:
                jd = json.loads(rep)
                if None == jd:
                    return str(sid)
                shopName = jd[0]['name']
                self.shopNameMap[sid] = shopName
                return shopName
            
    def export(self):
        if None == self.db_id or int(self.db_id) <= 0 :
            print('Invalid database id')
            return
        if None == self.strShopIds or len(self.strShopIds) <= 0 :
            print('Invalid shop_id')
            return
        memberTypeIds = self.getMemberTypeIds()
        if None == memberTypeIds:
            return
        for mbt in memberTypeIds:
            mbt_id = mbt['id']
            mbt_sid = mbt['shop_id']
            strShopIds = self.getChildShopIds(mbt_sid)
            if None == strShopIds:
                print('No child shop ids')
                return
            shopName = self.getShopName(mbt_sid)
            fileName = str(mbt_sid) + '_' + shopName + '_' + mbt['name']
            offset = 0
            sql0 = 'select left(ml.created,16) as created,m.number as number, m.member_mobile as member_mobile,m.member_name as member_name,' + \
            'm.state as state, ml.shop_id as busi_sid,ml.type as type,var_amt,var_amt_reward,var_score,amt_reward,' + \
            '(score_reward + gift_score_reward) as score_reward from member_busi_log as ml left join member as m on ml.member_id=m.id where ' + \
            'ml.member_id in (select id from member where shop_id in (' + strShopIds + ') and member_type_id=\'' + mbt_id + \
            '\' ) and ml.state in (0,2) order by ml.created limit '
            while True:
                sql = sql0 + str(offset) + ',5000;'
                rep = restique.req_restique(self.env,self.db_id, sql, self.restique_user, self.restique_optcode)
                if None == rep or len(rep) == 0 or rep == 'null':
                    print('No data from clound,mbt_id:' + str(mbt_id))
                    continue
                jd = json.loads(rep)
                if None == jd or len(jd) == 0:
                    break
                if not os.path.exists(r'./' + fileName):
                    os.mkdir(r'./' + fileName)
                self.write_excel(jd, r'./' + fileName + r'/' + fileName + '_' + str(offset) + '.xls')
                offset += len(jd)

    def save_file(self, file_name, jD):
        with codecs.open(file_name, 'w', encoding='utf-8') as f:
            f.write(json.dumps(jD, indent=4, ensure_ascii=False))

    def write_excel(self, jd, file_name):
        if None == jd:
            return
        wk = xlwt.Workbook(encoding = 'ascii')
        ws = wk.add_sheet(u'交易记录')        
        ws.write(0, 0, u'时`间')
        ws.write(0, 1, u'交易类型')
        ws.write(0, 2, u'会员卡号')
        ws.write(0, 3, u'会员电话')
        ws.write(0, 4, u'会员姓名')
        ws.write(0, 5, u'交易店铺ID')
        ws.write(0, 6, u'交易店铺名称')
        ws.write(0, 7, u'本金变化')
        ws.write(0, 8, u'赠金变化')
        ws.write(0, 9, u'奖励赠金')
        ws.write(0, 10, u'积分变化')
        ws.write(0, 11, u'奖励积分')
        
        row = 1
        for item in jd:
            created = item['created']
            number = item['number']
            member_mobile = item['member_mobile']
            #state = (int)(item['state'])
            member_name = item['member_name']
            busi_sid = item['busi_sid']
            busi_shopName = self.getShopName(busi_sid)
            busitype = self.strMbBusiType((int)(item['type']))
            var_amt = item['var_amt']
            var_amt_reward = item['var_amt_reward']
            var_score = item['var_score']
            amt_reward = item['amt_reward']
            score_reward = item['score_reward']
                         
            ws.write(row, 0, created)
            ws.write(row, 1, busitype)
            ws.write(row, 2, number)
            ws.write(row, 3, member_mobile)
            ws.write(row, 4, member_name)
            ws.write(row, 5, busi_sid)
            ws.write(row, 6, busi_shopName)
            ws.write(row, 7, var_amt)
            ws.write(row, 8, var_amt_reward)
            ws.write(row, 9, amt_reward)
            ws.write(row, 10, var_score)
            ws.write(row, 11, score_reward)
            row += 1
        wk.save(file_name)            
            
    def strMbBusiType(self,busitype):
        if 21 == busitype:
            return u'充值'
        elif 31 == busitype:
            return u'消费'
        elif 24 == busitype:
            return u'销卡'
        elif 22 == busitype:
            return u'续期'
        elif 25 == busitype:
            return u'退卡'
        elif 32 == busitype:
            return u'积分兑换'
        elif 33 == busitype:
            return u'挂账核销'
        else:
            return u'未知'        
        
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
    #strShopIds = '101563,101564,101801,104509,104510,104511,104512,104513,104514,104515,104744,105290,106841,107757,107861,108270,108283,108344,108345,108566,108567,108686'
    #strShopIds = '101802,104508,104516,104517,104518,104519,104520,104521,104543,104544'
    #strShopIds = '106385'
    #strShopIds = '107046'
    #strShopIds = '108849'
    strShopIds = '108850'
    p = Export_MemberBusiLog('uc', 4, strShopIds, user, opt_code)
    p.export()                     