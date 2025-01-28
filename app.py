import customtkinter as ctk
from tkinter import messagebox
import sqlite3

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

frame_em_edicao = None
conn = None

def conectar_bd():
    global conn
    conn = sqlite3.connect('tarefas.db')
    criar_tabela()

def criar_tabela():
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tarefas
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     tarefa TEXT NOT NULL,
                     concluida BOOLEAN NOT NULL DEFAULT 0)''')
    conn.commit()

def carregar_tarefas():
    cursor = conn.cursor()
    cursor.execute("SELECT id, tarefa, concluida FROM tarefas")
    return cursor.fetchall()

def adicionar_tarefa_bd(tarefa):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tarefas (tarefa) VALUES (?)", (tarefa,))
    conn.commit()
    return cursor.lastrowid

def atualizar_tarefa_bd(id_tarefa, nova_tarefa):
    cursor = conn.cursor()
    cursor.execute("UPDATE tarefas SET tarefa = ? WHERE id = ?", (nova_tarefa, id_tarefa))
    conn.commit()

def alternar_status_bd(id_tarefa, status):
    cursor = conn.cursor()
    cursor.execute("UPDATE tarefas SET concluida = ? WHERE id = ?", (status, id_tarefa))
    conn.commit()

def deletar_tarefa_bd(id_tarefa):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tarefas WHERE id = ?", (id_tarefa,))
    conn.commit()

def iniciar_programa_principal():
    global frame_em_edicao, conn
    conectar_bd()
    
    janela = ctk.CTk()
    janela.title("Tarefas Diárias")
    janela.geometry("1024x768")

    def adicionar_tarefa():
        global frame_em_edicao
        tarefa = entrada_tarefa.get().strip()
        if tarefa and tarefa != "Inserir Tarefa":
            if frame_em_edicao is not None:
                atualizar_tarefa(tarefa)
                frame_em_edicao = None
            else:
                id_tarefa = adicionar_tarefa_bd(tarefa)
                adicionar_item_tarefa(tarefa, id_tarefa)
            entrada_tarefa.delete(0, ctk.END)
        else:
            messagebox.showwarning("Entrada Inválida", "Por favor, insira uma tarefa válida.")

    def adicionar_item_tarefa(tarefa, id_tarefa, concluida=False):
        frame_tarefa = ctk.CTkFrame(canvas_interior, corner_radius=5)
        frame_tarefa.id = id_tarefa

        label_tarefa = ctk.CTkLabel(frame_tarefa, text=tarefa, font=("Garamond", 16), width=300, anchor="w")
        if concluida:
            label_tarefa.configure(font=("Garamond", 16, "overstrike"))
        label_tarefa.pack(side=ctk.LEFT, fill=ctk.X, padx=10, pady=5)

        botao_editar = ctk.CTkButton(frame_tarefa, text="Editar", width=70, 
                                   command=lambda: preparar_edicao(frame_tarefa, label_tarefa))
        botao_editar.pack(side=ctk.RIGHT, padx=5)

        botao_deletar = ctk.CTkButton(frame_tarefa, text="Deletar", width=70, fg_color="red",
                                    command=lambda: deletar_tarefa(frame_tarefa))
        botao_deletar.pack(side=ctk.RIGHT, padx=5)

        checkbutton = ctk.CTkCheckBox(frame_tarefa, text="", 
                                    command=lambda: alternar_sublinhado(label_tarefa, frame_tarefa.id))
        checkbutton.pack(side=ctk.RIGHT, padx=5)
        if concluida:
            checkbutton.select()

        frame_tarefa.pack(fill=ctk.X, padx=5, pady=5)
        canvas_interior.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    def preparar_edicao(frame_tarefa, label_tarefa):
        global frame_em_edicao
        frame_em_edicao = frame_tarefa
        entrada_tarefa.delete(0, ctk.END)
        entrada_tarefa.insert(0, label_tarefa.cget("text"))

    def atualizar_tarefa(nova_tarefa):
        global frame_em_edicao
        for widget in frame_em_edicao.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.configure(text=nova_tarefa)
        atualizar_tarefa_bd(frame_em_edicao.id, nova_tarefa)

    def deletar_tarefa(frame_tarefa):
        deletar_tarefa_bd(frame_tarefa.id)
        frame_tarefa.destroy()
        canvas_interior.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    def alternar_sublinhado(label, id_tarefa):
        fonte_atual = label.cget("font")
        novo_status = not ("overstrike" in fonte_atual)
        
        if novo_status:
            nova_fonte = fonte_atual + ("overstrike",)
        else:
            nova_fonte = ("Garamond", 16)
            
        label.configure(font=nova_fonte)
        alternar_status_bd(id_tarefa, novo_status)

    # Restante da interface
    rotulo_cabecalho = ctk.CTkLabel(janela, text="Tarefas Diárias", font=("Garamond", 24, "bold"))
    rotulo_cabecalho.pack(pady=20)

    frame = ctk.CTkFrame(janela)
    frame.pack(pady=10)

    entrada_tarefa = ctk.CTkEntry(frame, placeholder_text="Inserir Tarefa", font=("Garamond", 14), width=300)
    entrada_tarefa.pack(side=ctk.LEFT, padx=10)

    botao_adicionar = ctk.CTkButton(frame, text="Adicionar", command=adicionar_tarefa, width=100)
    botao_adicionar.pack(side=ctk.LEFT, padx=10)
    
    frame_lista_tarefas = ctk.CTkFrame(janela)
    frame_lista_tarefas.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)
    
    canvas = ctk.CTkCanvas(frame_lista_tarefas)
    canvas.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
    
    scrollbar = ctk.CTkScrollbar(frame_lista_tarefas, orientation="vertical", command=canvas.yview)
    scrollbar.pack(side=ctk.RIGHT, fill=ctk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas_interior = ctk.CTkFrame(canvas)
    canvas.create_window((0, 0), window=canvas_interior, anchor="nw")
    canvas_interior.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    for tarefa in carregar_tarefas():
        id_tarefa, texto_tarefa, concluida = tarefa
        adicionar_item_tarefa(texto_tarefa, id_tarefa, concluida)

    janela.protocol("WM_DELETE_WINDOW", lambda: (conn.close(), janela.destroy()))
    janela.mainloop()

if __name__ == "__main__":
    iniciar_programa_principal()