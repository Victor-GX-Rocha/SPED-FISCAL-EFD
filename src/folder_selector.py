# folder_selector.py
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, Scrollbar, MULTIPLE, END

def select_folders():
    """Abre uma janela para selecionar uma ou mais pastas e retorna uma lista de caminhos."""
    root = tk.Tk()
    root.title("Selecionar Pastas para Processamento")
    root.geometry("500x400")
    root.attributes('-topmost', True)

    # Frame principal
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Listbox para exibir as pastas selecionadas
    listbox = Listbox(main_frame, selectmode=MULTIPLE, height=10)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Scrollbar
    scrollbar = Scrollbar(main_frame, orient=tk.VERTICAL, command=listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox.config(yscrollcommand=scrollbar.set)

    # Frame para botões
    btn_frame = tk.Frame(root)
    btn_frame.pack(fill=tk.X, padx=10, pady=5)

    def adicionar_pasta():
        pasta = filedialog.askdirectory(
            title="Selecione uma pasta com arquivos fiscais",
            mustexist=True
        )
        if pasta:
            # Verifica se já não está na lista
            if pasta not in listbox.get(0, END):
                listbox.insert(END, pasta)
            else:
                messagebox.showinfo("Aviso", "Esta pasta já foi adicionada.")

    def remover_selecionadas():
        selecionados = listbox.curselection()
        if not selecionados:
            messagebox.showwarning("Aviso", "Nenhuma pasta selecionada para remover.")
            return
        # Remove de trás para frente para não alterar índices
        for idx in reversed(selecionados):
            listbox.delete(idx)

    def confirmar():
        pastas = list(listbox.get(0, END))
        if not pastas:
            messagebox.showwarning("Aviso", "Nenhuma pasta selecionada.")
            return
        root.destroy()
        root.pastas_selecionadas = pastas  # Guarda o resultado

    # Botões
    btn_adicionar = tk.Button(btn_frame, text="Adicionar Pasta", command=adicionar_pasta)
    btn_adicionar.pack(side=tk.LEFT, padx=5)

    btn_remover = tk.Button(btn_frame, text="Remover Selecionada(s)", command=remover_selecionadas)
    btn_remover.pack(side=tk.LEFT, padx=5)

    btn_confirmar = tk.Button(btn_frame, text="Confirmar", command=confirmar)
    btn_confirmar.pack(side=tk.RIGHT, padx=5)

    # Instruções
    label = tk.Label(root, text="Adicione as pastas que contêm os arquivos fiscais.", font=("Arial", 10))
    label.pack(pady=5)

    root.mainloop()

    # Após o fechamento, retorna a lista armazenada, se existir
    return getattr(root, 'pastas_selecionadas', [])

if __name__ == "__main__":
    pastas = select_folders()
    print("Pastas selecionadas:", pastas)
