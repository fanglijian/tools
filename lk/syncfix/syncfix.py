# -*- coding: utf-8 -*-
from sys import argv
import os
import xml.dom.minidom
import codecs
import warnings

path = argv[1]
out_f = './result.txt'

TYPE_ORDERS = 'orders'
TYPE_ONE_ORDER = 'one_order'
TYPE_ORDER_ITEM = 'order_item'
TYPE_PAYMENT = 'payment'
TYPE_ORDER_PAYMENT = 'order_payment'
TYPE_ORDER_DELIVERY = 'order_delivery'
TYPE_ORDER_DELIVERY_PROCESS = 'order_delivery_process'
TYPE_STAFF_PERFORMANCE = 'staff_performance'

# 定义一个排序level 让列表中的元素按照下面字段的level排序
level = {
    'orders': 1, 'one_order': 2, 'order_item': 3, 'payment': 4, 'order_payment': 5,
    'order_delivery': 6, 'order_delivery_process': 7, 'staff_performance': 8
}


def format_with_template(table_type, xml_file):
    tamp = open('./templates/' + table_type + '.temp', 'r').read()
    # print tamp
    rows_dic = {}
    # 打开xml文档
    dom = xml.dom.minidom.parse(xml_file)

    # 得到文档元素对象
    root = dom.documentElement

    rows = root.getElementsByTagName('row')
    for row in rows:
        fields = row.getElementsByTagName('field')
        for f in fields:
            if f.firstChild is not None:
                k = f.getAttribute('name')
                v = f.firstChild.data
                rows_dic[k] = v
            else:
                k = f.getAttribute('name')
                v = u''
                rows_dic[k] = v
                pass
            pass
        pass

        # print rows_dic
        out_text = tamp % rows_dic
        # 写入utf-8
        out_file = codecs.open(out_f, 'a', "utf-8")
        out_file.write(out_text)
        out_file.write(u'\ufeff')
        out_file.write('\r\n')
        out_file.close()

    pass


def format_data(fp):
    f_lev_dic = {}
    #os.system("rm -rf " + out_f)
    for f in os.listdir(fp):
        f_name = f.split('.')[0]
        if f_name in level.keys():
            f_lev_dic[level.get(f_name)] = f_name
            pass
        else:
            f_lev_dic[f_name] = 999  # 如果不在level中则排到最后
            warnings.warn("NOT SUPPORT %s, please add template and update level file!" % f_name)
            return
            pass
        pass
    print f_lev_dic
    for i in f_lev_dic.keys():
        n = f_lev_dic.get(i)
        format_with_template(str(n), os.path.join(path, str(n) + '.xml'))
        pass

    pass


if os.path.exists(path):
    format_data(path)
else:
    print "ERROR! PATH NOT EXIST!"
