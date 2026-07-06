# efd_interactor.py

import pyautogui
import pygetwindow as gw
import time
import subprocess
import os
from src.logger import get_logger

logger = get_logger(__name__)

class EFDInteractor:
    def __init__(self, app_path=r"C:\Arquivos de Programas RFB\Programas SPED\Fiscal\SpedEFD.exe", images_dir="images"):
        self.app_path = app_path
        self.images_dir = images_dir
        self.window_title = "EFD - ICMS IPI"
        self.window = None

    def ensure_open(self):
        """ Abre o programa se não estiver em execução. """
        windows = gw.getWindowsWithTitle(self.window_title)
        if windows:
            self.window = windows[0]
            self.window.activate()
            logger.info("Programa EFD já está aberto.")
        else:
            logger.info("Abrindo o programa EFD...")
            subprocess.Popen([self.app_path], shell=True)
            
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

    def _wait_and_click(self, image_name, timeout=20, confidence=0.85, click=True):
        """Localiza a imagem e clica (opcional). Retorna as coordenadas."""
        image_path = os.path.join(self.images_dir, image_name)
        start = time.time()
        while time.time() - start < timeout:
            try:
                location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
                if location:
                    if click:
                        pyautogui.click(location)
                        logger.debug(f"Clicado em {image_name}")
                    return location
            except Exception as e:
                logger.debug(f"Erro ao buscar {image_name}: {e}")
            time.sleep(0.5)
        raise TimeoutError(f"Imagem {image_name} não encontrada na tela.")

    def _type_text(self, text):
        """Digita o texto (com tratamento para caracteres especiais)."""
        pyautogui.write(text, interval=0.05)

    def navigate_to_validation(self):
        """Navega pelos menus até chegar na tela de validação."""
        # Exemplo: clicar em "Arquivo" -> "Importar" -> "Validar"
        # Ajuste conforme a interface real.
        self._wait_and_click("menu_arquivo.png")
        time.sleep(0.5)
        self._wait_and_click("menu_importar.png")
        time.sleep(0.5)
        self._wait_and_click("menu_validar.png")
        time.sleep(1)

    def select_file(self, file_path):
        """Seleciona o arquivo no campo apropriado."""
        # Clica no campo de seleção (ou no botão "Selecionar")
        self._wait_and_click("campo_arquivo.png")
        # Limpa o campo (Ctrl+A + Delete)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('delete')
        # Digita o caminho
        self._type_text(file_path)
        # Pressiona Enter ou clica em OK
        pyautogui.press('enter')
        time.sleep(1)

    def click_validate(self):
        """Clica no botão de validação."""
        self._wait_and_click("botao_validar.png")
        logger.info("Validação iniciada.")

    def wait_for_result(self, timeout=120):
        """Espera a conclusão e retorna True se sucesso, False se erro."""
        # Monitora se aparece imagem de sucesso ou erro.
        success_image = "msg_sucesso.png"
        error_image = "msg_erro.png"
        start = time.time()
        while time.time() - start < timeout:
            if pyautogui.locateOnScreen(os.path.join(self.images_dir, success_image), confidence=0.8):
                logger.info("Validação concluída com sucesso.")
                return True
            if pyautogui.locateOnScreen(os.path.join(self.images_dir, error_image), confidence=0.8):
                logger.error("Validação falhou.")
                return False
            time.sleep(1)
        raise TimeoutError("Tempo esgotado aguardando o resultado da validação.")

    def close_result_popup(self):
        """Fecha possíveis pop-ups de resultado (clicando em OK ou no X)."""
        try:
            self._wait_and_click("btn_ok.png", timeout=5, click=True)
        except TimeoutError:
            logger.debug("Nenhum pop-up de resultado encontrado.")

    def close_application(self):
        """Fecha o programa de forma segura."""
        if self.window:
            self.window.close()  # ou pyautogui.hotkey('alt', 'f4')
            logger.info("Programa EFD fechado.")
