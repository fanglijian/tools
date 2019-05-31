# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 11:39:26 2018

@author: ljfang
"""
import requests
#import re
import json

def req_login_session(user, opt_code):
    url = 'https://portal.paadoo.net/otp/verify?exuid=' + user + '&code='+ opt_code
    rsp = requests.get(url)
    if None == rsp:
        print('Null respong when login')
        return None
    elif 200 != rsp.status_code:
        print('Failed:' + rsp.status_code + ' when login')
        return None
    try:
        data = json.loads(rsp.text)
        return data['data']['session']
    except:
        print('Json decode failed when login')
        return None

def req_restique( dbname, db_idx, sql, user = None, opt_code = None):
    if None == dbname or ('ali' != dbname and 'uc' != dbname):
        print('dbname must be ali or uc')
        return None
    
    if 'ali' == dbname:
        url_prefix = r'https://restique-ali.paadoo.net:32779'
        cookies_file = r'../restique/portal_cookies'
    else:
        url_prefix = r'https://restique.paadoo.net:32779'
        cookies_file = r'../restique/portal_cookies'
    isMain = db_idx == 'main'
    if db_idx == None or ( False == isMain and db_idx < 0) or sql == None or len(sql) == 0:
        print('Invalid sql for restique')
        return None
    if None == user or None == opt_code or len(user) == 0 or len(opt_code) == 0:
        with open(cookies_file, 'r', encoding="utf-8") as f:
            user = f.readline()
            sessions = opt_code = f.readline()
    else:
        sessions = req_login_session(user, opt_code)
        if sessions:
            with open(cookies_file, 'w', encoding="utf-8") as f:
                f.write(user + '\n' + sessions)
        else:
            print('Invalid restique session')
            return None

    if None == user or None == opt_code or len(user) == 0 or len(opt_code) == 0:
        print('Invalid user and opt_code for restique')
        return None
    sessions = 'OTPSESSION=' + sessions
    if (isMain):
        db = db_idx
    else:
        db = 'unit-sql-%02d' %db_idx
    data = {'use': db, 'sql': sql, 'result': 2}
    headers = {'Cookie': sessions}
    try:
        rsp = requests.post( url_prefix + r'/query?', data, headers = headers, timeout=5)
    except Exception:
        return None
    if None == rsp:
        return None
    #print(rsp.text)
    return rsp.text