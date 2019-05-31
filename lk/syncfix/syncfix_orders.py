# -*- coding: utf-8 -*-
from sys import argv
import os
import xml.dom.minidom
import codecs

path = argv[1]
out_f = './result.txt'

TYPE_BOOK = 'book'
TYPE_ORDERS = 'orders'
TYPE_ONE_ORDER = 'one_order'
TYPE_ORDER_ITEM = 'order_item'
TYPE_PAYMENT = 'payment'
TYPE_ORDER_PAYMENT = 'order_payment'
TYPE_ORDER_DELIVERY = 'order_delivery'
TYPE_ORDER_DELIVERY_PROCESS = 'order_delivery_process'
TYPE_STAFF_PERFORMANCE = 'staff_performance'


def format_with_template(table_type, xml_file):
    tamp = open('./tamplates/' + table_type + '.tamp', 'r').read()
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
    os.system("rm -rf " + out_f)
    for f in os.listdir(fp):
        f_name = f.split('.')[0]

        if "orders" == f_name:
            format_with_template(TYPE_ORDERS, os.path.join(path, f))
        elif "one_order" == f_name:
            format_with_template(TYPE_ONE_ORDER, os.path.join(path, f))
        elif "order_item" == f_name:
            format_with_template(TYPE_ORDER_ITEM, os.path.join(path, f))
        elif "payment" == f_name:
            format_with_template(TYPE_PAYMENT, os.path.join(path, f))
        elif "order_payment" == f_name:
            format_with_template(TYPE_ORDER_PAYMENT, os.path.join(path, f))
        elif "order_delivery" == f_name:
            format_with_template(TYPE_ORDER_DELIVERY, os.path.join(path, f))
        elif "order_delivery_process" == f_name:
            format_with_template(TYPE_ORDER_DELIVERY_PROCESS, os.path.join(path, f))
        elif "staff_performance" == f_name:
            format_with_template(TYPE_STAFF_PERFORMANCE, os.path.join(path, f))
        else:
            print 'not support %' % f
    pass


if os.path.exists(path):
    format_data(path)
else:
    print "ERROR! PATH NOT EXIST!"
