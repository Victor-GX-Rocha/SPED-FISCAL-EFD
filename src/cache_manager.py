import json
from pathlib import Path
from typing import Any, Dict

class JsonCache:
    """
    Gerencia a persistência de um dicionário em um único arquivo JSON.
    Responsabilidades: Carregar, Salvar e garantir que o diretório exista.
    """
    def __init__(self, file_path: Path | str):
        self.file_path = Path(file_path)
    
    def load(self) -> Dict[str, Any]:
        """Carrega o JSON. Retorna dict vazio se o arquivo não existir."""
        if not self.file_path.exists():
            return {}
        with open(self.file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save(self, data: Dict[str, Any]) -> None:
        """Salva o dict no JSON, criando pastas se necessário."""
        # Cria o diretório pai se não existir (evita FileNotFoundError)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
