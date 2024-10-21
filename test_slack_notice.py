import logging
from logging import Logger
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from shared.settings import DATA
from BrownieAtelierNotice import settings
from BrownieAtelierNotice.slack.slack_notice import slack_notice
from datetime import datetime


def slack_notice_test():
    client = WebClient(token=settings.BROWNIE_ATELIER_NOTICE__SLACK_TOKEN)

    # トークンが正しいか確認します
    auth_test = client.auth_test()
    # bot_user_id = auth_test["user_id"]
    print(f"疎通確認OK: {auth_test}")


    # メッセージの送信のみ
    text = "て～～すと"
    try:
        response = client.chat_postMessage(
            channel=settings.BROWNIE_ATELIER_NOTICE__SLACK_CHANNEL_ID__ERROR,
            text=text
        )
        print(f"post message: {response}")
        assert response["message"]["text"] == text
    except SlackApiError as e:
        print(f"Error sending message: {e}")

    # ファイルライクオブジェクトを渡すことも可能
    # ファイルのパスで渡すことも可能(相対パス・絶対パス)
    with open(f"{DATA}/scraper_pattern_analysis_report.xlsx", "rb") as f:
        file_like = f.read()
    file_name = f.name
    print(f"file type {type(file_like)}")

    # file_like = f"{DATA}/debug/start_urls(asahi_com_sitemap).txt"
    # file_name = "start_urls(asahi_com_sitemap).txt"

    # 添付ファイルを送信
    try:
        # ファイルをアップロード
        response = client.files_upload_v2(
            channel=settings.BROWNIE_ATELIER_NOTICE__SLACK_CHANNEL_ID__ERROR,
            file=file_like,
            filename=file_name,
            title='添付ファイルのファイル名として表示される名称',   # これを指定しないとファイルのフルパスが表示される。
            initial_comment='添付ファイルと一緒に送信するメッセージがあればここに記述'
        )
        # print(f"File uploaded: {response['file']['id']}")
        print(f"File uploaded: {response['ok']}")
        assert response['ok'] == True
    except SlackApiError as e:
        print(f"Error uploading file: {e}")

if __name__ == "__main__":

    # 上記の接続実験ソース
    # slack_notice_test()
    
    # 以下正式なモジュールのテスト用
    logger: Logger = logging.getLogger("prefect")
    logger.setLevel(logging.DEBUG)  # ログレベルをDEBUGに設定
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # テスト１
    slack_notice(
        logger=logger,
        channel_id=settings.BROWNIE_ATELIER_NOTICE__SLACK_CHANNEL_ID__ERROR,
        message=f"1. slack_noticeメソッド(添付なし)のてすとーーーー！ {datetime.now().isoformat()}",
    )

    # テスト２
    file_path = f"{DATA}/scraper_pattern_analysis_report.xlsx"
    file_name = "ファイル名"
    slack_notice(
        logger=logger,
        channel_id=settings.BROWNIE_ATELIER_NOTICE__SLACK_CHANNEL_ID__ERROR,
        message=f"2. slack_noticeメソッド(ファイルパス)のてすとーーーー！ {datetime.now().isoformat()}",
        file=file_path,
        file_name=file_name,
    )

    # テスト３
    with open(file_path, "rb") as f:
        file_like = f.read()
        file_name = f.name

    slack_notice(
        logger=logger,
        channel_id=settings.BROWNIE_ATELIER_NOTICE__SLACK_CHANNEL_ID__ERROR,
        message=f"3. slack_noticeメソッド(ファイル・添付あり)のてすとーーーー！ {datetime.now().isoformat()}",
        file=file_like,
        file_name=file_name,
    )

    import io
    _ = "ファイルライクオブジェクト！！！"
    file_like = io.BytesIO(_.encode("utf-8"))

    slack_notice(
        logger=logger,
        channel_id=settings.BROWNIE_ATELIER_NOTICE__SLACK_CHANNEL_ID__ERROR,
        message=f"4. slack_noticeメソッド(ファイルライク・添付あり)のてすとーーーー！ {datetime.now().isoformat()}",
        file=file_like.read(),
        file_name="file_like.txt",
    )
