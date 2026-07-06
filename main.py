""" Execution file """

from src.efd_interactor import EfdInteractor
from src.efd_navigator import EfdNavigator
from src.paths import ImgPaths
from src.pag_tools import PagTools

import time

time.sleep(3)

def main() -> None:
    """ Execution function """
    # Refazendo tudo
    file_path_error: str = r'docs\46377727002218-353100786114-20250101-20250131-0-AF2854AA9F89B7A3A0B30E9A6DD1044F2BE8F277-SPED-EFD_limpo_20260705_220444.txt'
    file_path: str = r'C:\Users\Administrador\OneDrive\12-PROJECTS\SPED-FISCAL-EFD-2\docs\46377727002218-353100786114-20250301-20250331-0-441E2D9001930B156BE5D598924B812B85104C68-SPED-EFD_limpo.txt'
    
    # 1. Pegar os caminhos dos arquivos. (Já tenho pronto, posso inserir depois.)
    print('< Capiturando caminhos...')
    
    # 2. Abrir o programa. (Já tenho pronto, posso inserir depois.)
    print('< Abrindo programa de forma segura')
    
    # 3. Realizar escrituração.
    print('Iniciando a resolução das [número da quantidade de arquivos encontrados] escriturações')
    
    ei = EfdInteractor(
        file_path=file_path_error,
        img_paths=ImgPaths(),
        navigator=EfdNavigator(),
        pag_tools=PagTools()
    )
    ei.realizar_escrituracao()


if __name__ == '__main__':
    from src import log
    try:
        main()
    except Exception as e:
        log.dev.exception(f'Exceção global: {e}')
