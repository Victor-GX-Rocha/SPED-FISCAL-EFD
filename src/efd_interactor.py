""" Interage diretamente com o programa 'Sped Fiscal' através de hotkeys, comandos shell e identificação de imagens. """

import os
import sys
import subprocess
import pyautogui as pag
from tkinter import messagebox

from src import log
from src.efd_navigator import EfdNavigator
from src.paths import ImgPaths
from src.pag_tools import PagTools
from src.env_data import EnvData
from src.window_manager import WindowManager

import time

class MissingEfdProgram(Exception):...


class EfdInteractor:
    def __init__(
            self, 
            img_paths: ImgPaths,
            navigator: EfdNavigator,
            pag_tools: PagTools
        ) -> None:
        self.img_path: ImgPaths = img_paths
        self.navigator: EfdNavigator = navigator
        self.pag_tools: PagTools = pag_tools
        self.efd_processo: subprocess.Popen = None
        self.sped_whnd: int = None
    
    def abrir_sped_fiscal(self) -> None:
        """ Verifica se já há uma instância do sped fiscal aberta e abre uma nova se necessário. """
        
        janela_id: int = WindowManager.encontrar_janela_por_titulo('sped fiscal')
        print(f'{janela_id = }')
        
        if WindowManager.janela_ativa(janela_id):
            print('Calma lá! A janela está aberta!!')
            messagebox.showwarning(
                "Aviso", # Pede para o usuário fechar a janela.
                "Notei que o programa 'Sped fiscal' já está aberto, por favor, antes de iniciar a automação, finalize o que estava fazendo e feche-o. Após isso inicie a automação novamente com o 'Sped fiscal' fechado."
            )
            sys.exit()
        else:
            print('Não identificou a janela aberta...')
            app_dir: str = os.path.dirname(EnvData.efd_path)
            
            log.user.info(f"Iiniciando o executável do Sped Fiscal...")
            self.efd_processo: subprocess.Popen = WindowManager.abrir_programa(EnvData.efd_path, app_dir=app_dir)
            # print(f'{self.efd_processo.pid = }')
            
            # if self.pag_tools.espere_elemento(self.img_path.tela_inicial, limite_espera=20):
            #     self.sped_whnd: int = WindowManager.encontrar_janela_por_titulo('sped fiscal')
            #     print(f'{self.sped_whnd = }')
                
            #     # self.sped_whnd: int = WindowManager.encontrar_janela_por_pid(self.efd_processo.pid)
            #     WindowManager.tornar_topmost(self.sped_whnd)
    
    def fechar_sped_fiscal(self) -> None:
        """ Pode ser com uma busca por imagem direcionada, comando shell ou simplesmente um alt f4. Acho que comando shell é o mais seguro e menos sujeito a erros. """
        
        try:
            WindowManager.fechar_janela(self.efd_processo)
        except Exception as e:
            log.user.warning('Erro inesperado ao fechar o programa. Iniciando outros métodos de fechamento.')
            log.dev.exception(f'Acho que esse pid não deve ter funcionado...')
            # self.navigator.fechar_tela(1)
    
    def _selecionar_arquivo_escrituracao(self, file_path: str) -> None:
        """ Seleciona um arquivo de escrituração e confirma """
        print('Selecionando escrituração')
        self.navigator.abrir_escrituracao(espere=5)
        self.navigator.escrever_caminho_do_arquivo(file_path, espere=1)
        self.navigator.confirmar(espere=1)
    
    def realizar_escrituracao(self, file_path: str) -> bool:
        """  """
        file_path: str = os.path.abspath(file_path) # Garante que seja o caminho absoluto para o arquivo.
        
        log.user.info(f'Inciando escrituração do arquivo: {file_path}')
        
        # Verifica se o arquivo existe
        if not os.path.exists(file_path):
            log.user.warning(f'Arquivo {file_path} não foi encontrado! Verifique se o arquivo ainda existe ou se o nome foi alterado')
            return False
        
        # Verifica, antes começar, se a tela inicial do SPED está visível.
        print('Iniciando espera pela tela inicial')
        if not self.pag_tools.espere_elemento(self.img_path.tela_inicial, limite_espera=40):
            messagebox.showwarning(
                "Aviso", "O aplicativo do governo SPED EFD não está visivel na tela. Por favor, deixe-o em foco. \nO tempo de limite de espera pelo aplicativo foi excedido. Desligando o programa..."
            )
            sys.exit()
        
        print('Espera acabou')
        
        
        if not self.sped_whnd:
            self.sped_whnd: int = WindowManager.encontrar_janela_por_titulo('sped fiscal')
            print(f'{self.sped_whnd = }')
            if self.sped_whnd:
                WindowManager.tornar_topmost(self.sped_whnd)
                print("Está topmost!!")
        
        print('Clicando na tela inicial antes de atualizar as tabelas')
        # pag.click(self.img_path.tela_inicial)
        # self.navigator.atualizar_tabelas()
        
        if self.pag_tools.espere_elemento(self.img_path.tela_inicial, limite_espera=40):
            self._selecionar_arquivo_escrituracao(file_path)
        
        print('Esperando nota ser carregada após a importação')
        
        rota: str = self.pag_tools.escolher_rota(
            img_paths=[
                self.img_path.importacao_exito,
                self.img_path.escrituracao_ja_existe,
                
                self.img_path.importacao_nao_realizada,
                self.img_path.arquivo_nao_encontrado,
                self.img_path.arquivo_nao_encontrado2,
                self.img_path.erro
                ],
            limite_espera=120
        )
        
        print('Passou reto pela rota 1')
        
        if rota == self.img_path.importacao_exito:
            self.navigator.confirmar()
            
        elif rota == self.img_path.escrituracao_ja_existe: # Se a escrituaração já existir no sistema, simplesmente continue.
            log.user.info("Nota de escrituração já existe no sistema, confirmando e prosseguindo.")
            self.navigator.confirmar()
            self.navigator.espere_carregar(5)
            
        elif rota == self.img_path.importacao_nao_realizada:
            log.user.error('Foi encontrado um erro no arquivo!')
            self.navigator.confirmar(1)
            self.navigator.fechar_tela(1.5)
            return False
            
        elif rota in (self.img_path.arquivo_nao_encontrado, self.img_path.arquivo_nao_encontrado2, self.img_path.erro):
            if rota in (self.img_path.arquivo_nao_encontrado, self.img_path.arquivo_nao_encontrado2):
                log.user.warning(f'Arquivo {file_path} não foi encontrado! Verifique se o arquivo ainda existe ou se o nome foi alterado')
            self.navigator.sconfirmar()
            return False
        
        # 2° Rota
        rota: str = self.pag_tools.escolher_rota(
            img_paths=[
                self.img_path.importacao_exito,
                self.img_path.escrituracao_fiscal,
                self.img_path.atualizar_tabelas
                ],
            limite_espera=120
        )
        
        if rota == self.img_path.importacao_exito:
            self.navigator.confirmar()
            
        elif rota == self.img_path.escrituracao_fiscal:
            self.navigator.fechar_escrituracao()
            return True
            
        elif rota == self.img_path.atualizar_tabelas:
            self.navigator.confirmar(1)
            self.navigator.confirmar(1)
        
        # 3° Rota.
        rota: str = self.pag_tools.escolher_rota(
            img_paths=[
                self.img_path.importacao_exito,
                self.img_path.escrituracao_fiscal
                ],
            limite_espera=120
        )
        
        if rota == self.img_path.importacao_exito:
            self.navigator.confirmar()
            
        elif rota == self.img_path.atualizar_tabelas:
            self.navigator.confirmar(1)
            self.navigator.confirmar(1)
            
        elif rota == self.img_path.escrituracao_fiscal or rota == self.img_path.validado_com_sucesso:
            self.navigator.confirmar()
            self.navigator.fechar_escrituracao(1)
            return True
