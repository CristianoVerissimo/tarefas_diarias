import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

frame_em_edicao = None

def iniciar_programa_principal():
    global frame_em_edicao
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
                adicionar_item_tarefa(tarefa)
            entrada_tarefa.delete(0, ctk.END)
        else:
            messagebox.showwarning("Entrada Inválida", "Por favor, insira uma tarefa válida.")

    def adicionar_item_tarefa(tarefa):
        frame_tarefa = ctk.CTkFrame(canvas_interior, corner_radius=5)

        label_tarefa = ctk.CTkLabel(frame_tarefa, text=tarefa, font=("Garamond", 16), width=300, anchor="w")
        label_tarefa.pack(side=ctk.LEFT, fill=ctk.X, padx=10, pady=5)

        botao_editar = ctk.CTkButton(frame_tarefa, text="Editar", width=70, command=lambda f=frame_tarefa, l=label_tarefa: preparar_edicao(f, l))
        botao_editar.pack(side=ctk.RIGHT, padx=5)

        botao_deletar = ctk.CTkButton(frame_tarefa, text="Deletar", width=70, fg_color="red", command=lambda f=frame_tarefa: deletar_tarefa(f))
        botao_deletar.pack(side=ctk.RIGHT, padx=5)

        frame_tarefa.pack(fill=ctk.X, padx=5, pady=5)

        checkbutton = ctk.CTkCheckBox(frame_tarefa, text="", command=lambda label=label_tarefa: alternar_sublinhado(label))
        checkbutton.pack(side=ctk.RIGHT, padx=5)

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

    def deletar_tarefa(frame_tarefa):
        frame_tarefa.destroy()
        canvas_interior.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    def alternar_sublinhado(label):
        fonte_atual = label.cget("font")
        if "overstrike" in fonte_atual:
            nova_fonte = fonte_atual[:-1]
        else:
            nova_fonte = fonte_atual + ("overstrike",)
        label.configure(font=nova_fonte)

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

    janela.mainloop()

if __name__ == "__main__":
    iniciar_programa_principal()
