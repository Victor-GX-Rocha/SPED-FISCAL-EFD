from pathlib import Path
from PIL import Image
import ctypes
import pyautogui
from src import log  # assumindo que seu log está configurado

# --- CONSTANTES (simples, diretas) ---
BASE_DIR = Path(__file__).resolve().parent.parent
ORIGINAL_DIR = BASE_DIR / 'imgs' / 'originais'
TARGET_DIR = BASE_DIR / 'imgs'
BASE_RESOLUTION = (1920, 1080)  # Tupla simples

# --- Funções utilitárias (sem classe) ---
def _force_dpi_awareness() -> None:
    """Força DPI real no Windows."""
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except AttributeError:
        pass  # Não é Windows

def get_screen_resolution() -> tuple[int, int]:
    """Retorna a resolução atual da tela."""
    _force_dpi_awareness()
    try:
        user32 = ctypes.windll.user32
        return (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))
    except Exception:
        return pyautogui.size()  # fallback

def resize_image(src: Path, dst: Path, screen_size: tuple[int, int]) -> None:
    """Redimensiona UMA imagem baseado na resolução da tela."""
    base_w, base_h = BASE_RESOLUTION
    scr_w, scr_h = screen_size
    
    # Mantém proporção usando o menor fator (evita cortar)
    scale = min(scr_w / base_w, scr_h / base_h)
    
    img = Image.open(src)
    new_w = max(1, int(img.width * scale))
    new_h = max(1, int(img.height * scale))
    
    img.resize((new_w, new_h), Image.Resampling.LANCZOS).save(dst)
    log.user.info(f"✅ {dst.name} -> {new_w}x{new_h}")

def process_images() -> None:
    """Processa todas as imagens da pasta de origem para a de destino."""
    screen = get_screen_resolution()
    log.user.info(f"📺 Resolução detectada: {screen[0]}x{screen[1]}")
    
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    
    # Usando glob do pathlib (muito mais elegante que os.listdir com filtro)
    extensions = ('.png', '.jpg', '.jpeg', '.bmp')
    images = [f for f in ORIGINAL_DIR.glob('*') if f.suffix.lower() in extensions]
    
    if not images:
        log.user.warning(f"⚠️ Nenhuma imagem encontrada em {ORIGINAL_DIR}")
        return
    
    log.user.info(f"🔄 Redimensionando {len(images)} imagem(ns)...")
    for img_path in images:
        resize_image(img_path, TARGET_DIR / img_path.name, screen)
    
    log.user.info("✅ Todas as imagens processadas!")

if __name__ == "__main__":
    process_images()
