
import time
import pyautogui as pag

pag.FAILSAFE = True

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
