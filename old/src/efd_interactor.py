""" Manages the interactions with goverment program  """

import pyautogui
import pygetwindow as gw
import time
import subprocess
import os
from src.logger import get_logger

logger = get_logger(__name__)

from dotenv import load_dotenv
load_dotenv()


from dataclasses import dataclass

@dataclass
class AppConfig:
    app_path: str = os.getenv('APP_PATH').strip().replace("'", "").replace('"', '').replace('\\', '/')



class EfdInterector:
    def __init__(self, app_config: AppConfig):
        self.app_path: str = app_config.app_path
    
    def open(self) -> None:
        """ Safely open the 'EFD - ICMS IPI' program """
        
        app_dir: str = os.path.dirname(self.app_path)
        subprocess.Popen([self.app_path], cwd=app_dir)
        
        # Aguarda a janela aparecer e a armazena
        self.window = self._find_window()
        if not self.window:
            logger.warning("Janela não encontrada pelo título, tentando fallback visual.")
            # Fallback: esperar o loading sumir mesmo sem a janela
        
        self.wait_for_loading_to_disappear()



    def wait_for_loading_to_disappear(self, timeout=60, check_interval=0.5):
        """
        Aguarda até que a tela de loading desapareça.
        Utiliza a imagem 'loading.png' para identificar a presença do loading.
        """
        region = None
        if self.window:
            # Define uma região com margem para evitar bordas
            region = (
                self.window.left + 10,
                self.window.top + 30,   # ignora barra de título
                self.window.width - 20,
                self.window.height - 40
            )
        
        time.sleep(2)
        # loading_image = os.path.join("imgs", "loading0.png")
        loading_image = r"C:\Users\Administrador\OneDrive\12-PROJECTS\SPED-FISCAL-EFD-2\imgs\Captura de tela 2026-07-04 203722 copy.png"
        start = time.time()
        while time.time() - start < timeout:
            # Procura a imagem do loading na tela toda (ou em uma região específica)
            # Podemos limitar a região se soubermos onde a janela costuma aparecer,
            # mas por enquanto vamos buscar na tela inteira.
            if not pyautogui.locateOnScreen(loading_image, confidence=0.8):
                logger.info("Tela de loading não está mais visível.")
                # Pequena pausa extra para garantir que a janela principal se estabilize
                time.sleep(2)
                return True
            time.sleep(check_interval)
        raise TimeoutError("A tela de loading não desapareceu dentro do tempo limite.")

    def _find_window(self, title_substring="Sped Fiscal", timeout=30):
        """Encontra a janela que contém a substring no título."""
        start = time.time()
        while time.time() - start < timeout:
            windows = gw.getWindowsWithTitle(title_substring)
            # Filtra apenas janelas visíveis e que não são do navegador (ex: Edge)
            for w in windows:
                if w.visible and not w.title.startswith("Edge"):  # Ajuste conforme necessário
                    return w
            time.sleep(0.5)
        return None

if __name__ == '__main__':
    efd_interector = EfdInterector(AppConfig())
    efd_interector.open()
