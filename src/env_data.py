""" Carrega os dados do arquivo .env e os disponiliza em dataclasses """

import os
from src import log
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class EnvData:
    efd_path: str = str(os.getenv('APP_PATH')).strip().replace("'", "").replace("\\", "/")

