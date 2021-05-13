import requests
from bs4 import BeautifulSoup
import threading

import smtplib
from email.mime.text import MIMEText

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--coin_name", type=str, default='ethereum', help='Coin Object')
parser.add_argument("--in_price", type=float, default=3827.0, help='Purchase Price')
parser.add_argument("--bound", type=float, default=0.5, help='Range Rate: [(Now - IN) / IN] should less than bound, '
                                                             'otherwise alarm by email')
parser.add_argument("--update_interval", default=10, type=float, help='Time between each two update')
parser.add_argument("--mail_user", type=str, default='xxx', help='sender email username')
parser.add_argument("--mail_pass", type=str, default='xxx', help='sender email password')
parser.add_argument("--sender", type=str, default='xxx@qq.com', help='sender email address')
parser.add_argument("--receivers", type=str, default='xxx@qq.com', help='receiver email address')
args = parser.parse_args()

url = "https://www.feixiaohao.com/currencies/" + args.coin_name

alarm_key = False

RECEIVERS = [address.strip() for address in args.receivers.split(',')]


def send_Abnormal(buy, now, range):
    # 设置服务器所需信息
    # qq邮箱服务器地址
    mail_host = 'smtp.qq.com'
    # qq用户名
    mail_user = args.mail_user
    # 密码(部分邮箱为授权码)
    mail_pass = args.mail_pass
    # 邮件发送方邮箱地址
    sender = args.sender
    # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
    receivers = RECEIVERS

    # 设置email信息
    # 邮件内容设置

    message = MIMEText('Coin: {}, Buy Price: {}, Now Price: {}, rate: {}'.format(args.coin_name, buy, now, range),
                       'plain', 'utf-8')
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


def coin_timer():
    global alarm_key

    strhtml = requests.get(url)
    soup = BeautifulSoup(strhtml.text, 'lxml')
    data = soup.select("#__layout > section > div.pageWrapper > div > div.PageLeftSide > div.box.coinInfoHeader > div.info > div.priceInfo > div:nth-child(2) > span:nth-child(1) > span")

    price = float(data[0].get_text())

    price_range = (price - args.in_price) / args.in_price
    print(price, args.in_price, price_range)
    if abs(price_range) > args.bound:
        if not alarm_key:
            send_Abnormal(args.in_price, price, price_range)
            alarm_key = True
    else:
        alarm_key = False

    global timer
    timer = threading.Timer(args.update_interval, coin_timer)
    timer.start()


if __name__ == "__main__":
    timer = threading.Timer(1, coin_timer)
    timer.start()
