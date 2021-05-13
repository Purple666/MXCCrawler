# MXCCrawler
## 1. main.py
通过爬虫从币价网站上爬取对象货币的价格
### 1.1 功能
- 定时监控功能，可设定`update_interval`控制监控间隔时间长短
- 邮件报警功能，若波动超出所设定的阈值`bound`，则通过`smtplib`模块发送警报邮件
### 1.2 参数输入
- 对象货币：`coin_name`
- 买入价：`in_price`
- 允许波动范围：`bound`
- 监控间隔时间：`update_interval`
- 发送邮箱用户名：`mail_user`
- 发送邮箱密码(验证码)：`mail_pass`
- 发送邮箱地址：`sender`
- 接收邮箱地址：`receivers`（多个邮箱之间可通过`,`分隔）
### 1.3 使用前提
- 需要发送邮箱提供`smtp`功能
- 需要提供发送邮箱开通`smtp`功能后所获取到的授权码。并且填入`mail_pass`

## 2. mxcAPI.py
通过`mxc`交易所提供的API接口获取货币信息
### 2.1 额外特性
使用`requests.get`从`mxc`提供的API接口获取数据，并且用`json()`进行解析