import pymysql
from tqdm import *

# 连接mySQL服务器
print('正在连接mySQL服务器……')
con = pymysql.connect(user='python', passwd='pythonpwd', charset='utf8')
print('服务器连接成功！')
cur = con.cursor()

# 计算还款历史表中还款本金合计，生成临时表
print('正在查询还款历史表……')
sqlq = 'select loan_id,iou_id,sum(return_prin) from pai.repay_history group by loan_id, iou_id;'
cur.execute(sqlq)
repaylist = cur.fetchall()
print('找到 %s 条统计记录。' % (len(repaylist)))

# 更新贷款协议表
print('\r' + '正在更新贷款协议表……')
for i in tqdm(range(0, len(repaylist))):
    loanid = repaylist[i][0]
    iouid = repaylist[i][1]
    returnprin = repaylist[i][2]
    sqlq = 'select loan_remamount from pai.loan_agreement where loan_id = %s;'
    cur.execute(sqlq, (loanid))
    remamountlist = cur.fetchall()
    remamount = remamountlist[0][0]
    result = round(remamount - returnprin, 2)
    print('\r' + '%s %s %s %s' % (loanid, returnprin, remamount, result))
    # print(cur.execute(sqlq,(loanid)))
    sqlu = 'update pai.loan_agreement set loan_remamount = %s where loan_id = %s;'
    # cur.execute(sqlu, (remamount - returnprin, loanid))

print('贷款协议表更新成功！')

# 更新贷款借据表
print('正在更新贷款借据表……')

print('贷款借据表更新成功！')
