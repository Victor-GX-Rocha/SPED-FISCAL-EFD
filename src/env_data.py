""" Carrega os dados do arquivo .env e os disponiliza em dataclasses """

import os
from src import log
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

def normalize_path(path: str) -> str:
    return str(path).strip().replace("'", "").replace('"', '')#.replace('\\', '\\\\')

@dataclass
class EnvData:
    efd_path: str = normalize_path(os.getenv('APP_PATH'))
    limite_espera: float = float(os.getenv('LIMITE_ESPERA')) if os.getenv('LIMITE_ESPERA') != None else None

@dataclass
class DestinyFolders:
    PROCESSADO: str = os.getenv('PASTA_PROCESSADO')
    ERRO: str = os.getenv('PASTA_ERRO')
