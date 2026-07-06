

import os
from src import log
from src.efd_navigator import EfdNavigator
from src.paths import ImgPaths, DestinyFolders, mover_arquivo
from src.pag_tools import verificar_elemento

class EfdInteractor:
    def __init__(
            self, 
            file_path: str, 
            img_paths: ImgPaths,
            navigator: EfdNavigator
        ) -> None:
        """  """
        
        self.file_path: str = file_path
        self.img_path: ImgPaths = img_paths
        self.navigator: EfdNavigator = navigator
    
    def abrir_programa():
        """ Abrir é fácil, mas eu preciso rever a rotina que verifica se o programa já está aberto. Para verificar a janela inicial em específco eu acho que posso por 'nome da janela' como variável de ambiente, assim mesmo que ela mude o programa ainda se adapta. Como eu vou precisar das variáveis de ambiente para abrir o programa já posso pegar no embalo."""
    
    def fechar_programa():
        """ Pode ser com uma busca por imagem direcionada, comando shell ou simplesmente um alt f4. Acho que comando shell é o mais seguro e menos sujeito a erros. """
    
    def realizar_escrituracao(self) -> bool:
        """  """
        
        if not os.path.exists(self.file_path):
            log.user.warning(f'Arquivo {self.file_path} não foi encontrado! Verifique se o arquivo ainda existe ou se o nome foi alterado')
            return
        
        self.navigator.abrir_escrituracao(espere=4)
        self.navigator.escrever_caminho_do_arquivo(self.file_path, espere=1)
        self.navigator.confirmar(espere=1)
        
        print('- Esperando nota ser carregada após a importação')
        self.navigator.espere_carregar(10)
        
        # Se a escrituaração já existir no sistema, continue.
        if verificar_elemento(self.img_path.escrituracao_ja_existe):
            self.navigator.confirmar()
            self.navigator.espere_carregar(5)
            print("- Escrituração já existe: confirmando e prosseguindo.")
        
        self.navigator.espere_carregar(10) # O erro avisa rápido, então uma espera de 3 segundos basta.
        # Caso de erro!
        if verificar_elemento(self.img_path.importacao_nao_realizada):
            print('- Foi encontrado um erro no arquivo!')
            self.navigator.confirmar()
            self.navigator.fechar_tela(1.5)
            # Mover arquivo para a pasta de erro.
            mover_arquivo(self.file_path, DestinyFolders.ERRO)
            return False
        
        # 
        # if verificar_elemento(self.img_path.escrituracao_fiscal): 
        #     self.navigator.confirmar()
        
        # self.navigator.espere_carregar(10)
        if verificar_elemento(self.img_path.importacao_exito):
            self.navigator.confirmar()
        
        # "Validando a escrituração selecionada" - Depois de importar a nota, Espera o programa validar
        self.navigator.espere_carregar(40) # Eu posso trocar isso por um wait dinâmico de fato
        self.navigator.confirmar()
        self.navigator.espere_carregar(2)
        
        if verificar_elemento(self.img_path.escrituracao_fiscal):
            self.navigator.fechar_escrituracao()
            # Mover para a pasta processado
            mover_arquivo(self.file_path, DestinyFolders.PROCESSADO)
            return True
        
        self.navigator.espere_carregar(3)

