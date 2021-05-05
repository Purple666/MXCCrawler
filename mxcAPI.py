import requests
import threading

import smtplib
from email.mime.text import MIMEText

Coin = 'TLM_USDT'
url = 'https://www.mxc.com/open/api/v2/market/ticker?symbol=' + Coin

RMB_NOW = '2443.94'

IN_PRICE = 0.6672
OUT_PRICE = 0.68
ALARM_KEY = False


def send_remind(buy, now, range):
    # 设置服务器所需信息
    # qq邮箱服务器地址
    mail_host = 'smtp.qq.com'
    # qq用户名
    mail_user = '616562636'
    # 密码(部分邮箱为授权码)
    mail_pass = 'mwbojqlmxyfobcdi'
    # 邮件发送方邮箱地址
    sender = '616562636@qq.com'
    # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
    receivers = ['616562636@qq.com']

    # 设置email信息
    # 邮件内容设置

    message = MIMEText('Buy Price: {}, Now Price: {}, rate: {}%'.format(buy, now, range), 'plain', 'utf-8')
    # 邮件主题
    message['Subject'] = 'Price Abnormal'
    # 发送方信息
    message['From'] = sender
    # 接受方信息
    message['To'] = receivers[0]

    # 登录并发送邮件
    try:
        # 连接到服务器
        smtpObj = smtplib.SMTP_SSL(mail_host)
        # 登录到服务器
        smtpObj.login(mail_user, mail_pass)
        # 发送
        smtpObj.sendmail(
            sender, receivers, message.as_string())
        # 退出
        smtpObj.quit()
        print('success')
    except smtplib.SMTPException as e:
        print('error', e)  # 打印错误


def fun_timer():
    import time
    r = requests.get(url)
    response_dict = r.json()['data'][0]
    time = time.strftime("%Y/%m/%d/%H:%M:%S", time.localtime(response_dict['time'] // 1000))
    print("Time: {} Coin: {}, IN: {}, Target: {}, Deal: {}, Rate: {}".format(time, response_dict['symbol'], IN_PRICE,
                                                                             OUT_PRICE, response_dict['last'],
                                                                             (float(response_dict['last']) - IN_PRICE) / IN_PRICE * 100))

    global ALARM_KEY
    if (float(response_dict['last']) - OUT_PRICE) / float(response_dict['last']) < -0.04:
        if ALARM_KEY == False:
            send_remind(IN_PRICE, float(response_dict['last']), (float(response_dict['last']) - IN_PRICE) / IN_PRICE * 100)
            ALARM_KEY = True
    else:
        ALARM_KEY = False

    global timer
    timer = threading.Timer(1, fun_timer)
    timer.start()


timer = threading.Timer(1, fun_timer)
timer.start()