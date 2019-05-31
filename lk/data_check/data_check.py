# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 18:40:17 2018

@author: user
"""
import os
import requests
import datetime
import re
import json

class Data_Check():
    
    def __init__(self):
        self.url = r'http://123.59.135.46:5338/'
        #self.log_date = datetime.date.today() + datetime.timedelta(days=-1)
        self.log_date = datetime.date.today()
        self.log_date = self.log_date.strftime("%Y%m%d")

    def downErrFiles(self):
        fp = r'./' + self.log_date
        if not os.path.exists(fp):
            os.mkdir(fp)
        log_id = self.getLogId()
        if None == log_id:
            print(' no log_id')
            return
        file_names = self.getERRFile(log_id)
        if None == file_names or len(file_names) == 0:
            print('no err files')
            return
        ErrPos = None
        class_statics = {}
        for fn in file_names:
            if None == ErrPos:
                ErrPos = re.search('ERR_', fn).start()
            err_type = fn[ErrPos:]
            url = self.url + self.log_date + r'/' + log_id + r'/' + fn + r'.json'
            rsp = self.download(url)
            if None == rsp:
                print('downlaod failed:' + url)
                continue
            verRes = self.classifyByVer(rsp)
            if None == verRes:
                continue
            for k,v in verRes.items():
                k = str(k)
                if k not in class_statics:
                    class_statics[k]={}
                    class_statics[k]['count'] = 0
                if err_type not in class_statics[k]:
                    class_statics[k][err_type] = 0
                c = len(v)
                class_statics[k]['count'] += c
                class_statics[k][err_type] += c
                vpath = fp + r'/' + k
                if not os.path.exists(vpath):
                    os.mkdir(vpath)
                path = vpath + r'/' + err_type
                with open(path, 'w', encoding="utf-8") as f:
                    f.write(json.dumps(v, indent=4))
        with open(fp + r'/' + 'statics.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(class_statics, indent=4))
   
    def classifyByVer(self, err_json):
        jD = None
        try:
            jD = json.loads(err_json)
        except Exception:
            print('parse json failed')
            return None
        res = {}
        for db_iter in jD:
            db_id = int(db_iter['db_id'].split("-")[-1])
            jData = db_iter['data']
            for jItem in jData:
                jItem['db_id'] = db_id
                ver = jItem['version']
                if ver not in res:
                    res[ver] = []
                res[ver].append(jItem)
        return res
        
    def getLogId(self):
        url = self.url + self.log_date
        rsp = self.download(url)
        if None == rsp:
            return None
        mat = re.search('>(0300\w+)/', str(rsp))
        if None != mat:
            return str(mat.group(1))
        return None

    def getERRFile(self, log_id):
        url = self.url + self.log_date + r'/' + log_id
        rsp = self.download(url)
        if None == rsp:
            return None
        mat = re.findall('>(orders_check__update_data_ERR_[^\.]+)\.', rsp)
        return mat
    
    def download(self, url):
        try:
            rsp = requests.get(url, None, headers = None, timeout=5)
            return rsp.text
        except Exception:
            return None
        return None          
     
        
if __name__ == '__main__':
    p = Data_Check()
    p.downErrFiles()