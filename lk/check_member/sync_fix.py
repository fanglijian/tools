# -*- coding: utf-8 -*-
"""
Created on Tue May  8 16:09:52 2018

@author: user
"""

import json

class SyncFix:
    
    fp = r'G:\Programs\python\check_member\sync_fix_res.txt'
    datas = {}
    updated = 0
    
    def __init__(self):
        
        try:
            with open(self.fp, 'r', encoding="utf-8") as f:
                d = f.read()
                if None != d:
                    try:
                        self.datas = json.loads(d)
                    except Exception:
                        print('json load error\n')
        except Exception as e:
            print(e)
            pass

    def save(self):
        if self.updated:
            with open(self.fp, 'w', encoding="utf-8") as f:
                f.write(json.dumps(self.datas))
            
    def add(self, db_idx, shop_id, tbl, item_id, props):
        if None == props or len(props) == 0 or None == shop_id or None == tbl:
            print('invalid parameters when call add of SyncFix\n')
            return
        idb = str(db_idx)
        sid = str(shop_id)
        if idb not in self.datas:
            self.datas[idb] = {}
        if sid not in self.datas[idb]:
            self.datas[idb][sid] = {}            
        if tbl not in self.datas[idb][sid]:
            self.datas[idb][sid][tbl]={}
        if 'upd' not in self.datas[idb][sid][tbl]:
            self.datas[idb][sid][tbl]['upd'] = {}
        if item_id not in self.datas[idb][sid][tbl]['upd']:
            self.datas[idb][sid][tbl]['upd'][item_id] = {}
        for k,v in props.items():
            self.datas[idb][sid][tbl]['upd'][item_id][str(k)] = str(v)
        
        if 0 == self.updated:
            self.updated = 1
            
    def to_fix_txt(self):
        if None == self.datas or len(self.datas) == 0:
            return
        for db_idx,sD in self.datas.items():
            print("\n\nshop_db:" + str(db_idx) + '\n\n')
            for sid,tbls in sD.items():
                print("\n\nshop_id:" + str(sid) + '\n')
                for tbl, opers in tbls.items():
                    for oper, items in opers.items():
                        if 'upd' == oper:
                            for item_id,props in items.items():
                                print( tbl + '.' + item_id )
                                for k,v in props.items():
                                    print('    ' + str(k) + '=' + str(v) )
                        elif 'ins' == oper:
                            for item_id,props in items.items():
                                print( tbl + '\n    id=' + item_id)
                                for k,v in props.items():
                                    print('    ' + str(k) + '=' + str(v) )
            print('\n\n')
    
    
if __name__ == '__main__':
    syncfix = SyncFix()
    syncfix.to_fix_txt()