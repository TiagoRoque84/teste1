import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
from fpdf import FPDF

# Cria o banco de dados e a tabela, se não existirem
def create_db():
    conn = sqlite3.connect("pesagens.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS pesagens (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    placa TEXT,
                    motorista TEXT,
                    transportadora TEXT,
                    cliente TEXT,
                    residuos TEXT,
                    tipo TEXT,
                    pesagem_particular REAL,
                    destino TEXT,
                    mtr_sigor TEXT,
                    mtr_feam TEXT,
                    peso1 REAL,
                    peso2 REAL,
                    observacao1 TEXT,
                    observacao2 TEXT,
                    manifesto TEXT,
                    data_entrada TEXT,
                    data_saida TEXT,
                    neto REAL
                )''')
    conn.commit()
    conn.close()

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Pesagem - Aterro Sanitário")
        self.geometry("800x600")
        self.resizable(False, False)
        self.create_widgets()
    
    def create_widgets(self):
        # Cria as abas: Nova Pesagem, Fechar Pesagem e Consulta Pesagens
        notebook = ttk.Notebook(self)
        self.frame_nova = ttk.Frame(notebook)
        self.frame_fechar = ttk.Frame(notebook)
        self.frame_consulta = ttk.Frame(notebook)
        notebook.add(self.frame_nova, text="Nova Pesagem")
        notebook.add(self.frame_fechar, text="Fechar Pesagem")
        notebook.add(self.frame_consulta, text="Consulta Pesagens")
        notebook.pack(expand=1, fill="both")
        self.create_nova_widgets()
        self.create_fechar_widgets()
        self.create_consulta_widgets()
    
    def create_nova_widgets(self):
        row = 0
        # Placa
        ttk.Label(self.frame_nova, text="Placa:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_placa = ttk.Entry(self.frame_nova, width=30)
        self.entry_placa.grid(row=row, column=1, padx=5, pady=5)
        row += 1
        # Motorista
        ttk.Label(self.frame_nova, text="Motorista:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_motorista = ttk.Entry(self.frame_nova, width=30)
        self.entry_motorista.grid(row=row, column=1, padx=5, pady=5)
        row += 1
        # Transportadora
        ttk.Label(self.frame_nova, text="Transportadora:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_transportadora = ttk.Entry(self.frame_nova, width=30)
        self.entry_transportadora.grid(row=row, column=1, padx=5, pady=5)
        row += 1
        # Cliente
        ttk.Label(self.frame_nova, text="Cliente:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_cliente = ttk.Entry(self.frame_nova, width=30)
        self.entry_cliente.grid(row=row, column=1, padx=5, pady=5)
        row += 1
        # Resíduo(s)
        ttk.Label(self.frame_nova, text="Resíduo(s):").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_residuos = ttk.Entry(self.frame_nova, width=30)
        self.entry_residuos.grid(row=row, column=1, padx=5, pady=5)
        row += 1
        # Tipo de Pesagem
        ttk.Label(self.frame_nova, text="Tipo de Pesagem:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.combo_tipo = ttk.Combobox(self.frame_nova, values=["Entrada", "Saída", "Pesagem Particular"], state="readonly")
        self.combo_tipo.grid(row=row, column=1, padx=5, pady=5)
        self.combo_tipo.bind("<<ComboboxSelected>>", self.tipo_changed)
        row += 1
        # Campos para Pesagem Particular (serão exibidos somente se selecionado)
        self.label_pesagem_particular = ttk.Label(self.frame_nova, text="Valor Pesagem Particular:")
        self.entry_pesagem_particular = ttk.Entry(self.frame_nova, width=30)
        # Destino
        ttk.Label(self.frame_nova, text="Destino:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_destino = ttk.Entry(self.frame_nova, width=30)
        self.entry_destino.grid(row=row, column=1, padx=5, pady=5)
        row += 1
        # Campo de MTR
        ttk.Label(self.frame_nova, text="Campo de MTR:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.combo_mtr = ttk.Combobox(self.frame_nova, values=["SIGOR", "FEAM", "Ambos"], state="readonly")
        self.combo_mtr.grid(row=row, column=1, padx=5, pady=5)
        self.combo_mtr.bind("<<ComboboxSelected>>", self.mtr_changed)
        row += 1
        # Frame para os campos dinâmicos de MTR
        self.frame_mtr_extra = ttk.Frame(self.frame_nova)
        self.frame_mtr_extra.grid(row=row, column=0, columnspan=4, sticky=tk.W, padx=5, pady=5)
        row += 1
        # Peso (Kg)
        ttk.Label(self.frame_nova, text="Peso (Kg):").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_peso = ttk.Entry(self.frame_nova, width=30)
        self.entry_peso.grid(row=row, column=1, padx=5, pady=5)
        row += 1
        # Observação 1
        ttk.Label(self.frame_nova, text="Observação 1:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.text_obs1 = tk.Text(self.frame_nova, width=40, height=3)
        self.text_obs1.grid(row=row, column=1, padx=5, pady=5, columnspan=3)
        row += 1
        # Observação 2
        ttk.Label(self.frame_nova, text="Observação 2:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.text_obs2 = tk.Text(self.frame_nova, width=40, height=3)
        self.text_obs2.grid(row=row, column=1, padx=5, pady=5, columnspan=3)
        row += 1
        # Manifesto
        ttk.Label(self.frame_nova, text="Manifesto:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_manifesto = ttk.Entry(self.frame_nova, width=30)
        self.entry_manifesto.grid(row=row, column=1, padx=5, pady=5)
        row += 1
        # Botões: Cancelar, Fechar e Salvar
        self.button_cancel = ttk.Button(self.frame_nova, text="Cancelar", command=self.clear_nova_form)
        self.button_cancel.grid(row=row, column=0, padx=5, pady=10)
        self.button_fechar = ttk.Button(self.frame_nova, text="Fechar", command=self.destroy)
        self.button_fechar.grid(row=row, column=1, padx=5, pady=10)
        self.button_salvar = ttk.Button(self.frame_nova, text="Salvar", command=self.save_new_weighing)
        self.button_salvar.grid(row=row, column=2, padx=5, pady=10)
    
    def tipo_changed(self, event):
        # Exibe os campos de Pesagem Particular se essa opção for selecionada
        tipo = self.combo_tipo.get()
        if tipo == "Pesagem Particular":
            self.label_pesagem_particular.grid(row=5, column=2, sticky=tk.W, padx=5, pady=5)
            self.entry_pesagem_particular.grid(row=5, column=3, padx=5, pady=5)
        else:
            self.label_pesagem_particular.grid_forget()
            self.entry_pesagem_particular.grid_forget()
    
    def mtr_changed(self, event):
        # Limpa e recria os campos dinâmicos de MTR conforme a seleção
        for widget in self.frame_mtr_extra.winfo_children():
            widget.destroy()
        mtr = self.combo_mtr.get()
        if mtr == "SIGOR":
            ttk.Label(self.frame_mtr_extra, text="Número MTR SIGOR:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
            self.entry_mtr_sigor = ttk.Entry(self.frame_mtr_extra, width=30)
            self.entry_mtr_sigor.grid(row=0, column=1, padx=5, pady=5)
        elif mtr == "FEAM":
            ttk.Label(self.frame_mtr_extra, text="Número MTR FEAM:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
            self.entry_mtr_feam = ttk.Entry(self.frame_mtr_extra, width=30)
            self.entry_mtr_feam.grid(row=0, column=1, padx=5, pady=5)
        elif mtr == "Ambos":
            ttk.Label(self.frame_mtr_extra, text="Número MTR SIGOR:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
            self.entry_mtr_sigor = ttk.Entry(self.frame_mtr_extra, width=30)
            self.entry_mtr_sigor.grid(row=0, column=1, padx=5, pady=5)
            ttk.Label(self.frame_mtr_extra, text="Número MTR FEAM:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
            self.entry_mtr_feam = ttk.Entry(self.frame_mtr_extra, width=30)
            self.entry_mtr_feam.grid(row=1, column=1, padx=5, pady=5)
    
    def clear_nova_form(self):
        # Limpa todos os campos da aba "Nova Pesagem"
        self.entry_placa.delete(0, tk.END)
        self.entry_motorista.delete(0, tk.END)
        self.entry_transportadora.delete(0, tk.END)
        self.entry_cliente.delete(0, tk.END)
        self.entry_residuos.delete(0, tk.END)
        self.combo_tipo.set('')
        self.entry_pesagem_particular.delete(0, tk.END)
        self.entry_destino.delete(0, tk.END)
        self.combo_mtr.set('')
        for widget in self.frame_mtr_extra.winfo_children():
            widget.destroy()
        self.entry_peso.delete(0, tk.END)
        self.text_obs1.delete("1.0", tk.END)
        self.text_obs2.delete("1.0", tk.END)
        self.entry_manifesto.delete(0, tk.END)
    
    def save_new_weighing(self):
        # Captura os dados e salva a nova pesagem no banco
        placa = self.entry_placa.get()
        motorista = self.entry_motorista.get()
        transportadora = self.entry_transportadora.get()
        cliente = self.entry_cliente.get()
        residuos = self.entry_residuos.get()
        tipo = self.combo_tipo.get()
        pes_part = self.entry_pesagem_particular.get() if tipo == "Pesagem Particular" else None
        destino = self.entry_destino.get()
        mtr = self.combo_mtr.get()
        mtr_sigor = self.entry_mtr_sigor.get() if mtr in ["SIGOR", "Ambos"] and hasattr(self, "entry_mtr_sigor") else None
        mtr_feam = self.entry_mtr_feam.get() if mtr in ["FEAM", "Ambos"] and hasattr(self, "entry_mtr_feam") else None
        try:
            peso = float(self.entry_peso.get())
        except ValueError:
            messagebox.showerror("Erro", "Peso inválido.")
            return
        obs1 = self.text_obs1.get("1.0", tk.END).strip()
        obs2 = self.text_obs2.get("1.0", tk.END).strip()
        manifesto = self.entry_manifesto.get()
        data_entrada = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        conn = sqlite3.connect("pesagens.db")
        c = conn.cursor()
        c.execute('''INSERT INTO pesagens 
            (placa, motorista, transportadora, cliente, residuos, tipo, pesagem_particular, destino, mtr_sigor, mtr_feam, peso1, observacao1, observacao2, manifesto, data_entrada)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (placa, motorista, transportadora, cliente, residuos, tipo, pes_part, destino, mtr_sigor, mtr_feam, peso, obs1, obs2, manifesto, data_entrada))
        conn.commit()
        ticket_id = c.lastrowid
        conn.close()
        
        messagebox.showinfo("Sucesso", f"Pesagem salva com sucesso! Ticket: {ticket_id}")
        self.clear_nova_form()
        self.load_open_weighings()
        self.load_concluded_weighings()
    
    def create_fechar_widgets(self):
        # Aba para fechar pesagens abertas
        left_frame = ttk.Frame(self.frame_fechar)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        right_frame = ttk.Frame(self.frame_fechar)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(left_frame, text="Pesagens Abertas").pack(pady=5)
        self.tree_open = ttk.Treeview(left_frame, columns=("ID", "Placa", "Cliente", "Peso Entrada", "Data Entrada"), show="headings")
        self.tree_open.heading("ID", text="ID")
        self.tree_open.heading("Placa", text="Placa")
        self.tree_open.heading("Cliente", text="Cliente")
        self.tree_open.heading("Peso Entrada", text="Peso Entrada")
        self.tree_open.heading("Data Entrada", text="Data Entrada")
        self.tree_open.pack(fill=tk.BOTH, expand=True)
        btn_fechar = ttk.Button(left_frame, text="Fechar Peso", command=self.open_fechar_peso_window)
        btn_fechar.pack(pady=10)
        
        # Detalhes do registro selecionado (lado direito)
        ttk.Label(right_frame, text="Detalhes da Pesagem Selecionada").grid(row=0, column=0, columnspan=2, pady=5)
        ttk.Label(right_frame, text="ID:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.label_detail_id = ttk.Label(right_frame, text="")
        self.label_detail_id.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(right_frame, text="Placa:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.label_detail_placa = ttk.Label(right_frame, text="")
        self.label_detail_placa.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(right_frame, text="Peso Entrada:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.label_detail_peso1 = ttk.Label(right_frame, text="")
        self.label_detail_peso1.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
        self.tree_open.bind("<<TreeviewSelect>>", self.on_tree_open_select)
        self.load_open_weighings()
    
    def load_open_weighings(self):
        # Carrega os registros com peso2 ainda não informado (exceto Pesagem Particular)
        for item in self.tree_open.get_children():
            self.tree_open.delete(item)
        conn = sqlite3.connect("pesagens.db")
        c = conn.cursor()
        c.execute("SELECT id, placa, cliente, peso1, data_entrada FROM pesagens WHERE peso2 IS NULL AND tipo != 'Pesagem Particular'")
        rows = c.fetchall()
        for row in rows:
            self.tree_open.insert("", tk.END, values=row)
        conn.close()
    
    def on_tree_open_select(self, event):
        # Exibe os detalhes do registro selecionado na aba "Fechar Pesagem"
        selected = self.tree_open.selection()
        if selected:
            item = self.tree_open.item(selected[0])
            values = item["values"]  # Ordem: id, placa, cliente, peso1, data_entrada
            self.label_detail_id.config(text=values[0])
            self.label_detail_placa.config(text=values[1])
            self.label_detail_peso1.config(text=values[3])
    
    def open_fechar_peso_window(self):
        # Abre uma janela para fechar o peso de um registro selecionado
        selected = self.tree_open.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione uma pesagem aberta para fechar.")
            return
        item = self.tree_open.item(selected[0])
        values = item["values"]  # [id, placa, cliente, peso1, data_entrada]
        id_val = values[0]
        placa = values[1]
        peso1 = values[3]
        
        win = tk.Toplevel(self)
        win.title("Fechar Peso")
        win.geometry("400x200")
        
        ttk.Label(win, text=f"ID: {id_val}").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(win, text=f"Placa: {placa}").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(win, text=f"Peso Entrada: {peso1} Kg").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(win, text="Peso de Saída (Kg):").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        
        entry_peso_saida = ttk.Entry(win, width=20)
        entry_peso_saida.grid(row=3, column=1, padx=5, pady=5)
        
        def confirmar_fechamento():
            try:
                peso2 = float(entry_peso_saida.get())
            except ValueError:
                messagebox.showerror("Erro", "Peso de Saída inválido.")
                return
            neto = abs(float(peso1) - peso2)
            data_saida = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            conn = sqlite3.connect("pesagens.db")
            c = conn.cursor()
            c.execute("UPDATE pesagens SET peso2=?, data_saida=?, neto=? WHERE id=?", (peso2, data_saida, neto, id_val))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", f"Fechamento salvo! Peso líquido: {neto} Kg")
            self.generate_pdf(id_val)
            win.destroy()
            self.load_open_weighings()
            self.load_concluded_weighings()
        
        btn_confirmar = ttk.Button(win, text="Confirmar Fechamento", command=confirmar_fechamento)
        btn_confirmar.grid(row=4, column=0, columnspan=2, pady=10)
    
    def create_consulta_widgets(self):
        # Aba de Consulta de Pesagens Concluídas
        frame = self.frame_consulta
        ttk.Label(frame, text="Pesagens Concluídas").pack(pady=5)
        self.tree_consult = ttk.Treeview(frame, columns=("ID", "Placa", "Cliente", "Peso Entrada", "Peso Saída", "Peso Líquido", "Data Entrada", "Data Saída"), show="headings")
        self.tree_consult.heading("ID", text="ID")
        self.tree_consult.heading("Placa", text="Placa")
        self.tree_consult.heading("Cliente", text="Cliente")
        self.tree_consult.heading("Peso Entrada", text="Peso Entrada")
        self.tree_consult.heading("Peso Saída", text="Peso Saída")
        self.tree_consult.heading("Peso Líquido", text="Peso Líquido")
        self.tree_consult.heading("Data Entrada", text="Data Entrada")
        self.tree_consult.heading("Data Saída", text="Data Saída")
        self.tree_consult.pack(fill=tk.BOTH, expand=True)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)
        btn_reprint = ttk.Button(btn_frame, text="Reimprimir PDF", command=self.reimprimir_pdf)
        btn_reprint.pack(side=tk.LEFT, padx=5)
        btn_refresh = ttk.Button(btn_frame, text="Atualizar", command=self.load_concluded_weighings)
        btn_refresh.pack(side=tk.LEFT, padx=5)
        
        self.load_concluded_weighings()
    
    def load_concluded_weighings(self):
        # Carrega os registros com peso2 informado (pesagens concluídas)
        for item in self.tree_consult.get_children():
            self.tree_consult.delete(item)
        conn = sqlite3.connect("pesagens.db")
        c = conn.cursor()
        c.execute("SELECT id, placa, cliente, peso1, peso2, neto, data_entrada, data_saida FROM pesagens WHERE peso2 IS NOT NULL")
        rows = c.fetchall()
        for row in rows:
            self.tree_consult.insert("", tk.END, values=row)
        conn.close()
    
    def reimprimir_pdf(self):
        # Reimprime o PDF da pesagem selecionada na aba "Consulta Pesagens"
        selected = self.tree_consult.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione uma pesagem concluída para reimprimir.")
            return
        item = self.tree_consult.item(selected[0])
        values = item["values"]
        id_val = values[0]
        self.generate_pdf(id_val)
    
    def generate_pdf(self, id_val):
        # Gera um PDF com os dados da pesagem para impressão
        conn = sqlite3.connect("pesagens.db")
        c = conn.cursor()
        c.execute("SELECT * FROM pesagens WHERE id=?", (id_val,))
        record = c.fetchone()
        conn.close()
        if not record:
            messagebox.showerror("Erro", "Registro não encontrado para PDF.")
            return
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        campos = ["ID", "Placa", "Motorista", "Transportadora", "Cliente", "Resíduos", "Tipo",
                  "Pesagem Particular", "Destino", "MTR SIGOR", "MTR FEAM", "Peso Entrada",
                  "Peso Saída", "Observação 1", "Observação 2", "Manifesto", "Data Entrada",
                  "Data Saída", "Peso Líquido"]
        for i, campo in enumerate(campos):
            valor = record[i] if record[i] is not None else ""
            pdf.cell(0, 10, f"{campo}: {valor}", ln=True)
        filename = f"pesagem_{id_val}.pdf"
        pdf.output(filename)
        messagebox.showinfo("PDF Gerado", f"PDF gerado: {filename}")

if __name__ == "__main__":
    create_db()
    app = Application()
    app.mainloop()
