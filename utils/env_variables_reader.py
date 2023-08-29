import os
from dotenv import load_dotenv


class EnvVariablesReader:
     def get_app_base_url(path: str):
        load_dotenv(path)
        app_base_url = os.getenv('APP_BASE_URL')
        return app_base_url
