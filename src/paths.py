import os
import sys
import time
import shutil
import pyautogui as pag
from dataclasses import dataclass

from src.env_data import DestinyFolders

pag.FAILSAFE = True


def normalize_path(path: str) -> str:
    """  """
    return path.strip().replace("'", "").replace('"', '').replace('\\', '/')


def resource_path(relative_path: str) -> str:
    """Retorna o caminho absoluto para um recurso, baseado no diretório do executável (ou do script em desenvolvimento)."""
    if getattr(sys, 'frozen', False):
        # Estamos rodando como executável (PyInstaller)
        base_path = os.path.dirname(sys.executable)
    else:
        # Em desenvolvimento (script Python)
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent # sobe dois níveis (src/paths.py)
IMG_DIR = BASE_DIR / 'imgs'

@dataclass
class ImgPaths:
    """ Um caminho direto e organizado para as imagens. """
    # mains
    tela_inicial: str = str(IMG_DIR / 'tela_inicial.png')
    tela_inicial_validacao: str = str(IMG_DIR / 'tela_inicial_validacao.png')
    erro: str = str(IMG_DIR / 'erro.png')
    aviso: str = str(IMG_DIR / 'aviso.png')
    info: str = str(IMG_DIR / 'info.png')
    gray_bar: str = str(IMG_DIR / 'gray_bar.png')
    sucesso: str = str(IMG_DIR / 'sucesso.png')
    resultado_importacao: str = str(IMG_DIR / 'resultado_importacao.png')
    loading_cancelar: str = str(IMG_DIR / 'loading_cancelar.png')
    
    # Intermediárias
    relatorio_erros: str = str(IMG_DIR / 'relatorio_erros.png')
    
    
    escrituracao_ja_existe: str = str(IMG_DIR / 'Escrituracao-ja-existe.png')
    importacao_exito: str = str(IMG_DIR / 'importacao exito.png')
    escrituracao_fiscal: str = str(IMG_DIR / 'Escrituracao_fiscal.png')
    importacao_nao_realizada: str = str(IMG_DIR / 'importacao_nao_realizada.png')
    arquivo_nao_encontrado: str = str(IMG_DIR / 'arquivo_nao_encontrado.png')
    arquivo_nao_encontrado2: str = str(IMG_DIR / 'arquivo_nao_encontrado2.png')
    
    atualizar_tabelas: str = str(IMG_DIR / 'atualizar_tabelas.png')
    atualizar_tabelas_2: str = str(IMG_DIR / 'atualizar_tabelas_2.png')
    atualizar_tabelas_2_ok: str = str(IMG_DIR / 'atualizar_tabelas_2_ok.png')
    
    validado_com_sucesso: str = str(IMG_DIR / 'validado_com_sucesso.png')
    arquivo_contem_erros: str = str(IMG_DIR / 'arquivo_contem_erros.png')
    pendencia_validacao: str = str(IMG_DIR / 'pendencia_validacao.png')
    
    

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
