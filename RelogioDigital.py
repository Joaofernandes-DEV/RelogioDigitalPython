import secrets
import string
import tkinter as tk
from tkinter import messagebox, PhotoImage
import os

# --- Lógica de Geração de Senhas (mantida e importada ou integrada) ---
def generate_strong_password(length: int = 12,
                             use_uppercase: bool = True,
                             use_lowercase: bool = True,
                             use_digits: bool = True,
                             use_symbols: bool = True) -> str:
    """
    Gera uma senha aleatória e criptograficamente segura.
    """
    if length < 4:
        raise ValueError("O comprimento da senha deve ser de no mínimo 4 caracteres para segurança.")

    characters = ''
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    if not characters:
        raise ValueError("Pelo menos um tipo de caractere (maiúsculas, minúsculas, dígitos, símbolos) deve ser selecionado.")

    # Garante que pelo menos um caractere de cada tipo selecionado esteja na senha
    # para aumentar a robustez, especialmente para senhas curtas.
    password_list = []
    if use_uppercase:
        password_list.append(secrets.choice(string.ascii_uppercase))
    if use_lowercase:
        password_list.append(secrets.choice(string.ascii_lowercase))
    if use_digits:
        password_list.append(secrets.choice(string.digits))
    if use_symbols:
        password_list.append(secrets.choice(string.punctuation))

    # Preenche o restante do comprimento com caracteres aleatórios dos tipos selecionados
    remaining_length = length - len(password_list)
    if remaining_length < 0: # Caso o comprimento seja menor que o número de tipos selecionados
        password_list = password_list[:length] # Trunca para o comprimento desejado
        remaining_length = 0

    password_list.extend(secrets.choice(characters) for _ in range(remaining_length))
    secrets.SystemRandom().shuffle(password_list) # Embaralha a lista para aleatoriedade
    
    return ''.join(password_list)


# --- Lógica da Interface Gráfica (Tkinter) ---

class PasswordGeneratorApp:
    def __init__(self, master):
        self.master = master
        master.title("Gerador de Senhas Seguras")
        master.geometry("500x250") # Tamanho fixo da janela
        master.resizable(False, False) # Impede o redimensionamento
        
        # Cor de fundo preta suave (dark gray)
        self.bg_color = "#1e1e1e" # Um cinza escuro para ser menos agressivo que preto puro
        self.text_color = "#e0e0e0" # Quase branco para contraste
        self.accent_color = "#88EE88" # Um verde suave para destaque
        self.button_bg_color = "#3a3a3a"
        self.button_active_bg_color = "#555555"

        master.configure(bg=self.bg_color)

        # Configurar estilo para widgets
        self.style = tk.ttk.Style()
        self.style.theme_use('clam') # Um tema que permite mais personalização
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("TLabel", background=self.bg_color, foreground=self.text_color, font=("Segoe UI", 10))
        self.style.configure("TCheckbutton", background=self.bg_color, foreground=self.text_color, font=("Segoe UI", 10), indicatorforeground=self.text_color)
        self.style.map("TCheckbutton", background=[('active', self.bg_color)])
        
        # Estilo para os botões
        self.style.configure("TButton", 
                             background=self.button_bg_color, 
                             foreground=self.text_color, 
                             font=("Segoe UI", 10, "bold"),
                             bordercolor=self.button_bg_color,
                             focusthickness=0,
                             relief="flat")
        self.style.map("TButton", 
                       background=[('active', self.button_active_bg_color)],
                       foreground=[('active', self.accent_color)])
        
        # Estilo para o slider (Scale)
        self.style.configure("TScale", background=self.bg_color, troughcolor=self.button_bg_color, sliderthickness=20)
        self.style.map("TScale", background=[('active', self.bg_color)])


        self._create_widgets()

    def _create_widgets(self):
        # Frame principal para agrupar tudo
        main_frame = tk.Frame(self.master, bg=self.bg_color, padx=20, pady=20)
        main_frame.pack(expand=True, fill="both")

        # Título
        title_label = tk.Label(main_frame, 
                               text="Gerador de Senhas Seguras", 
                               bg=self.bg_color, 
                               fg=self.accent_color, 
                               font=("Segoe UI", 18, "bold"))
        title_label.pack(pady=(0, 20))

        # Comprimento da Senha
        length_frame = tk.Frame(main_frame, bg=self.bg_color)
        length_frame.pack(pady=10, fill="x")

        tk.Label(length_frame, text="Comprimento da Senha:", bg=self.bg_color, fg=self.text_color, font=("Segoe UI", 11)).pack(side="left", padx=(0, 10))
        
        self.length_var = tk.IntVar(value=12)
        self.length_scale = tk.Scale(length_frame, 
                                     from_=6, to=32, 
                                     orient="horizontal", 
                                     variable=self.length_var,
                                     bg=self.bg_color, 
                                     fg=self.text_color, 
                                     highlightbackground=self.bg_color, # Remove borda branca
                                     troughcolor=self.button_bg_color, # Cor da "calha" do slider
                                     activebackground=self.accent_color, # Cor quando ativo/clicado
                                     sliderrelief="flat", # Estilo do "botão" do slider
                                     length=250, # Comprimento visual do slider
                                     font=("Segoe UI", 10))
        self.length_scale.pack(side="right", expand=True, fill="x")

        # Tipos de Caracteres
        options_frame = tk.LabelFrame(main_frame, 
                                      text="Tipos de Caracteres", 
                                      bg=self.bg_color, 
                                      fg=self.text_color, 
                                      font=("Segoe UI", 11, "bold"),
                                      padx=15, pady=10, bd=1, relief="solid", highlightbackground=self.button_bg_color, highlightcolor=self.button_bg_color)
        options_frame.pack(pady=20, padx=10, fill="x")

        self.use_uppercase = tk.BooleanVar(value=True)
        self.use_lowercase = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)

        tk.Checkbutton(options_frame, text="Letras Maiúsculas (A-Z)", variable=self.use_uppercase, 
                       bg=self.bg_color, fg=self.text_color, selectcolor=self.bg_color, 
                       activebackground=self.bg_color, activeforeground=self.accent_color,
                       font=("Segoe UI", 10), relief="flat", highlightbackground=self.bg_color).pack(anchor="w", pady=2)
        tk.Checkbutton(options_frame, text="Letras Minúsculas (a-z)", variable=self.use_lowercase, 
                       bg=self.bg_color, fg=self.text_color, selectcolor=self.bg_color, 
                       activebackground=self.bg_color, activeforeground=self.accent_color,
                       font=("Segoe UI", 10), relief="flat", highlightbackground=self.bg_color).pack(anchor="w", pady=2)
        tk.Checkbutton(options_frame, text="Números (0-9)", variable=self.use_digits, 
                       bg=self.bg_color, fg=self.text_color, selectcolor=self.bg_color, 
                       activebackground=self.bg_color, activeforeground=self.accent_color,
                       font=("Segoe UI", 10), relief="flat", highlightbackground=self.bg_color).pack(anchor="w", pady=2)
        tk.Checkbutton(options_frame, text="Símbolos (!@#$%)", variable=self.use_symbols, 
                       bg=self.bg_color, fg=self.text_color, selectcolor=self.bg_color, 
                       activebackground=self.bg_color, activeforeground=self.accent_color,
                       font=("Segoe UI", 10), relief="flat", highlightbackground=self.bg_color).pack(anchor="w", pady=2)

        # Botão Gerar Senha
        generate_button = tk.Button(main_frame, 
                                    text="Gerar Senha", 
                                    command=self._generate_password_gui,
                                    bg=self.button_bg_color, 
                                    fg=self.text_color, 
                                    activebackground=self.button_active_bg_color, 
                                    activeforeground=self.accent_color,
                                    font=("Segoe UI", 12, "bold"), 
                                    width=20, height=2, 
                                    relief="flat", bd=0)
        generate_button.pack(pady=20)

        # Campo da Senha Gerada
        self.password_entry = tk.Entry(main_frame, 
                                       width=40, 
                                       font=("Consolas", 14), 
                                       bg=self.button_bg_color, # Usar a cor do botão para o campo
                                       fg=self.accent_color, # Cor verde para a senha
                                       insertbackground=self.accent_color, # Cor do cursor
                                       justify="center", 
                                       readonlybackground=self.button_bg_color, # Cor quando somente leitura
                                       relief="flat", bd=0)
        self.password_entry.pack(pady=10)
        
        # Botão Copiar Senha (aparece após a geração)
        self.copy_button = tk.Button(main_frame, 
                                     text="Copiar Senha", 
                                     command=self._copy_password,
                                     bg=self.button_bg_color, 
                                     fg=self.text_color, 
                                     activebackground=self.button_active_bg_color, 
                                     activeforeground=self.accent_color,
                                     font=("Segoe UI", 10), 
                                     width=15, 
                                     relief="flat", bd=0)
        # Ocultar o botão inicialmente
        # self.copy_button.pack_forget() 
        # Packando sempre e desabilitando/habilitando é mais fácil com Tkinter

    def _generate_password_gui(self):
        try:
            length = self.length_var.get()
            password = generate_strong_password(
                length=length,
                use_uppercase=self.use_uppercase.get(),
                use_lowercase=self.use_lowercase.get(),
                use_digits=self.use_digits.get(),
                use_symbols=self.use_symbols.get()
            )
            
            # Limpa o campo e insere a nova senha
            self.password_entry.config(state=tk.NORMAL) # Habilita para edição
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, password)
            self.password_entry.config(state="readonly") # Define como somente leitura
            
            # Habilita o botão de copiar
            self.copy_button.pack(pady=(0,10)) # Mostra o botão após gerar
            self.copy_button.config(state=tk.NORMAL)

        except ValueError as e:
            messagebox.showerror("Erro de Geração", str(e))
            self.password_entry.config(state=tk.NORMAL)
            self.password_entry.delete(0, tk.END)
            self.password_entry.config(state="readonly")
            self.copy_button.config(state=tk.DISABLED) # Desabilita o botão de copiar em caso de erro
        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro: {e}")
            self.password_entry.config(state=tk.NORMAL)
            self.password_entry.delete(0, tk.END)
            self.password_entry.config(state="readonly")
            self.copy_button.config(state=tk.DISABLED)

    def _copy_password(self):
        password = self.password_entry.get()
        if password:
            self.master.clipboard_clear()
            self.master.clipboard_append(password)
            messagebox.showinfo("Copiado!", "Senha copiada para a área de transferência!")
        else:
            messagebox.showwarning("Atenção", "Nenhuma senha para copiar.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()