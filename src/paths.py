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


@dataclass
class ImgPaths:
    """ Um caminho direto e organizado para as imagens. """
    # mains
    tela_inicial: str = resource_path(r'imgs\tela_inicial.png')
    tela_inicial_validacao: str = resource_path(r'imgs\tela_inicial_validacao.png')
    erro: str = resource_path(r'imgs\erro.png')
    aviso: str = resource_path(r'imgs\aviso.png')
    info: str = resource_path(r'imgs\info.png')
    gray_bar: str = resource_path(r'imgs\gray_bar.png')
    sucesso: str = resource_path(r'imgs\sucesso.png')
    resultado_importacao: str = resource_path(r'imgs\resultado_importacao.png')
    loading_cancelar: str = resource_path(r'imgs\loading_cancelar.png')
    
    # Intermediárias
    relatorio_erros: str = resource_path(r'imgs\relatorio_erros.png')
    
    
    escrituracao_ja_existe: str = resource_path(r'imgs\Escrituracao-ja-existe.png')
    importacao_exito: str = resource_path(r'imgs\importacao exito.png')
    escrituracao_fiscal: str = resource_path(r'imgs\Escrituracao_fiscal.png')
    importacao_nao_realizada: str = r'imgs\importacao_nao_realizada.png'
    arquivo_nao_encontrado: str = resource_path(r'imgs\arquivo_nao_encontrado.png')
    arquivo_nao_encontrado2: str = resource_path(r'imgs\arquivo_nao_encontrado2.png')
    atualizar_tabelas: str = resource_path(r'imgs\atualizar_tabelas.png')
    validado_com_sucesso: str = resource_path(r'imgs\validado_com_sucesso.png')
    arquivo_contem_erros: str = resource_path(r'imgs\arquivo_contem_erros.png')
    pendencia_validacao: str = resource_path(r'imgs\pendencia_validacao.png')
    
    

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
