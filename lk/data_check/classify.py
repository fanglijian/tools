d# -*- coding: utf-8 -*-
"""
Created on Thu May 31 10:35:20 2018

@author: user
"""

import sys 
import os,os.path
sys.path.append(os.path.abspath(r'G:\Programs\python\restique'))
import json
#import restique
import getopt

class ClassifyCheckLog:
    
    def __init__(self, log_dir, opt_user = None, opt_code = None):
        self.log_dir = log_dir
        self.opt_user = opt_user
        self.opt_code = opt_code
    
    def classify_dup_payment(self):
        fp = self.log_dir + './orders_check__update_data_ERR_DUP_PAYMENT_TYPE.json'
        res = {}
        with open(fp, 'r', encoding="utf-8") as f:
            d = f.read()
            jD = json.loads(d)
            for db_iter in jD:
                jdata = db_iter['data']
                for jdata_iter in jdata:
                    total = round(float(jdata_iter['total']),2)
                    paid = round(float(jdata_iter['paid']),2)
                    if ',' not in jdata_iter['pay_method']:
                        pay_method = int(jdata_iter['pay_method'])
                    else:
                        pay_method_array = jdata_iter['pay_method'].split(",")
                        pay_method = None
                        for i in pay_method_array:
                            if None == pay_method:
                                pay_method = int(i)
                            elif int(i) != pay_method:
                                pay_method = 'mulPayMethod'
                                break
                    if paid != total * 2:
                        pay_method = 'notEqual'
                    if pay_method not in res:
                        res[pay_method] = []
                    res[pay_method].append(jdata_iter)
                    
        self.classify_by_type_src(res)
        for k,v in res.items():
            f = open(self.log_dir + r'./ERR_DUP_PAYMENT_TYPE_' + str(k), 'w', encoding="utf-8")
            f.write(json.dumps(v, indent=4))
            f.close()
 
    def classify_by_type_src(self,res):            
            for k,v in res.items():
                abstract = {}
                abstract['total'] = len(v)
                shops = []
                src = {}
                for item in v:
                    ot = int(item['order_type'])
                    if ot in src:
                        src[ot] = src[ot] + 1
                    else:
                        src[ot] = 1
                    if ot == 12:
                        subsrc = item['order_sub_src']
                        if subsrc in src:
                            src[subsrc] = src[subsrc] + 1
                        else:
                            src[subsrc] = 1
                    shop_id = item['shop_id']
                    if shop_id not in shops:
                        shops.append(shop_id)
                abstract['shop_count'] = len(shops)
                abstract['shops:'] = ','.join(shops)
                for src_k,src_v in src.items():
                    abstract[src_k] = src_v
                v.append(abstract)
            
    def classify_total_price(self):
        fp = self.log_dir + './orders_check__update_data_ERR_TOTAL_PRICE.json'
        res = {}
        with os.path.isfile(fp) and open(fp, 'r', encoding="utf-8") as f:
            d = f.read()
            jD = json.loads(d)
            for db_iter in jD:
                db_id = int(db_iter['db_id'].split("-")[-1])
                jdata = db_iter['data']
                for jdata_iter in jdata:
                    total = round(float(jdata_iter['total']),2)
                    final = 0
                    if 'final_sum' in jdata_iter and None != jdata_iter['final_sum']:
                        final = round(float(jdata_iter['final_sum']),2)
                    final_sub = 0;
                    if 'final_sub' in jdata_iter and None != jdata_iter['final_sub']:
                        final_sub = round(float(jdata_iter['final_sub']),2)
                    display = 0
                    if 'display_sum' in jdata_iter and None != jdata_iter['display_sum']:
                        display = round(float(jdata_iter['display_sum']),2)
                    paid = 0
                    if 'paid' in jdata_iter and None != jdata_iter['paid']:
                        paid = round(float(jdata_iter['paid']),2)
                    receivable = 0
                    if 'receivable' in jdata_iter and None != jdata_iter['receivable']:
                        receivable = round(float(jdata_iter['receivable']),2)
                    fr94_c = 0
                    if 'fr94' in jdata_iter and None != jdata_iter['fr94']:
                        fr94_c = int(jdata_iter['fr94'])
                    #fr94_p = float(jdata_iter['rf94_price'])
                    unit0_c = 0
                    if 'unit_0' in jdata_iter and None != jdata_iter['unit_0']:
                        unit0_c = int(jdata_iter['unit_0'])
                    #unit0_price = float(jdata_iter['unit0_price'])
                    class_type = 'NotClassify'
                    price_diff = None
                    if unit0_c > 0 :
                        class_type = 'unit0'
                    elif fr94_c > 1 :
                        class_type = 'fr94_' + str(fr94_c)
                    elif total != final:
                        class_type = 'final_sum'
                        price_diff = abs(total - final)
                    elif total != display:
                        class_type = 'display'
                        price_diff = abs(total - display)
                    elif total != final_sub:
                        class_type = 'final_sub'
                        price_diff = abs(total - final_sub)
                    elif total != paid:
                        class_type = 'paid'
                        if paid != 0 :
                            price_diff = abs(total - paid)
                    elif total != receivable:
                        class_type = 'receivable'
                        if receivable != 0:
                            price_diff = abs(total - receivable)    
                    if None != price_diff:
                        if price_diff > 1:
                            class_type = class_type + '_1'
                        elif price_diff < 0.05:
                            class_type = class_type + '_0.05'
                    if class_type not in res:
                        res[class_type] = []
                    jdata_iter['db_id'] = db_id
                    res[class_type].append(jdata_iter)
        self.classify_by_type_src(res)
        for k,v in res.items():
            f = open(self.log_dir + r'./ERR_TOTAL_PRICE_' + str(k), 'w', encoding="utf-8")
            f.write(json.dumps(v, indent=4))
            f.close()       

    def classify_date(self):
        fp = self.log_dir + './orders_check__update_data_ERR_ORDER_DATE.json'
        res = {}
        with open(fp, 'r', encoding="utf-8") as f:
            d = f.read()
            jD = json.loads(d)
            for db_iter in jD:
                db_id = int(db_iter['db_id'].split("-")[-1])
                jdata = db_iter['data']
                for jdata_iter in jdata:
                    order_type = int(jdata_iter['order_type'])
                    order_src = int(jdata_iter['order_src'])
                    order_sub_src = jdata_iter['order_sub_src']
                    date_msg = jdata_iter['date_msg:']
                    class_type = 'NotClassify'
                    if None != date_msg:
                        if 'order_date' in date_msg:
                            class_type = 'date_'
                        elif 'service_time_slot' in date_msg:
                            class_type = 'slot_'
                    if 20 == order_type or ( 12 == order_src and ('SwshmNvO' == order_sub_src or 'fKHF2MoE' == order_sub_src) ):
                        if None == jdata_iter['close_time']:
                            cal_time = 0
                            print('None close_time')
                            print(jdata_iter)
                        else:                            
                            cal_time = int(jdata_iter['create_time'])
                    else:
                        if None == jdata_iter['close_time']:
                            cal_time = 0
                            print('None close_time')
                            print(jdata_iter)
                        else:
                            cal_time = int(jdata_iter['close_time'])
                    cal_time = (cal_time + 28800) % 86400
                    if cal_time < 21600: 
                        class_type += '6am'
                    elif cal_time < 32400:
                        class_type += '9am'
                    elif cal_time < 39600:
                        class_type += '11am'
                    elif cal_time < 54000:
                        class_type += '3pm'
                    elif cal_time < 61200:
                        class_type += '5pm'
                    elif cal_time < 79200:
                        class_type += '10pm'
                    jdata_iter['db_id'] = db_id
                    if class_type not in res:
                        res[class_type] = []                    
                    res[class_type].append(jdata_iter)
        self.classify_by_type_src(res)
        for k,v in res.items():
            f = open(self.log_dir + r'./ERR_ORDER_DATE_' + str(k), 'w', encoding="utf-8")
            f.write(json.dumps(v, indent=4))
            f.close()          

    def base_abstract(self, file_list):
        for fname in file_list:
            fp = self.log_dir + './' + fname
            if not os.path.isfile(fp):
                continue
            outFname = fname.find('ERR_')
            if outFname > 0:
                dotPos = fname.find('.json')
                if dotPos > 0:
                    outFname = fname[outFname:dotPos]
                else:
                    outFname = fname[outFname:]
            else:
                outFname = fname
            res = {}
            res['all'] = [] 
            with open(fp, 'r', encoding="utf-8") as f:
                d = f.read()
                jD = json.loads(d)
                for db_iter in jD:
                    db_id = int(db_iter['db_id'].split("-")[-1])
                    jdata = db_iter['data']
                    for jdata_iter in jdata:
                        jdata_iter['db_id'] = db_id                  
                        res['all'].append(jdata_iter)
            self.classify_by_type_src(res)
            for k,v in res.items():
                f = open(self.log_dir + r'./' + outFname + '_' + str(k), 'w', encoding="utf-8")
                f.write(json.dumps(v, indent=4))
                f.close()              

def help():
    print("\nusage: python classify.py -u ljfang -c 12345678 date_dir -t [dupPayment price date abstract]\n") 
            

if __name__ == '__main__':
    user = None
    opt_code = None
    class_type = None
    args = None
    try:
        if len(sys.argv) > 1:
            opts,args = getopt.getopt(sys.argv[1:], "u:c:t:")
            for opt,arg in opts:
                if opt == '-u':
                    user = arg
                elif opt == '-c':
                    opt_code = arg
                elif opt == '-t':
                    class_type = arg
    except getopt.GetoptError:
        help()
        exit(2)

    p = ClassifyCheckLog(r'./20180613', user, opt_code)
    if 'dupPayment' == class_type:
        p.classify_dup_payment()
    elif 'price' == class_type:
        p.classify_total_price()
    elif 'date' == class_type:
        p.classify_date()
    elif 'abstract' == class_type:
        file = ['orders_check__update_data_ERR_ITEMS.json', 'orders_check__update_data_ERR_MEMBER_DATA.json', \
                'orders_check__update_data_ERR_ONE_ORDER.json', 'orders_check__update_data_ERR_PAYMENT.json', \
                'orders_check__update_data_ERR_PAYMENT_TIME.json', 'orders_check__update_data_ERR_BUSI_LOG.json',\
                'orders_check__update_data_ERR_ORDER_SRC_NULL']
        p.base_abstract(file)
    else:
        p.classify_dup_payment()
        p.classify_total_price()
        p.classify_date()
        file = ['orders_check__update_data_ERR_ITEMS.json', 'orders_check__update_data_ERR_MEMBER_DATA.json', \
                'orders_check__update_data_ERR_ONE_ORDER.json', 'orders_check__update_data_ERR_PAYMENT.json', \
                'orders_check__update_data_ERR_PAYMENT_TIME.json', 'orders_check__update_data_ERR_BUSI_LOG.json', \
                'orders_check__update_data_ERR_ORDER_SRC_NULL.json']
        p.base_abstract(file)            