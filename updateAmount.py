# -*- Codeing:UTF-8
# -*- Richard(410982635@qq.com)
# -*- 2018.08.09

import pymysql
from tqdm import *
from decimal import *

# 连接mySQL服务器
print('正在连接mySQL服务器……')
con = pymysql.connect(user='python', passwd='pythonpwd', charset='utf8')
print('服务器连接成功！')
cur = con.cursor()

# 计算还款历史表中还款本金合计，生成临时表
print('\r' + '正在查询还款历史表……')
sqlq = 'select loan_id,iou_id,sum(return_prin) from pai.repay_history group by loan_id, iou_id;'
cur.execute(sqlq)
repaylist = cur.fetchall()
print('\r' + '找到 %s 条统计记录。' % (len(repaylist)))

# 更新贷款协议表
print('\r' + '正在更新贷款协议表……')
for i in tqdm(range(0, len(repaylist))):
    loanid = repaylist[i][0]
    iouid = repaylist[i][1]
    returnprin = repaylist[i][2]
    sqlq = 'select loan_amount from pai.loan_agreement where loan_id = %s;'
    cur.execute(sqlq, (loanid))
    remamountlist = cur.fetchall()
    remamount = remamountlist[0][0]
    result = Decimal(remamount - returnprin).quantize(Decimal('0.00'))
    # print('\r' + '%s %s %s %s' % (loanid, returnprin, remamount, result))
    sqlu = 'update pai.loan_agreement set loan_remamount = %s where loan_id = %s;'
    cur.execute(sqlu, (result, loanid))
    con.commit()
print('\r' + '贷款协议表更新成功！')

# 更新贷款借据表
print('\r' + '正在更新贷款借据表……')
for i in tqdm(range(0, len(repaylist))):
    loanid = repaylist[i][0]
    iouid = repaylist[i][1]
    returnprin = repaylist[i][2]
    sqlq = 'select iou_amount from pai.loan_iou where loan_id = %s;'
    cur.execute(sqlq, (loanid))
    remamountlist = cur.fetchall()
    remamount = remamountlist[0][0]
    result = Decimal(remamount - returnprin).quantize(Decimal('0.00'))
    # print('\r' + '%s %s %s %s' % (loanid, returnprin, remamount, result))
    sqlu = 'update pai.loan_iou set iou_remamount = %s where loan_id = %s;'
    cur.execute(sqlu, (result, loanid))
    con.commit()
print('\r' + '贷款借据表更新成功！')
