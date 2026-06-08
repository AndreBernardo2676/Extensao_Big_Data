import tkinter as tk
from tkinter import messagebox

from database.criar_banco import criar_banco
from views.tela_principal import TelaPrincipal



USUARIO_PADRAO = "admin"
SENHA_PADRAO = "admin"


class TelaLogin:
    

    def __init__(self, root):
        self.root = root
        self.root.title("Login - Sistema de Vendas")
        self.root.geometry("360x240")
        self.root.resizable(False, False)
        self.root.configure(bg="#f4f4f4")

       
        titulo = tk.Label(
            root,
            text="Sistema de Vendas",
            font=("Arial", 16, "bold"),
            bg="#f4f4f4",
            fg="#222",
        )
        titulo.pack(pady=15)

       
        frame = tk.Frame(root, bg="#f4f4f4")
        frame.pack(pady=5)

        tk.Label(frame, text="Usuário:", bg="#f4f4f4").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_usuario = tk.Entry(frame, width=22)
        self.entry_usuario.grid(row=0, column=1, padx=5, pady=5)
        self.entry_usuario.insert(0, "admin")

        tk.Label(frame, text="Senha:", bg="#f4f4f4").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_senha = tk.Entry(frame, width=22, show="*")
        self.entry_senha.grid(row=1, column=1, padx=5, pady=5)

      
        btn_entrar = tk.Button(
            root,
            text="Entrar",
            width=15,
            bg="#2d6cdf",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.autenticar,
        )
        btn_entrar.pack(pady=15)

        
        self.root.bind("<Return>", lambda event: self.autenticar())

      
        dica = tk.Label(
            root,
            text="(usuário: admin   |   senha: admin)",
            font=("Arial", 8),
            bg="#f4f4f4",
            fg="#666",
        )
        dica.pack()

    def autenticar(self):
        
        usuario = self.entry_usuario.get().strip()
        senha = self.entry_senha.get().strip()

        if usuario == USUARIO_PADRAO and senha == SENHA_PADRAO:
            self.root.destroy()
            
            root_principal = tk.Tk()
            TelaPrincipal(root_principal)
            root_principal.mainloop()
        else:
            messagebox.showerror("Erro de Login", "Usuário ou senha inválidos.")


def main():
    
    criar_banco()

    
    root = tk.Tk()
    TelaLogin(root)
    root.mainloop()


if __name__ == "__main__":
    main()
