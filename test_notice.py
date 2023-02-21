from BrownieAtelierNotice.mail_send import mail_send
from BrownieAtelierNotice.mail_attach_send import mail_attach_send

# 件名、本文、添付ファイルなし。
mail_send('テスト','あああああ')

# 件名、本文、添付ファイルあり。
mail_attach_send(title='test', msg='手動で実行', filepath="BrownieAtelierNotice/test_notice.py")
