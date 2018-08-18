# -*- Codeing:UTF-8
# -*- Richard(410982635@qq.com)
# -*- 2018.08.09

import os
import pymysql
from decimal import *
from xml.dom.minidom import *
from tqdm import *

# 读取数据库配置文件、连接mySQL服务器
PWD = os.getcwd()
cfgfile = PWD + '/Parameters/mysql_cfg.xml'
try:
    f1 = open(cfgfile)
    f1.close()
except FileNotFoundError:
    print("发现错误：数据库配置文件 \"%s\" 不存在！" % cfgfile)
    os._exit(0)
dom = parse(cfgfile)
cfglist = dom.documentElement
cfg_user = cfglist.getElementsByTagName('user')[0].firstChild.data
cfg_passwd = cfglist.getElementsByTagName('password')[0].firstChild.data
cfg_db = cfglist.getElementsByTagName('database')[0].firstChild.data
cfg_char = cfglist.getElementsByTagName('charset')[0].firstChild.data
print('正在连接mySQL服务器……')
con = pymysql.connect(user=cfg_user, passwd=cfg_passwd, db=cfg_db, charset=cfg_char)
print('服务器连接成功！')
cur = con.cursor()

# 计算还款历史表中还款本金合计，生成临时队列
print('\r' + '正在查询还款历史表……')
sqlq = 'select loan_id,iou_id,sum(return_prin) from pai.repay_history group by loan_id, iou_id;'
cur.execute(sqlq)
repaylist = cur.fetchall()
print('\r' + '找到 %s 条统计记录。' % (len(repaylist)))

# 更新贷款协议表还款数据
print('\r' + '正在更新贷款协议表中还款数据……')
for i in tqdm(range(0, len(repaylist))):
    loanid = repaylist[i][0]
    iouid = repaylist[i][1]
    returnprin = repaylist[i][2]
    sqlq = 'select loan_amount from pai.loan_agreement where loan_id=%s;'
    cur.execute(sqlq, (loanid))
    remamountlist = cur.fetchall()
    remamount = remamountlist[0][0]
    result = Decimal(remamount - returnprin).quantize(Decimal('0.00'))
    if result == 0.00:
        sqlu = 'update pai.loan_agreement set loan_remamount=%s,loan_status=1 where loan_id=%s;'
    else:
        sqlu = 'update pai.loan_agreement set loan_remamount=%s where loan_id=%s;'
    cur.execute(sqlu, (result, loanid))
    con.commit()
print('\r' + '贷款协议表更新成功！')

# 更新贷款借据表还款数据
print('\r' + '正在更新贷款借据表中还款数据……')
for i in tqdm(range(0, len(repaylist))):
    loanid = repaylist[i][0]
    iouid = repaylist[i][1]
    returnprin = repaylist[i][2]
    sqlq = 'select iou_amount from pai.loan_iou where loan_id=%s;'
    cur.execute(sqlq, (loanid))
    remamountlist = cur.fetchall()
    remamount = remamountlist[0][0]
    result = Decimal(remamount - returnprin).quantize(Decimal('0.00'))
    if result == 0.00:
        sqlu = 'update pai.loan_iou set iou_remamount=%s,iou_status=1 where loan_id=%s;'
    else:
        sqlu = 'update pai.loan_iou set iou_remamount=%s where loan_id=%s;'
    cur.execute(sqlu, (result, loanid))
    con.commit()
print('\r' + '贷款借据表更新成功！')

# 计算违约历史表中欠款期数、欠还利息、欠还本金、欠款合计，生成临时队列
print('\r' + '正在查询违约历史表……')
sqlq = 'select loan_id,iou_id,count(repay_serial),min(repay_serial),sum(def_int),sum(def_prin),sum(def_amount) from pai.loan_default group by loan_id,iou_id;'
cur.execute(sqlq)
deflist = cur.fetchall()
print('\r' + '找到 %s 条统计记录。' % (len(deflist)))

# 更新贷款协议表违约数据
print('\r' + '正在更新贷款协议表中违约数据……')
for i in tqdm(range(0, len(deflist))):
    loanid = deflist[i][0]
    iouid = deflist[i][1]
    sqlu = 'update pai.loan_agreement set loan_status=2 where loan_id=%s;'
    cur.execute(sqlu, (loanid))
    con.commit()
print('\r' + '贷款协议表更新成功！')

# 更新贷款借据表违约数据
print('\r' + '正在更新贷款借据表中违约数据……')
for i in tqdm(range(0, len(deflist))):
    loanid = deflist[i][0]
    iouid = deflist[i][1]
    defcount = deflist[i][2]
    defstart = deflist[i][3]
    defint = deflist[i][4]
    defprin = deflist[i][5]
    defamount = deflist[i][6]
    sqlu = 'update pai.loan_iou set iou_status=2,iou_defcount=%s,iou_defstart=%s,iou_defint=%s,iou_defprin=%s,iou_defamount=%s where loan_id=%s;'
    cur.execute(sqlu, (defcount, defstart, defint, defprin, defamount, loanid))
    con.commit()
print('\r' + '贷款借据表更新成功！')
