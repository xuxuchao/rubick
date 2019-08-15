import sys;sys.path.append('..')
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

from utils.config import PROJECT_ROOT, Config
from utils.log import logging, log_action


@log_action
def get_last_report():
    config = Config()
    report_config = config.get_report_config()
    report_dir = os.path.join(PROJECT_ROOT, report_config.get("report_dir") or 'report')
    lists = os.listdir(report_dir)

    lists.sort(key=lambda fn: os.path.getmtime(os.path.join(report_dir, fn)))
    report_file = os.path.join(report_dir, lists[-1])
    return report_file


@log_action
def send_email(report_file=''):
    report_file = report_file or get_last_report()
    config = Config()
    email_config = config.get_email_config()
    smtp_server = email_config.get("smtp_server") or 'mail.163.com'
    smtp_user = email_config.get('smtp_user') or 'ivan-me@163.com'
    smtp_password = email_config.get('smtp_password') or 'hanzhichao123'
    subject = email_config.get('subject') or 'Test Report'
    body = email_config.get('body') or 'hi, all<br>Test complete, please see the attachments'
    receivers = email_config.get('receivers')

    msg = MIMEMultipart()
    msg.attach(MIMEText(body, 'html', 'utf-8'))

    msg['From'] = smtp_user
    msg['To'] = ''
    msg['Subject'] = Header(subject, 'utf-8')

    att1 = MIMEText(open(report_file, 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename="{}"'.format(os.path.basename(report_file))
    msg.attach(att1)

    try:
        logging.debug("连接SMTP服务器: {}".format(smtp_server))
        smtp = smtplib.SMTP(smtp_server)  # 从配置文件中读取
        logging.debug("登录SMTP服务器 用户名: {} 密码: {}".format(smtp_user, smtp_password))
        smtp.login(smtp_user, smtp_password)  # 从配置文件中读取
        for receiver in receivers:
            msg['To'] = receiver
            logging.debug("由{}发送邮件给: {}".format(smtp_user, receiver))
            smtp.sendmail(smtp_user, receiver, msg.as_string())
        logging.info("邮件发送完成！")
    except Exception as e:
        logging.error(str(e))
    finally:
        smtp.quit()


if __name__ == "__main__":
    print(get_last_report())
    send_email()


