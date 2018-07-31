创建面向银行零售信贷业务风险建模时使用的基础数据，
包括：1.个人客户信息，2.贷款协议，3.贷款借据，4.还款计划，5.还款历史，6.贷款违约

1.个人客户信息-customer_info
    客户编号,cus_id,char(12);
    客户姓名,cus_name,char(20);
    证件类型,id_type,char(1); 0-居民身份证
    证件号码,id_num,char(20);
    出生日期,cus_brith,date;
    客户性别,cus_gender,char(1); 0-男/1-女
    婚姻状况,mar_status,char(1); 0-已婚/1-未婚/2-其他
    教育程度,edu_level,char(1); 0-初中及以下/1-高中/2-大学/3-硕士研究生/4-博士研究生
    客户职业,occ_type,char(2); 0-公务员/1-事业员工/2-金融员工/3-公司职员/4-军人/5-学生/6-自由职业/7-其他
    联系电话,cus_phone,char(20);
    电子邮件,cus_email,char(30);
    居住类型,live_type,char(1); 0-自有无贷款/1-自有有贷款/2-租赁/3-宿舍/4-其他
    居住地址,cus_address,char(100);
    银行卡号,cus_cardno,char(20);
    开户银行,cus_bank,char(100);
    卡种代码,card_typecode,char(2); 1-借记卡/2-贷记卡/3-准贷记卡/4-预付费卡
    卡种名称,card_typename,char(20);
    创建机构,cre_branch,char(10);
    创建柜员,cre_teller,char(10);
    创建日期,cre_date,date;
    创建时间,cre_time,time;

2.贷款协议-loan_agreement
    客户编号,cus_id,char(12);
    协议编号,loan_id,chr(12);
    产品名称,loan_name,char(100);
    贷款用途,loan_used,char(100);
    贷款金额,loan_amount,float(12,2);
    贷款币种,loan_currency,char(3); 001-人民币
    剩余本金,loan_remamount,float(12,2);
    贷款利率,loan_rate,float(6,4);
    贷款期限,loan_term,char(5);
    期限单位,term_unit,char(1); 0-天/1-月/2-季/3-年
    担保方式,iou_guaran,char(1); 0-信用/1-抵押/2-质押/3-保证
    生效日期,loan_effdate,date;
    到期日期,loan_duedate,date;
    还款卡号,repay_cardno,char(20);
    贷款机构,loan_branch,char(10);
    贷款状态,loan_stat,char(1); 0-正常/1-结清/2-逾期/3-其他

3.贷款借据-loan_iou
    协议编号,loan_id,chr(12);
    借据编号,iou_id,char(3);
    借据金额,iou_amount,float(12,2);
    借据币种,iou_currency,char(3); 001-人民币
    剩余本金,iou_remamount,float(12,2);
    借据利率,iou_rate,float(6,4);
    还款方式,iou_method,char(1); 0-等额本息/1-等额本金/2-先息后本
    还款顺序,repay_order,char(1); 0-费用_利息_本金/1-本金_利息_费用
    罚息利率,def_rate,float(6,4);
    提前还款标志,prepay_flag,char(1); 0-允许/1-不允许
    提前还款费率,prepay_fee,float(6,4);
    展期标志,change_flag,char(1); 0-允许/1-不允许
    展期费率,change_fee,float(6,4);
    生效日期,iou_effdate,date;
    到期日期,iou_duedate,date;
    借据状态,iou_stat.char(1); 0-正常/1-结清/2-逾期/3-其他

4.还款计划-repay_plan
    协议编号,loan_id,chr(12);
    借据编号,iou_id,char(3);
    还款期数,repay_serial,char(5);
    应还日期,repay_date,date;
    应还利息,repay_int,float(12,4);
    应还本金,repay_prin,float(12,4);
    应还本息,repay_amount,float(12,4);
    还款标志,return_flag,char(1); 0-正常还款/1-部分还款/2-未还款

5.还款历史-repay_his
    协议编号,loan_id,chr(12);
    借据编号,iou_id,char(3);
    还款日期,return_date,date;
    还款期数,return_bill,char(5);
    还款金额,return_amount,float(12,2);
    实还利息,return_imt,float(12,2);
    实还本金,return_prin,flost(12,2);

6.贷款违约-loan_default
    协议编号,loan_id,chr(12);
    借据编号,iou_id,char(3);
    还款期数,repay_serial,char(5);
    欠还利息,def_int,float(12,2);
    欠还本金,def_ptin,float(12,2);
    欠款本息,def_amount,float(12,2);
