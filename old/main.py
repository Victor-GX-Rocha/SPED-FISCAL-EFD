""" Execution file """

from src.folder_selector import FolderSelector

def main() -> None:
    """ Execution function """
    
    print("Iniciando o Bot do EFD-ICMS IPI")
    folders = FolderSelector.get_folders()
    
    if not folders:
        print("Nenhuma pasta selecionada. Encerrando.")
        return
    print(f"Pastas selecionadas: {folders}")
    
    processor = BatchProcessor()
    processor.run(folders)
    
    print("Processamento concluído.")

if __name__ == '__main__':
    main()


""" Execution function 
Pensar como se fosse um sistema de rotas.

Rota pacifista (tudo ocorre bem e o arquivo funciona)
    0. O programa está aberto na interface base.
    1. Ele aperta CTRL + I para abrir a janela de escriturações.
    
    
    
    
    
    
Rota pacifista (tudo ocorre bem e o arquivo funciona)
    0. O programa está aberto na interface base.
    1. Ele anda um bloco pro lado e seleciona o arquivo.
        IF 1. Pode ser que o arquivo já estivesse lá. Se sim, só vai, aperta SIM.
        ELSE 2. É o caminho normal, só continua.
        
        NO final de uma validação bem sucedida, o quarto botão (verde de confirmação) já vai estar selecionado.

Lembre-se:
- Se quiser fechar algo é só parter 'esc'

Ideias:
- Como todas as posições dos botões são fixas, eu posso criar um "passador de botões"
    - Dessa forma eu sempre vou saber em que botão eu estou, basta enumerar eles.
    - Eu posso criar uma espécie de "mapa" onde todo botão possui nome e index.
    - Sempre que eu mover o 'tab' para passar ou 'shift + tab' para voltar eu posso ir registrando a mudança nesse indexador.
    - Sempre que o programa saltar diretamente para um botão eu posso fazer o mesmo também. (agora que eu vi 'right' e left' também funcionam)
    - Criar uma espécie de "set_bar_index".
        - Isso é útil porque algumas operações levam diretamente para um botão específico.
    - Eu posso criar um espécie de "move_to" ou melhor "press_button" assim eu deixo esse gerenciador de barra cuidar de tudo!
    - Pensa bem, se eu sempre souber em que botão eu estou agora, vou saber os outros botões que posso me mover, eu posso criar algo como "clique diretamente em certo botão" esse gerenciador só vai precisar verificar em que botão ele está agora e mover a quantidade necessária de casas para chegar lá. 
"""
""" 
# 1. Pegar as pastas
# 2. Passar as pastas para o executador
# 3. Rodar o processo do programa
    # 1. Abrir o programa.
    # 2. Iniciar o loop com todos os arquivos.
        # 1. 
"""