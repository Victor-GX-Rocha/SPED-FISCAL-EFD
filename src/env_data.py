""" Carrega os dados do arquivo .env e os disponiliza em dataclasses """

import os, sys
from src import log
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

def normalize_path(path: str) -> str:
    return str(path).strip().replace("'", "").replace('"', '')#.replace('\\', '\\\\')

def resource_path(relative_path: str) -> str:
    """Retorna o caminho absoluto para um recurso, baseado no diretório do executável (ou do script em desenvolvimento)."""
    if getattr(sys, 'frozen', False):
        # Estamos rodando como executável (PyInstaller)
        base_path = os.path.dirname(sys.executable)
    else:
        # Em desenvolvimento (script Python)
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

@dataclass
class EnvData:
    efd_path: str = resource_path(os.getenv('APP_PATH'))
    limite_espera: float = float(os.getenv('LIMITE_ESPERA')) if os.getenv('LIMITE_ESPERA') != None else None

@dataclass
class DestinyFolders:
    PROCESSADO: str = os.getenv('PASTA_PROCESSADO')
    ERRO: str = os.getenv('PASTA_ERRO')
