""" Execution file """

from dotenv import load_dotenv
import sys
import pyautogui as pag
pag.FAILSAFE = True
load_dotenv()

from src import log
from src.paths import ImgPaths
from src.pag_tools import PagTools
from src.efd_interactor import EfdInteractor
from src.efd_navigator import EfdNavigator
from src.processor import BatchProcessor
from src.folder_selector import FolderSelector

def main() -> None:
    """ Execution function """
    try:
        log.user.info('Capturando caminhos...')
        pastas: list[str] = FolderSelector.get_folders()
        
        ei = EfdInteractor(
            img_paths=ImgPaths(),
            navigator=EfdNavigator(),
            pag_tools=PagTools()
        )
        
        processor = BatchProcessor(ei)
        processor.processar(pastas)
    except pag.FailSafeException:
        sys.exit(0)
    except KeyboardInterrupt as k:
        log.user.info('Comando: Desligar programa.')
    except SystemExit:
        sys.exit(0)
    except Exception as e:
        log.dev.exception(f'Exceção global: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
    # pyinstaller --onedir --add-data "imgs;imgs" --add-data ".env;." --name SpedProcessor main.py                                                              
    # pyinstaller --onedir --noconsole --add-data "imgs;imgs" --add-data ".env;." --name SpedProcessor main.py

    """
    Alterações:
    Ao abrir o programa ---
    
    Se, no arquivo .env "REDIMENSIONAR_IMAGENS=True" 
        > Ele vai pegar a resolução real do monitor atual do dispositivo.
        Se for igual 1980x1280: (o tamanho original utilziado)
            Ele simplesmente pega a base de dados original.
        Se não:
            Ele converte as imagens para a proporção adequada (usando os dados que obeteve antes).
    Se não:
        Só passa direto.
    
    # O arquivo .env também pode ter a opção de inserir esses dados manualmente:
        RESOLUCAO_DA_TELA=1080x800
        USAR_RESOLUCAO_MANUAL=False
    """