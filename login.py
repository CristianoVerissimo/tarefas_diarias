import customtkinter as ctk
from tkinter import messagebox
from app import iniciar_programa_principal

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

USUARIO_VALIDO = "admin"
SENHA_VALIDA = "12345"

def verificar_login():
    usuario = entrada_usuario.get()
    senha = entrada_senha.get()
    if usuario == USUARIO_VALIDO and senha == SENHA_VALIDA:
        tela_login.destroy()
        iniciar_programa_principal()
    else:
        messagebox.showerror("Login Inválido", "Usuário ou senha incorretos.")

tela_login = ctk.CTk()
tela_login.title("Login")
tela_login.geometry("400x300")

rotulo_login = ctk.CTkLabel(tela_login, text="Login", font=("Garamond", 24, "bold"))
rotulo_login.pack(pady=20)

frame_login = ctk.CTkFrame(tela_login)
frame_login.pack(pady=20)

entrada_usuario = ctk.CTkEntry(frame_login, placeholder_text="Usuário", font=("Arial", 14), width=250)
entrada_usuario.pack(pady=10)

entrada_senha = ctk.CTkEntry(frame_login, placeholder_text="Senha", font=("Arial", 14), show="*", width=250)
entrada_senha.pack(pady=10)

botao_login = ctk.CTkButton(frame_login, text="Entrar", command=verificar_login)
botao_login.pack(pady=10)

tela_login.mainloop()
