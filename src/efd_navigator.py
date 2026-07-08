""" Uma intercade simples e intuitiva para navegar pelo programa EFD. """

import time
import pyautogui as pag

pag.FAILSAFE = True

class EfdNavigator:
    """ Executa comandos de teclado no EFD """
    
    @staticmethod
    def abrir_escrituracao(espere: float = 0) -> None:
        """ Abre uma escrituração através do comando CTRL + I """
        if espere:
            time.sleep(espere)
        pag.hotkey('ctrl', 'i')
    
    @staticmethod
    def fechar_escrituracao(espere: float = 0) -> None:
        """ Fechauma escrituração através do comando CTRL + F """
        if espere:
            time.sleep(espere)
        pag.hotkey('ctrl', 'f')
    
    @staticmethod
    def escrever_caminho_do_arquivo(file_path: str, interval: int = 0, espere: float = 0) -> None:
        """  """
        if espere:
            time.sleep(espere)
        pag.write(file_path, interval=interval)
    
    @staticmethod
    def confirmar(espere: float = 0) -> None:
        if espere:
            time.sleep(espere)
        pag.press('enter')
    
    @staticmethod
    def sconfirmar(espere: float = 0) -> None:
        """ Confirma com 'space' ao invés de 'enter' """
        if espere:
            time.sleep(espere)
        pag.press('enter')

    @staticmethod
    def espere_carregar(espere: float = 0) -> None:
        time.sleep(espere)

    @staticmethod
    def fechar_tela(espere: float = 0) -> None:
        if espere:
            time.sleep(espere)
        pag.hotkey('alt', 'f4')
    
    @staticmethod
    def atualizar_tabelas(espere: float = 0, espere_ataulizar: float = 1.5) -> None:
        """ Abre uma escrituração através do comando CTRL + I """
        if espere:
            print('Esperando antes de atualizar a tabela')
            time.sleep(espere)
        pag.hotkey('ctrl', 'shift', 'z')
        
        print('Esperando antes de fechar a tabela')
        time.sleep(espere_ataulizar)
        pag.press('enter')


