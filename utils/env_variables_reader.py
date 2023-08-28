import os
from dotenv import load_dotenv


class EnvVariablesReader:
     def get_domain(path: str):
        load_dotenv(path)
        domain = os.getenv('DOMAIN')
        return domain
