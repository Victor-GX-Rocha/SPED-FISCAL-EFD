
import subprocess
import win32gui
import win32con
import win32process
import time

class WindowManager:
    
    @staticmethod
    def abrir_programa(exe_caminho: str, app_dir: str, topmost: bool = False):
        """
        Abre um programa inicindo seu executável.
        
        Args:
            exe_caminho (str): Caminho para o executável.
            app_dir (str): Caminho para o diretório do executável. (Necessário para evitar erros).
        """
        return subprocess.Popen(exe_caminho, cwd=app_dir)
    
    @staticmethod
    def encontrar_janela_por_titulo(trecho: str) -> int:
        """ Retorna o HWND da primeira janela cujo título contenha o 'trecho' especificado."""
        def callback(hwnd: int, extra: list[int]):
            """ 
            Funlção interna que será repassada a API do win32.
            
            Args:
                hwnd (int): ID da janela utilizado pelo windows.
                extra (list): Lista com os HWND (IDs) capturados. OBS: extra é o nome que 'handles' recebe dentro da operação.
            """
            if win32gui.IsWindowVisible(hwnd):
                titulo = win32gui.GetWindowText(hwnd)
                if trecho.strip().lower() in titulo.lower():
                    extra.append(hwnd)
            return True # Por padrão, essas operações param na primeira janela. return True permite que elas continuem.
        
        handles = []
        win32gui.EnumWindows(callback, handles)
        return handles[0] if handles else None


    @staticmethod
    def encontrar_janela_por_pid(pid: int, trecho: str = None) -> int:
        """
        Encontra uma janela através de seu pid (ID da janela no windows).
        
        Args:
            pid (int): pid aqui é o mesmo que HWND. Trata-se do ID da janela.
            trecho (str): Utilizado para validar se o pid realmente corresponde ao trecho procurado.
        """
        def callback(hwnd: int, extra: list[str]):
            if win32gui.IsWindowVisible(hwnd):
                _, janela_pid = win32process.GetWindowThreadProcessId(hwnd)
                if janela_pid == pid:
                    if trecho is None or trecho.lower() in win32gui.GetWindowText(hwnd).lower():
                        extra.append(hwnd)
            return True
        
        handles = []
        win32gui.EnumWindows(callback, handles)
        return handles[0] if handles else None
    
    @staticmethod
    def janela_ativa(hwnd: int) -> bool:
        """ 
        Verifica se o whnd  está ativo no momento 
        
        Args:
            hwnd (int): ID da janela.
        Returns:
            bool: Se sim, True, se não, False.
        """
        # return win32gui.GetForegroundWindow() == hwnd
        return bool(win32gui.IsWindow(hwnd) and win32gui.IsWindowVisible(hwnd))
    
    @staticmethod
    def tornar_topmost(hwnd: int):
        """
        Utiliza o hwnd da janela para coloca-la em topmost (em destaque na tela, acima das demais)
        
        Args:
            hwnd (int): ID da janela.
        """
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        # win32gui.SetWindowPos -> Define a posição das janelas do windows.
        # win32con.SWP_NOMOVE | win32con.SWP_NOSIZE -> Não entendi o que é isso.
        # Também não entendi o que são esses dois últimos zeros (cx, cy)
    
    @staticmethod
    def fechar_janela(hwnd: int) -> None:
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
        # win32gui.PostMessage -> Isso envia uma mensagem? Para o sistema ou para o usuário? Acredito que seja tipo "enviar mensagem de desligar para o sistema"
        # wparam e lparam -> Não entendi o que são.

if __name__ == '__main__':
    # Testando o trecho do programa ====
    import os
    time.sleep(3)
    hwnd = None
    
    # Exemplo de uso:
    exe_caminho: str = r"C:\Arquivos de Programas RFB\Programas SPED\Fiscal\SpedEFD.exe"
    trecho_busca: str = "sped fiscal"
    # hwnd: int = WindowManager.encontrar_janela_por_titulo(trecho_busca)
    # print(f'Janela ativa? {WindowManager.janela_ativa(hwnd)}')
    # print(f'Janela ativa 2? {bool(win32gui.IsWindow(hwnd) and win32gui.IsWindowVisible(hwnd))}')
    
    if hwnd is None:
        # Não encontrou, então abre o programa
        proc: subprocess.Popen = WindowManager.abrir_programa(exe_caminho, os.path.dirname(exe_caminho))
        # Aguarda a janela aparecer (dê um tempo ou use WaitForInputIdle)
        time.sleep(0)  # ou um loop até encontrar
        hwnd = WindowManager.encontrar_janela_por_pid(proc.pid, trecho_busca)
        print(f'{hwnd = }')
        print(f'encontrar_janela_por_titulo: {WindowManager.encontrar_janela_por_titulo(trecho_busca)}')
    
    # if hwnd:
    #     if not WindowManager.janela_ativa(hwnd):
    #         WindowManager.tornar_topmost(hwnd)  # ativa e coloca em topmost
    # else:
    #     print("Janela não encontrada.")