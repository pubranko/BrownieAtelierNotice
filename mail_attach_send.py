import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from logging import Logger, LoggerAdapter
from typing import Optional, TypeVar, Union

from BrownieAtelierNotice import settings


def mail_attach_send(
    title: str,
    msg: str,
    filepath: str,
    param_logger: Optional[Union[Logger, LoggerAdapter]] = None,
) -> None:
    """添付ファイル付きメールの送信"""
    if param_logger:
        logger = param_logger
    else:
        logger = settings.logger

    smtp_host = settings.BROWNIE_ATELIER_NOTICE__SMTP_HOST
    smtp_port = settings.BROWNIE_ATELIER_NOTICE__SMTP_PORT
    username = settings.BROWNIE_ATELIER_NOTICE__FROM_EMAIL
    password = settings.BROWNIE_ATELIER_NOTICE__PASSWORD
    to_email = settings.BROWNIE_ATELIER_NOTICE__TO_EMAIL
    from_email = settings.BROWNIE_ATELIER_NOTICE__FROM_EMAIL
    timeout_limit: float = settings.BROWNIE_ATELIER_NOTICE__TIMEOUT_LIMIT

    mail = MIMEMultipart()
    mail["Subject"] = title
    mail["From"] = from_email
    mail["To"] = to_email
    mail.attach(MIMEText(msg, "html"))

    with open(filepath, "rb") as f:
        mb = MIMEApplication(f.read())

    mb.add_header("Content-Disposition", "attachment", filename=filepath)
    mail.attach(mb)

    try:
        server = smtplib.SMTP(smtp_host, smtp_port, timeout=timeout_limit)
        # server.set_debuglevel(True) # デバックモードをONにしたい場合
        server.ehlo(
            "mylowercasehost"
        )  # smtp.office365.comに送る場合「mylowercasehost」の指定が必要らしい。
        server.starttls()
        server.ehlo(
            "mylowercasehost"
        )  # smtp.office365.comに送る場合「mylowercasehost」の指定が必要らしい。
        server.login(username, password)
        server.send_message(mail)
        server.quit()
    except Exception as e:
        logger.error(f"=== メール通知失敗({os.path.basename(__file__)}): {e}")
    else:
        logger.info(f"=== メール通知完了({os.path.basename(__file__)}): title = {title}")
