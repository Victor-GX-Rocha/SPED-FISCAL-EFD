# processor.py

import os
from typing import Iterable

from src import log
from src.efd_interactor import EfdInteractor
from src.paths import DestinyFolders, mover_arquivo


class BatchProcessor:
    def __init__(self, efd_interactor: EfdInteractor):
        self.ei: EfdInteractor = efd_interactor
    
    def processar(self, folders: Iterable[str]):
        """ Abre o Sped Fiscal, processa os dados e fecha ao terminar as operações. """
        
        self.ei.abrir_sped_fiscal()
        
        for folder in folders:
            log.user.info(f"Iniciando processamento da pasta: {folder}...")
            self.processar_pasta(folder)
        
        # self.ei.fechar_sped_fiscal()
    
    def processar_pasta(self, folder_path: str) -> None:
        """ Processa todos os arquivos dentro de uma pasta. """
        
        files: list[str] = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
        
        if not files:
            log.user.warning(f"Nenhum arquivo fiscal encontrado em {folder_path}")
            return
        
        log.user.info(f'Iniciando a resolução das {len(files)} escriturações encontradas')
        for filename in files:
            full_path: str = os.path.join(folder_path, filename)
            self._processar_arquivo_unico(full_path)
    
    def _processar_arquivo_unico(self, full_path) -> bool:
        """ Interage com o EFD para validar o arquivo. """
        try:
            
            success: bool = self.ei.realizar_escrituracao(full_path)
            if not success:
                mover_arquivo(full_path, DestinyFolders.ERRO)
            mover_arquivo(full_path, DestinyFolders.PROCESSADO)
            
        except Exception as e:
            log.dev.exception(f"Falha ao processar {full_path}: {e}")
            return 
