
import time
import pyautogui as pag
from typing import Iterable

from src import log

pag.FAILSAFE = True

class PagTools:
    def verificar_elemento(
            self,
            img_path: str, 
            confidence: float = 0.9
        ) -> bool:
        try:
            exists = pag.locateCenterOnScreen(img_path, confidence=confidence)
            if not exists:
                print("Elemento não encontrado...")
                return False
            print("Elemento encontrado na tela!")
            return True
        except pag.ImageNotFoundException:
            print(f"Erro: Imagem {img_path} não está visível na tela.")
            return False

    def espere_elemento(
            self,
            img_path: str, 
            confidence: float = 0.9, 
            limite_espera: int = 10, 
            intervalo_espera: int = 1
        ) -> bool:
        """ Espera até que um elemento surja na tela. """
        try:
            start = time.time()
            
            while time.time() - start < limite_espera:
                exists = pag.locateCenterOnScreen(img_path, confidence=confidence)
                if exists:
                    return True
                time.sleep(intervalo_espera)
            else:
                raise TimeoutError(f'Tempo de espera de {limite_espera} para | {img_path} | excedido!')
        except TimeoutError as t:
            log.dev.error(t)
            return False
        except Exception as e:
            log.dev.error(f"Erro inesperado durante espera por elemento! | {img_path} | {e}")

    def espere_elementos(
            self,
            img_paths: Iterable, 
            confidence: float = 0.9, 
            limite_espera: int = 10, 
            intervalo_espera: int = 1,
            todos: bool = False
        ) -> bool:
        """ Recebe uma grupo de elementos e espera até que um deles (ou todos eles) surjam na tela. """
        try:
            start = time.time()
            
            while time.time() - start < limite_espera:
                resultados: list = [] # limpa a lista a cada execução.
                for img_path in img_paths:
                    resultado = pag.locateCenterOnScreen(img_path, confidence=confidence)
                    resultados.append(resultado is not None)
                    
                    if not todos and any(resultados):
                        print('Um dos elemtnos foi encontrado na tela!')
                        return True
                    
                    if todos and all(resultados):
                        print('Todos os elementos estão presentes na tela!')
                        return True
                    
                time.sleep(intervalo_espera)
            else:
                raise TimeoutError(f'Tempo de espera de {intervalo_espera} para | {img_paths} | excedido!')
        except TimeoutError as t:
            log.user.error(t)
            return False
        except Exception as e:
            log.dev.error(f"Erro inesperado durante espera por elemento! | {img_paths} | {e}")

    def espere_elemento_sumir(
            self,
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
                raise TimeoutError(f'Tempo de espera excedido e o elemento {img_path} ainda está na tela!')
        except pag.ImageNotFoundException as n:
            print(f'Imagem não encontrada na tela {n}\nOu seja, deu certo!')
            return True
        except TimeoutError as t:
            log.dev.warning(t)
            return False
        except Exception as e:
            print(f'Erro inesperado durante espera de um elemento sumir {e}')

    def escolher_rota(
            self,
            img_paths: Iterable, 
            confidence: float = 0.9, 
            limite_espera: int = 10, 
            intervalo_espera: int = 1
        ) -> str:
        """
        Recebe um grupo de imagens e aguarda até que uma delas esteja presente na tela.
        As imagens serão utilizados para definir que rota o fluxo deve tomar.
        
        Cada caminho de imagem serrvirá como um ID, caso essa imagem seja encontrada na tela (como a imagem de um menu) o seu caminho será retornado.
        
        Isso pode ser utilizado para saber exatamente que elemento está presente na tela naquele momento.
        """
        try:
            start = time.time()
            
            while time.time() - start < limite_espera:
                for img_path in img_paths:
                    try:
                        resultado = pag.locateCenterOnScreen(img_path, confidence=confidence)
                        if resultado:
                            return img_path
                    except pag.ImageNotFoundException:
                        pass
                time.sleep(intervalo_espera)
            else:
                raise TimeoutError(f'Tempo limite de espera de {limite_espera} para | {img_paths} | excedido!')
        except TimeoutError as t:
            log.dev.exception(t)
            return False
        except Exception as e:
            log.dev.exception(f"Erro inesperado durante espera por elemento! | {img_paths} | {e}")

"""
Ideia! Criar um sistema de rotas.
Como ralizar uma operação pode levar a telas diferentes, eu posso criar um método que direcione para uma rota específica.
A ideia é tipo, como eu já tenho as imagens que devem ser identificadas para cada tipo de telas elas podem servir como uma espécie de ID.
Se por exemplo, surgir uma tela de erro, eu posso capturar essa informação com o programa, retornar o caminho dessa imagem (que aqui servirá como ID já que é a imagem da tela de erro)
E com base no ID retornado eu posso direcionar o programa para uma rota específica diretamente!

De início eu vou fazer algo simples com uns ifs e elses, mas como agora eu estou optando fazer etapa por etapa, o ideal seria criar um dicionário de funções cheve=id e rota=caminho_da_funçao e para então enfim passar para algo mais robusto e apropriado como um strategy pattern de fato.
"""