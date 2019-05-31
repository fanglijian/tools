1.连接hermes

2.进入数据库查询工具 

3.查询数据

4.导出数据

5.同级目录新建data文件夹,导出的csv数据放入data目录

6.修改csv文件为表名(订单相关的表不需要修改表名)

7.执行python脚本。python3执行 fixYc.py,  python2执行 fixYc2.py

8.查看output.txt 文件



订单查询sql

select * from orders where id in ("96zcwuFUH2r97dI1");
select * from one_order where order_id in ("96zcwuFUH2r97dI1");
select * from order_item where one_order_id in (select id from one_order where order_id in ("96zcwuFUH2r97dI1"));
select * from order_payment where one_order_id in (select id from one_order where order_id in ("96zcwuFUH2r97dI1"));
select * from payment where id in (select payment_id from order_payment where one_order_id in (select id from one_order where order_id in ("96zcwuFUH2r97dI1")));
select * from order_delivery where orders_id in ("96zcwuFUH2r97dI1");
select * from order_delivery_process where order_delivery_id=(select id from order_delivery where orders_id in ("96zcwuFUH2r97dI1"));
select * from staff_performance where object_Id in ("xX25VkVCkZUKmjKo","6mFp0QICanJUnSyp","nFOJf72M9AEgVvDI","mBGGfX4UrDPzxYfu","YOk4Ms95AO3zYKcQ","vSAo3rlZwWwTlbKp","vSAo3rlZwWwTlbKp") or object_Id in (select id from order_item where one_order_Id in (select id from one_order where order_id in ("96zcwuFUH2r97dI1"))) or object_Id in (select id from one_order where order_id in ("96zcwuFUH2r97dI1")) or object_Id in (select payment_id from order_payment where one_order_id in (select id from one_order where order_id in ("96zcwuFUH2r97dI1")));