

import os, sys
from tkinter import messagebox
from src import log
from src.efd_navigator import EfdNavigator
from src.paths import ImgPaths, DestinyFolders, mover_arquivo # O certo é só mover depois, to movendo aqui para fins de teste.
from src.pag_tools import PagTools


class MissingEfdProgram(Exception):...

class EfdInteractor:
    def __init__(
            self, 
            file_path: str, 
            img_paths: ImgPaths,
            navigator: EfdNavigator,
            pag_tools: PagTools
        ) -> None:
        """  """
        
        self.file_path: str = os.path.abspath(file_path) # Garante que seja o caminho absoluto para o arquivo.
        self.img_path: ImgPaths = img_paths
        self.navigator: EfdNavigator = navigator
        self.pag_tools: PagTools = pag_tools
    
    def abrir_programa():
        """ Abrir é fácil, mas eu preciso rever a rotina que verifica se o programa já está aberto. Para verificar a janela inicial em específco eu acho que posso por 'nome da janela' como variável de ambiente, assim mesmo que ela mude o programa ainda se adapta. Como eu vou precisar das variáveis de ambiente para abrir o programa já posso pegar no embalo."""
    
    def fechar_programa():
        """ Pode ser com uma busca por imagem direcionada, comando shell ou simplesmente um alt f4. Acho que comando shell é o mais seguro e menos sujeito a erros. """

    def _selecionar_arquivo_escrituracao(self) -> None:
        """ Seleciona um arquivo de escrituração e confirma """
        self.navigator.abrir_escrituracao(espere=4)
        self.navigator.escrever_caminho_do_arquivo(self.file_path, espere=1)
        self.navigator.confirmar(espere=1)

    def realizar_escrituracao(self) -> bool:
        """  """
        print(f'< Inciando escrituração do arquivo: {self.file_path}')
        
        # Verifica se o arquivo existe
        if not os.path.exists(self.file_path):
            log.user.warning(f'Arquivo {self.file_path} não foi encontrado! Verifique se o arquivo ainda existe ou se o nome foi alterado')
            return False
        
        # Verifica, antes começar, se a tela inicial do SPED está visível.
        if not self.pag_tools.espere_elemento(self.img_path.tela_inicial, limite_espera=20):
            messagebox.showwarning("Aviso", "O aplicativo do governo SPED EFD não está visivel na tela. Por favor, deixe-o em foco. \nO tempo de limite de espera pelo aplicativo foi excedido. Desligando o programa...")
            sys.exit()
        
        self.navigator.atualizar_tabelas()
        
        self._selecionar_arquivo_escrituracao()
        
        print('- Esperando nota ser carregada após a importação')
        
        rota: str = self.pag_tools.escolher_rota(
            img_paths=[
                self.img_path.importacao_exito,
                self.img_path.escrituracao_ja_existe,
                
                self.img_path.importacao_nao_realizada,
                self.img_path.arquivo_nao_encontrado
                ],
            limite_espera=20
        )
        
        if rota == self.img_path.importacao_exito:
            self.navigator.confirmar()
            
        elif rota == self.img_path.escrituracao_ja_existe: # Se a escrituaração já existir no sistema, simplesmente continue.
            log.user.info("Nota de escrituração já existe no sistema, confirmando e prosseguindo.")
            self.navigator.confirmar()
            self.navigator.espere_carregar(5)
            
        elif rota == self.img_path.importacao_nao_realizada:
            log.user.error('- Foi encontrado um erro no arquivo!')
            self.navigator.confirmar()
            self.navigator.fechar_tela(1.5)
            
            # Mover arquivo para a pasta de erro.
            mover_arquivo(self.file_path, DestinyFolders.ERRO) # O certo é só mover depois, to movendo aqui para fins de teste.
            return False
            
        elif rota == self.img_path.arquivo_nao_encontrado:
            log.user.warning(f'Arquivo {self.file_path} não foi encontrado! Verifique se o arquivo ainda existe ou se o nome foi alterado')
            return False
        
        # 2° Rota
        rota: str = self.pag_tools.escolher_rota(
            img_paths=[
                self.img_path.importacao_exito,
                self.img_path.escrituracao_fiscal,
                self.img_path.atualizar_tabelas
                ],
            limite_espera=60
        )
        
        if rota == self.img_path.importacao_exito:
            self.navigator.confirmar()
            
        elif rota == self.img_path.escrituracao_fiscal:
            self.navigator.fechar_escrituracao()
            mover_arquivo(self.file_path, DestinyFolders.PROCESSADO) # O certo é só mover depois, to movendo aqui para fins de teste.
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
            limite_espera=60
        )
        
        if rota == self.img_path.importacao_exito:
            self.navigator.confirmar()
            
        elif rota == self.img_path.atualizar_tabelas:
            self.navigator.confirmar(1)
            self.navigator.confirmar(1)
            
        elif rota == self.img_path.escrituracao_fiscal or rota == self.img_path.validado_com_sucesso:
            self.navigator.confirmar()
            self.navigator.fechar_escrituracao(1)
            mover_arquivo(self.file_path, DestinyFolders.PROCESSADO) # O certo é só mover depois, to movendo aqui para fins de teste.
            return True
