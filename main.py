import os
import time

starttime = time.time()
os.system('/usr/local/bin/python3 ./cre_customer_info.py')
os.system('/usr/local/bin/python3 ./cre_loan_agreement.py')
os.system('/usr/local/bin/python3 ./cre_loan_iou.py')
os.system('/usr/local/bin/python3 ./cre_repay_plan.py')
os.system('/usr/local/bin/python3 ./batch_repay.py')
os.system('/usr/local/bin/python3 ./cre_database.py')
os.system('/usr/local/bin/python3 ./Txt2mySQL.py')
os.system('/usr/local/bin/python3 ./updateAmount.py')
endtime = time.time()
inttime = int(endtime - starttime)
h = int(inttime / 3600)
sUp_h = inttime - 3600 * h
m = int(sUp_h / 60)
sUp_m = sUp_h - 60 * m
s = int(sUp_m)
print('\r' + '执行结束，累计用时 ' + ":".join(map(str, (h, '%02d' % m, '%02d' % s))))
