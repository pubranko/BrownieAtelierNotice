import sys
import logging
from logging import Logger
from decouple import config, AutoConfig
# .envファイルが存在するパスを指定。実行時のカレントディレクトリに.envを配置している場合、以下の設定不要。
# config = AutoConfig(search_path="./shared")


# ロガー設定。
# 各モジュールではここで設定した「logger」が使用できます。
logger: Logger = logging.getLogger('BrownieAtelierNotice')
logger.setLevel(str(config('BROWNIE_ATELIER_NOTICE__LOG_LEVEL', default='INFO')))
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)
format='%(asctime)s %(levelname)s [%(name)s] : %(message)s'
datefmt='%Y-%m-%d %H:%M:%S'
handler.setFormatter(logging.Formatter(fmt=format, datefmt=datefmt))


# Emailで通知を行う場合、以下のサーバー・ポートなどの情報が必要となります。
BROWNIE_ATELIER_NOTICE__SMTP_HOST:str = str(config('BROWNIE_ATELIER_NOTICE__SMTP_HOST'))
BROWNIE_ATELIER_NOTICE__SMTP_PORT:int = int(config('BROWNIE_ATELIER_NOTICE__SMTP_PORT'))
BROWNIE_ATELIER_NOTICE__FROM_EMAIL:str = str(config('BROWNIE_ATELIER_NOTICE__FROM_EMAIL'))
BROWNIE_ATELIER_NOTICE__TO_EMAIL:str = str(config('BROWNIE_ATELIER_NOTICE__TO_EMAIL'))
BROWNIE_ATELIER_NOTICE__PASSWORD:str = str(config('BROWNIE_ATELIER_NOTICE__PASSWORD'))
BROWNIE_ATELIER_NOTICE__TIMEOUT_LIMIT:float = float(config('BROWNIE_ATELIER_NOTICE__TIMEOUT_LIMIT', default=60))
