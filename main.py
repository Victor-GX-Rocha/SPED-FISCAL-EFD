""" Execution file """

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
    except KeyboardInterrupt as k:
        log.user.info('Comando: Desligar programa.')
    except Exception as e:
        log.dev.exception(f'Exceção global: {e}')


if __name__ == '__main__':
    main()
