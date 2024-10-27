from BrownieAtelierNotice.mail.mail_attach_send import mail_attach_send
from BrownieAtelierNotice.mail.mail_send import mail_send


if __name__ == "__main__":
    # 件名、本文、添付ファイルなし。
    mail_send("テスト", "あああああ")

    # 件名、本文、添付ファイルあり。
    mail_attach_send(
        title="test", msg="手動で実行", filepath="BrownieAtelierNotice/test_notice.py"
    )
