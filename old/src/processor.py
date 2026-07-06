"""  """

import os
from file_manager import FileManager
from efd_interactor import EFDInteractor
from src.logger import get_logger

logger = get_logger(__name__)

class BatchProcessor:
    def __init__(self):
        self.file_manager = FileManager()
        self.efd = EFDInteractor()
        self.processed_dir: str = "processado"
        self.error_dir: str = "erro"
        self._create_dirs()
    
    def _create_dirs(self):
        for d in [self.processed_dir, self.error_dir]:
            os.makedirs(d, exist_ok=True)
    
    def run(self, folders):
        for folder in folders:
            logger.info(f"Iniciando processamento da pasta: {folder}")
            self.process_folder(folder)
        # Ao final, fechar o programa EFD
        self.efd.close_application()

    def process_folder(self, folder_path):
        """Processa todos os arquivos dentro de uma pasta."""
        
        files: list[str] = [f for f in os.listdir(folder_path) if f.endswith(('.txt', '.xml'))]
        if not files:
            logger.warning(f"Nenhum arquivo fiscal encontrado em {folder_path}")
            return
        
        for filename in files:
            full_path: str = os.path.join(folder_path, filename)
            success: bool = self._process_single_file(full_path)
            
            if not success:
                self.file_manager.move_file(full_path, self.error_dir)
            
            self.file_manager.move_file(full_path, self.processed_dir)

    def _process_single_file(self, file_path: str) -> bool:
        """Interage com o EFD para validar o arquivo."""
        try:
            # # 1. Abrir o programa EFD (se não estiver aberto)
            # self.efd.ensure_open()

            # # 2. Navegar até a tela de validação (clicar em menus, etc.)
            # #    usando reconhecimento de imagens
            # self.efd.navigate_to_validation()

            # # 3. Selecionar o arquivo (via campo de texto ou diálogo)
            # self.efd.select_file(file_path)

            # # 4. Clicar no botão "Validar" ou similar
            # self.efd.click_validate()

            # # 5. Aguardar conclusão (monitorar indicadores visuais)
            # result = self.efd.wait_for_result(timeout=60)

            # # 6. Fechar eventuais pop-ups de resultado
            # self.efd.close_result_popup()

            return result  # True se sucesso, False se erro
        except Exception as e:
            logger.exception(f"Falha ao processar {file_path}: {e}")
            return False
