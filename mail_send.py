import os
import smtplib
from typing import Optional,Union
from email import message
from logging import Logger,LoggerAdapter
from BrownieAtelierNotice import settings

# (参考情報)
# https://qiita.com/aj2727/items/81e5d67cbcbf7396e392
# Pythonでメールを送信（Outlook）

def mail_send(title: str, msg: str, param_logger: Optional[Union[Logger,LoggerAdapter]] = None) -> None:
    '''メール送信。件名(title)と本文(msg)を引数で渡す。'''

    if param_logger:
        logger = param_logger
    else:
        logger = settings.logger

    # 接続設定情報
    smtp_host = settings.BROWNIE_ATELIER_NOTICE__SMTP_HOST
    smtp_port = settings.BROWNIE_ATELIER_NOTICE__SMTP_PORT
    username = settings.BROWNIE_ATELIER_NOTICE__FROM_EMAIL
    password = settings.BROWNIE_ATELIER_NOTICE__PASSWORD
    to_email = settings.BROWNIE_ATELIER_NOTICE__TO_EMAIL
    from_email = settings.BROWNIE_ATELIER_NOTICE__FROM_EMAIL
    timeout_limit: float = settings.BROWNIE_ATELIER_NOTICE__TIMEOUT_LIMIT

    # メール作成
    mail = message.EmailMessage()
    mail.set_content(msg)  # 本文
    mail['Subject'] = title  # タイトル
    mail['From'] = from_email  # 送信元
    mail['To'] = to_email  # 送信先

    '''
    【メール送信】
    送信先ホスト、ポートを指定
    ehlo()でsmtpサーバーと今からやりとりしますよと呼んであげます。
    セキュアにするためにserver.starttls()と記述した後にもう一度server.ehlo()とします。
    次にホットメールでログインするための情報が聞かれるので、usernameとpasswordを記述します。
    ログインできたらsend_message()を使用して()の中に作成したメッセージ内容を入れます。
    一番最後にもうサーバーとやりとりしないので終了させるためにserver.quit()とします
    '''
    try:
        server = smtplib.SMTP(smtp_host, smtp_port, timeout=timeout_limit)
        # server.set_debuglevel(True) # デバックモードをONにしたい場合
        server.ehlo('mylowercasehost')  # smtp.office365.comに送る場合「mylowercasehost」の指定が必要らしい。
        server.starttls()
        server.ehlo('mylowercasehost')  # smtp.office365.comに送る場合「mylowercasehost」の指定が必要らしい。
        server.login(username, password)
        server.send_message(mail)
        server.quit()
    except Exception as e:
        logger.error(f'=== メール通知失敗({os.path.basename(__file__)}): {e}')
    else:
        logger.info(f'=== メール通知完了({os.path.basename(__file__)}): title = {title}')
