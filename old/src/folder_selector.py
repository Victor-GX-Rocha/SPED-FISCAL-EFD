"""Manages the capture of folder paths for execution."""

import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, Scrollbar, MULTIPLE, END

class FolderSelector:
    def __init__(self):
        self.selected_folders: list[str] = []
        self.__build_window()
        self.__build_main_frame()
        self.__add_buttons()
        self.__add_instructions()
        
    @classmethod
    def get_folders(cls) -> list[str]:
        """Facade method to initialize and return folders in a single line."""
        selector = cls()
        return selector.run()

    def run(self) -> list[str]:
        """Starts the interface loop and returns the selected paths."""
        self.root.mainloop()
        return self.selected_folders
    
    def __build_window(self) -> None:
        self.root = tk.Tk()
        self.root.title("Selecionar Pastas para Processamento")
        self.root.geometry("500x400")
        self.root.attributes('-topmost', True)
    
    def __build_main_frame(self) -> None:
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.listbox = Listbox(self.main_frame, selectmode=MULTIPLE, height=10)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Correção: Mudado para side=tk.RIGHT para o scroll ficar no lugar certo
        self.scrollbar = Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        
        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
    def __add_buttons(self) -> None:
        self.btn_add = tk.Button(self.btn_frame, text="Adicionar Pasta", command=self.add_folder)
        self.btn_add.pack(side=tk.LEFT, padx=5)
        
        self.btn_remove = tk.Button(self.btn_frame, text="Remover Selecionada(s)", command=self.remove_selecteds)
        self.btn_remove.pack(side=tk.LEFT, padx=5)
        
        self.btn_confirm = tk.Button(self.btn_frame, text="Confirmar", command=self.confirm)
        self.btn_confirm.pack(side=tk.RIGHT, padx=5)

    def __add_instructions(self) -> None:
        self.label = tk.Label(self.root, text="Adicione as pastas que contêm os arquivos fiscais.", font=("Arial", 10))
        self.label.pack(pady=5)
        
    def add_folder(self) -> None:
        folder: str = filedialog.askdirectory(
            title="Selecione uma pasta com arquivos fiscais",
            mustexist=True
        )
        
        if not folder:
            return
        
        if folder in self.listbox.get(0, END):
            messagebox.showinfo("Aviso", "Esta pasta já foi adicionada.")
            return 
        
        self.listbox.insert(END, folder)
    
    def remove_selecteds(self) -> None:
        selecteds = self.listbox.curselection()
        
        if not selecteds:
            messagebox.showwarning("Aviso", "Nenhuma pasta selecionada para remover.")
            return
        
        for idx in reversed(selecteds):
            self.listbox.delete(idx)
    
    def confirm(self) -> None:
        folders = list(self.listbox.get(0, END))
        
        if not folders:
            messagebox.showwarning("Aviso", "Nenhuma pasta selecionada.")
            return
        
        self.selected_folders = folders
        self.root.destroy()

if __name__ == "__main__":
    pastas = FolderSelector.get_folders()
    print("Pastas selecionadas:", pastas)
