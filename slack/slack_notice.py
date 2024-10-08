import os
from typing import Union
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from logging import Logger, LoggerAdapter
from BrownieAtelierNotice import settings

def slack_notice(
    logger:Union[Logger,LoggerAdapter],
    channel_id:str,
    message:str,
    file:Union[str, bytes] = "",
    file_name: str="",):
    """
    slackへ指定したチャンネルにメッセージを送信します。
    添付ファイルがある場合は、fileとfile_nameを設定してください。
    Args:
        channel_id (str): 送信先のチャンネルIDを指定
        message (str): 送信したいメッセージを指定
        file (Union[str, bytes], optional): 添付ファイルを送信する場合、そのファイルパスかファイルライクオブジェクトを指定
        file_name (str, optional): 添付ファイルを送信する場合、ファイル名を指定（メッセージ内に表示する名称＆実際に保存される名称）
    """

    def _files_upload_v2():
        """ファイルアップロード用"""
        try:
            # ファイルをアップロード
            response = client.files_upload_v2(
                channel=channel_id,
                file=file, # ファイルパスまたはファイルライクオブジェクト
                filename=file_name, # 添付されるファイル名
                title=file_name, # slackに表示されるファイル名
                initial_comment=message
            )
            assert response["ok"] == True
            logger.info(f"Slackへファイルアップロード完了")
        except SlackApiError as e:
            logger.error(f"Slackへファイルアップロード失敗: {e}")

    
    def _chat_postMessage():
        """メッセージ送信専用"""
        try:
            response = client.chat_postMessage(
                channel=channel_id,
                text=message
            )
            assert response["ok"] == True
            logger.info(f"Slackへメッセージ送信完了")
        except SlackApiError as e:
            logger.error(f"Slackへメッセージ送信失敗: {e}")



    client = WebClient(token=settings.BROWNIE_ATELIER_NOTICE__SLACK_TOKEN)

    # トークンが正しいか確認します
    try:
        auth_test = client.auth_test()
        # bot_user_id = auth_test["user_id"]
        assert auth_test["ok"] == True
        logger.info(f"Slack疎通確認: {auth_test['ok']}")
    except:
        logger.critical(f"slackへ接続できませんでした。トークンを確認してください。{auth_test}")

    if file:
        # 添付ファイルを送信する場合

        # ファイルパス指定の場合、ファイルの存在チェックを実施
        if type(file) == str:
            exists_checked:bool = os.path.exists(file)
            
            if exists_checked:
                # ファイルが存在する場合、添付ファイルとメッセージを送信
                _files_upload_v2()
            else:
                # エラー時はエラー用チャンネルに送信
                channel_id = settings.BROWNIE_ATELIER_NOTICE__SLACK_CHANNEL_ID__ERROR
                logger.error(f"slackへ送信したいファイルが存在しません。 file: {file}")
                message = "### 添付ファイルが存在しなかったためファイルの添付を中止 ###\n\n" + message
                _chat_postMessage()
        
        else:
            # ファイルライクオブジェクトの場合、そのまま送信
            _files_upload_v2()
    
    else:
        # 添付ファイルの指定がない場合メッセージを送信
        _chat_postMessage()
