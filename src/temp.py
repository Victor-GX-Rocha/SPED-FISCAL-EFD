""" Local para guardar o caminho das imagens """

import os
import time
import enum
import shutil
import pyautogui as pag
from dataclasses import dataclass

pag.FAILSAFE = True


def normalize_path(path: str) -> str:
    """  """
    return path.strip().replace("'", "").replace('"', '').replace('\\', '/')

@dataclass
class ImgPaths:
    """ Um caminho direto e organizado para as imagens. """
    escrituracao_ja_existe: str = normalize_path(r'imgs\Escrituracao-ja-existe.png')
    importacao_exito: str = normalize_path(r'C:\Users\Administrador\OneDrive\12-PROJECTS\SPED-FISCAL-EFD-2\imgs\importacao exito.png')
    escrituracao_fiscal: str = normalize_path(r'C:\Users\Administrador\OneDrive\12-PROJECTS\SPED-FISCAL-EFD-2\imgs\Escrituracao_fiscal.png')
    importacao_nao_realizada: str = r'C:\Users\Administrador\OneDrive\12-PROJECTS\SPED-FISCAL-EFD-2\imgs\importacao_nao_realizada.png'

@dataclass
class DestinyFolders:#(enum.Enum):
    PROCESSADO: str = 'processado'
    ERRO: str = 'erro'

def verificar_elemento(img_path: str, confidence: float = 0.9) -> bool:
    try:
        exists = pag.locateCenterOnScreen(img_path, confidence=confidence)
        if not exists:
            print("Elemento não encontrado...")
            return False
        print("Elemento encontrado na tela!")
        return True
    except pag.ImageNotFoundException:
        nome_imagem: str = img_path#.split('\\')[-2]
        print(f"Erro: Imagem {nome_imagem} não está visível na tela.")

def espere_por_elemento():...
def espere_elemento_sumir(
        img_path: str, 
        confidence: float = 0.9, 
        limite_espera: int = 30, 
        intervalo_espera: int = 1
    ) -> bool:
    """ Verifica, durante um intervalo, se um elemento está presente na tela e aguarda até que ele suma. """
    try:
        start = time.time()
        
        while time.time() - start < limite_espera:
            exists = pag.locateCenterOnScreen(img_path, confidence=confidence)
            if not exists:
                return True
            time.sleep(intervalo_espera)
        else:
            raise TimeoutError('Tempo de espera excedido!') # Tempo de espera excedido e o elemento ainda está na tela
    except pag.ImageNotFoundException as n:
        print(f'Imagem não encontrada na tela {n}\nOu seja, deu certo!')
        return True
    except TimeoutError as t:
        print(t)
        return False
    except Exception as e:
        print(f'Erro inesperado durante espera de um elemento sumir {e}')




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
        """ Abre uma escrituração através do comando CTRL + I """
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
    def espere_carregar(espere: float = 0) -> None:
        time.sleep(espere)

    @staticmethod
    def fechar_tela(espere: float = 0) -> None:
        if espere:
            time.sleep(espere)
        pag.hotkey('alt', 'f4')



def mover_arquivo(file_path: str, dest_dir: DestinyFolders):
    """Move o arquivo para o diretório de destino (processado ou erro)."""
    try:
        
        os.makedirs(dest_dir, exist_ok=True)
        # dest_path: str = os.path.abspath(file_path) # Pega o caminho completo do arquivo, previne se um caminho relativo tiver sido passado.
        filename: str = os.path.basename(file_path)
        dest_path: str = os.path.join(dest_dir, filename)
        
        # print(filename)
        # print(f'''
        # {file_path = }
        # {filename = }
        # {dest_path = }
        # ''')
        
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
    
    def realizar_escrituracao(self) -> bool:
        """  """
        
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


if __name__ == '__main__':
    
    file_path_error: str = r'C:\Users\Administrador\OneDrive\12-PROJECTS\SPED-FISCAL-EFD-2\46377727002218-353100786114-20250101-20250131-0-AF2854AA9F89B7A3A0B30E9A6DD1044F2BE8F277-SPED-EFD_limpo_20260705_220444.txt'
    # r'C:\Users\Administrador\OneDrive\12-PROJECTS\SPED-FISCAL-EFD-2\46377727002218-353100786114-20250101-20250131-0-AF2854AA9F89B7A3A0B30E9A6DD1044F2BE8F277-SPED-EFD_limpo.txt'
    # 46377727002218-353100786114-20250301-20250331-0-441E2D9001930B156BE5D598924B812B85104C68-SPED-EFD_limpo
    file_path: str = r'C:\Users\Administrador\OneDrive\12-PROJECTS\SPED-FISCAL-EFD-2\46377727002218-353100786114-20250301-20250331-0-441E2D9001930B156BE5D598924B812B85104C68-SPED-EFD_limpo.txt'
    
    
    ei = EfdInteractor(
        file_path=file_path,
        img_paths=ImgPaths(),
        navigator=EfdNavigator()
    )
    ei.realizar_escrituracao()
    


