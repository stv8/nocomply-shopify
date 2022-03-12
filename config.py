from starlette.config import Config

config = Config(".env")


class AppConfig(object):
    SHOP_URL = config("SHOP_URL", default="")
    ACCESS_TOKEN = config("ACCESS_TOKEN", default="")

def get_config():
    return AppConfig