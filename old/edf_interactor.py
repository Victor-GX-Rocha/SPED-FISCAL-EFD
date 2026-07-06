""" Manages the interactions with goverment program  """

import subprocess
import os
from dotenv import load_dotenv

load_dotenv()
from dataclasses import dataclass

@dataclass
class AppConfig:
    app_path: str = os.getenv('APP_PATH').strip().replace("'", "").replace('"', '').replace('\\', '/')

import time

class EfdInterector:
    def __init__(self, app_config: AppConfig):
        self.app_path: str = app_config.app_path
    
    def open(self) -> None:
        """ Safely open the 'EFD - ICMS IPI' program """
        
        app_dir: str = os.path.dirname(self.app_path)
        subprocess.Popen([self.app_path], cwd=app_dir)
        
        # Waits the window propely open
        timeout: int = 30 # time in seconds
        start: float = time.time()
        
        while time.time() - start < timeout:
            
        
        # Aguarda a janela aparecer
        timeout = 30
        start = time.time()
        while time.time() - start < timeout:
            windows = gw.getWindowsWithTitle(self.window_title)
            if windows:
                self.window = windows[0]
                self.window.activate()
                logger.info("Programa EFD iniciado.")
                break
            time.sleep(1)
        else:
            raise RuntimeError("Não foi possível abrir o programa EFD.")

if __name__ == '__main__':
    efd_interector = EfdInterector(AppConfig())
    efd_interector.open()
