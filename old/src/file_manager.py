# file_manager.py
import os
import shutil
from src.logger import get_logger
import time

logger = get_logger(__name__)

class FileManager:
    def move_file(src_path, dest_dir):
        """Move o arquivo para o diretório de destino (processado ou erro)."""
        try:
            os.makedirs(dest_dir, exist_ok=True)
            filename = os.path.basename(src_path)
            dest_path = os.path.join(dest_dir, filename)
            # Evitar sobrescrita: adicionar timestamp se existir
            if os.path.exists(dest_path):
                base, ext = os.path.splitext(filename)
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                new_name = f"{base}_{timestamp}{ext}"
                dest_path = os.path.join(dest_dir, new_name)
            shutil.move(src_path, dest_path)
            logger.info(f"Arquivo movido para {dest_path}")
        except Exception as e:
            logger.exception(f"Falha ao mover {src_path}: {e}")
            raise
