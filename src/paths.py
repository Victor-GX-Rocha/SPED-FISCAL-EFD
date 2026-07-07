import os
import time
import shutil
import pyautogui as pag
from dataclasses import dataclass

from src.env_data import DestinyFolders

pag.FAILSAFE = True


def normalize_path(path: str) -> str:
    """  """
    return path.strip().replace("'", "").replace('"', '').replace('\\', '/')


@dataclass
class ImgPaths:
    """ Um caminho direto e organizado para as imagens. """
    tela_inicial: str = normalize_path(r'imgs\tela_inicial.png')
    escrituracao_ja_existe: str = normalize_path(r'imgs\Escrituracao-ja-existe.png')
    importacao_exito: str = normalize_path(r'C:\Users\Administrador\OneDrive\12-PROJECTS\SPED-FISCAL-EFD-2\imgs\importacao exito.png')
    escrituracao_fiscal: str = normalize_path(r'C:\Users\Administrador\OneDrive\12-PROJECTS\SPED-FISCAL-EFD-2\imgs\Escrituracao_fiscal.png')
    importacao_nao_realizada: str = r'C:\Users\Administrador\OneDrive\12-PROJECTS\SPED-FISCAL-EFD-2\imgs\importacao_nao_realizada.png'
    arquivo_nao_encontrado: str = normalize_path(r'C:\Users\Administrador\OneDrive\12-PROJECTS\SPED-FISCAL-EFD-2\imgs\arquivo_nao_encontrado.png')
    arquivo_nao_encontrado2: str = normalize_path(r'C:\Users\Administrador\OneDrive\12-PROJECTS\SPED-FISCAL-EFD-2\imgs\arquivo_nao_encontrado2.png')
    atualizar_tabelas: str = normalize_path(r'C:\Users\Administrador\OneDrive\12-PROJECTS\SPED-FISCAL-EFD-2\imgs\atualizar_tabelas.png')
    validado_com_sucesso: str = normalize_path(r'C:\Users\Administrador\OneDrive\12-PROJECTS\SPED-FISCAL-EFD-2\imgs\validado_com_sucesso.png')
    erro: str = normalize_path(r'imgs\erro.png')

def mover_arquivo(file_path: str, dest_dir: DestinyFolders):
    """Move o arquivo para o diretório de destino (processado ou erro)."""
    try:
        
        os.makedirs(dest_dir, exist_ok=True)
        filename: str = os.path.basename(file_path)
        dest_path: str = os.path.join(dest_dir, filename)
        
        # Evitar sobrescrita: adicionar timestamp se o arquivo já existir
        if os.path.exists(dest_path):
            base, ext = os.path.splitext(file_path)
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            new_name = f"{base}_{timestamp}{ext}"
            dest_path = os.path.join(dest_dir, new_name)
        
        # print(dest_path, dest_dir)
        destino: str = shutil.move(file_path, dest_path)
        print(f"Arquivo movido para {destino}")
        # logger.info(f"Arquivo movido para {file_path}")
    except Exception as e:
        print(f"Falha ao mover {file_path}: {e}")
        # logger.exception(f"Falha ao mover {file_path}: {e}")
        raise

__all__ = [
    "ImgPaths",
    "mover_arquivo"
]
