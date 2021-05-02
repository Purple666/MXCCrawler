import requests
from bs4 import BeautifulSoup
import threading

import smtplib
from email.mime.text import MIMEText

in_price = 7.49
bound = 0.01

alarm_key = False

CoinName = "bakeryswap"
url = "https://m.feixiaohao.com/currencies/" + CoinName


def send_Abnormal(buy, now, range):
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

    message = MIMEText('Buy Price: {}, Now Price: {}, rate: {}'.format(buy, now, range), 'plain', 'utf-8')
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
    global alarm_key
    strhtml = requests.get(url)
    soup = BeautifulSoup(strhtml.text, 'lxml')
    data = soup.select("#__layout > div > div > div.main_page.main_page_inner.colorNum > div.coin_head > div > div.main_price.textGreen > div:nth-child(3) > span.price_usd > span")

    price = float(data[0].get_text())

    range = (price - in_price) / in_price
    print(price, in_price, range)
    if abs(range) > bound:
        if alarm_key == False:
            send_Abnormal(in_price, price, range)
            alarm_key = True
    else:
        alarm_key = False

    global timer
    timer = threading.Timer(20, fun_timer)
    timer.start()

timer = threading.Timer(1, fun_timer)
timer.start()