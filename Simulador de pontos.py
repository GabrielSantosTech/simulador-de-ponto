
import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
import random
from datetime import datetime, timedelta

# --- ESTRUTURA DE DADOS E CONSTANTES ---

DIAS_SEMANA_NOME = { 0: "Segunda-feira", 1: "Terça-feira", 2: "Quarta-feira", 3: "Quinta-feira", 4: "Sexta-feira", 5: "Sábado", 6: "Domingo" }

info_cargos = {
    "func": {"descricao": "Segunda a Sexta, 9h-18h.", "dias_trabalho": [0, 1, 2, 3, 4], "salario_diario": 120},
    "segurança": {"descricao": "Segunda a Sexta, 9h-18h.", "dias_trabalho": [0, 1, 2, 3, 4], "salario_diario": 110},
    "t.i": {"descricao": "Apenas aos Sábados, 19h-22h.", "dias_trabalho": [5], "salario_diario": 250},
    "ceo": {"descricao": "Trabalho flexível.", "dias_trabalho": "flex", "salario_diario": 800},
    "dono": {"descricao": "Você é o dono, não bate ponto.", "dias_trabalho": [], "salario_diario": 2000},
    "marketing": {"descricao": "Híbrido: Seg, Qua, Sex.", "dias_trabalho": [0, 2, 4], "salario_diario": 180},
    "rh": {"descricao": "Segunda a Sexta, 8h-17h.", "dias_trabalho": [0, 1, 2, 3, 4], "salario_diario": 160},
    "estagiario": {"descricao": "Segunda a Sexta, 6h/dia.", "dias_trabalho": [0, 1, 2, 3, 4], "salario_diario": 60}
}

CLIMAS_POSSIVEIS = [
    ("Ensolarado", "Tolerância normal."),
    ("Nublado", "Tolerância normal."),
    ("Chuva Leve", "Tolerância de 15 minutos para atrasos."),
    ("Tempestade", "Trabalho remoto permitido ou tolerância de 1 hora."),
    ("Neve", "Folga remunerada! (Em um cenário hipotético no Brasil)")
]

ARQUIVO_USUARIOS = "usuarios.json"

# Palavras-chave para justificar uma ausência
MOTIVOS_JUSTIFICADOS_KEYWORDS = ['médico', 'doente', 'doença', 'emergência', 'família', 'exame', 'luto', 'consulta']


# --- CLASSE PARA GERENCIAR DADOS DO USUÁRIO ---

class Usuario:
    def __init__(self, username, nome_completo, senha, cargo):
        self.username = username
        self.nome_completo = nome_completo
        self.senha = senha
        self.cargo = cargo
        # Dados da simulação
        self.salario_acumulado = 0.0
        self.dias_para_pagamento = 30
        self.data_atual = datetime.now().date() # Usa a data real como ponto de partida
        self.clima_atual = random.choice(CLIMAS_POSSIVEIS)

    def to_dict(self):
        """Converte o objeto Usuario para um dicionário para salvar em JSON."""
        return {
            "nome_completo": self.nome_completo,
            "senha": self.senha,
            "cargo": self.cargo,
            "simulacao": {
                "salario_acumulado": self.salario_acumulado,
                "dias_para_pagamento": self.dias_para_pagamento,
                "data_atual": self.data_atual.isoformat() # Salva a data como string
            }
        }

    @staticmethod
    def from_dict(username, data):
        """Cria um objeto Usuario a partir de um dicionário."""
        usuario = Usuario(username, data['nome_completo'], data['senha'], data['cargo'])
        # Carrega dados da simulação se existirem
        if 'simulacao' in data:
            sim_data = data['simulacao']
            usuario.salario_acumulado = sim_data.get('salario_acumulado', 0.0)
            usuario.dias_para_pagamento = sim_data.get('dias_para_pagamento', 30)
            # Carrega a data a partir da string, ou usa a data atual se não existir
            data_salva = sim_data.get('data_atual')
            if data_salva:
                usuario.data_atual = datetime.fromisoformat(data_salva).date()
            else:
                # Compatibilidade com saves antigos
                dia_semana_antigo = sim_data.get('dia_semana_atual', 0)
                usuario.data_atual = datetime.now().date() # Apenas um fallback
        return usuario

# --- CLASSE PRINCIPAL DA APLICAÇÃO ---

class VerificadorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Ponto e Salário v2.0")
        self.root.geometry("1920x1080") # Alterado para 1920x1080
        self.root.state('zoomed') # Inicia a janela maximizada
        self.root.configure(bg="#2c3e50")
        self.root.resizable(False, False)  # Torna a janela não redimensionável
        
        self.usuarios_db = self.carregar_usuarios()
        self.usuario_logado = None
        self.usuario_atual = None
        
        self.criar_widgets_inicial()

    def carregar_usuarios(self):
        if os.path.exists(ARQUIVO_USUARIOS):
            try:
                with open(ARQUIVO_USUARIOS, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}

    def salvar_usuarios(self):
        try:
            with open(ARQUIVO_USUARIOS, "w") as f:
                json.dump(self.usuarios_db, f, indent=4)
        except IOError:
            messagebox.showerror("Erro", "Não foi possível salvar os dados.")

    def criar_widgets_inicial(self):
        self.limpar_tela()
        
        frame_login = tk.Frame(self.root, bg="#2c3e50")
        frame_login.pack(expand=True)

        tk.Label(frame_login, text="Login ou Registro", font=("Segoe UI", 22, "bold"), bg="#2c3e50", fg="#ecf0f1").pack(pady=(0, 20))

        # Botões para Login e Registro
        tk.Button(
            frame_login, text="Login", font=("Segoe UI", 12, "bold"),
            bg="#1abc9c", fg="#ffffff", command=self.criar_widgets_login, relief="flat", width=20
        ).pack(pady=10)
        
        tk.Button(
            frame_login, text="Registrar Novo Usuário", font=("Segoe UI", 12, "bold"),
            bg="#3498db", fg="#ffffff", command=self.criar_widgets_registro, relief="flat", width=20
        ).pack(pady=10)

    def criar_widgets_login(self):
        self.limpar_tela()
        
        frame_login = tk.Frame(self.root, bg="#2c3e50")
        frame_login.pack(expand=True)

        tk.Label(frame_login, text="Login do Funcionário", font=("Segoe UI", 22, "bold"), bg="#2c3e50", fg="#ecf0f1").pack(pady=(0, 20))

        tk.Label(frame_login, text="Cargo:", font=("Segoe UI", 12), bg="#2c3e50", fg="#ecf0f1").pack(anchor="w")
        self.entry_cargo_login = tk.Entry(frame_login, font=("Segoe UI", 12), width=30)
        self.entry_cargo_login.pack(pady=(0, 10))

        tk.Label(frame_login, text="Senha:", font=("Segoe UI", 12), bg="#2c3e50", fg="#ecf0f1").pack(anchor="w")
        self.entry_senha_login = tk.Entry(frame_login, font=("Segoe UI", 12), width=30, show="*")
        self.entry_senha_login.pack(pady=(0, 20))

        self.botao_login = tk.Button(
            frame_login, text="Entrar", font=("Segoe UI", 12, "bold"),
            bg="#1abc9c", fg="#ffffff", command=self.fazer_login, relief="flat", width=20
        )
        self.botao_login.pack(pady=10)

        # Botão para ver todos os cargos
        self.botao_ver_cargos = tk.Button(
            frame_login, text="Ver Todos os Cargos", font=("Segoe UI", 10),
            bg="#3498db", fg="#ffffff", command=self.mostrar_cargos, relief="flat", width=20
        )
        self.botao_ver_cargos.pack(pady=5)

        # Botão para voltar
        tk.Button(
            frame_login, text="Voltar", font=("Segoe UI", 10),
            bg="#e74c3c", fg="#ffffff", command=self.criar_widgets_inicial, relief="flat", width=20
        ).pack(pady=5)

    def criar_widgets_registro(self):
        self.limpar_tela()
        
        frame_registro = tk.Frame(self.root, bg="#2c3e50")
        frame_registro.pack(expand=True)

        tk.Label(frame_registro, text="Registro de Novo Usuário", font=("Segoe UI", 22, "bold"), bg="#2c3e50", fg="#ecf0f1").pack(pady=(0, 20))

        tk.Label(frame_registro, text="Cargo:", font=("Segoe UI", 12), bg="#2c3e50", fg="#ecf0f1").pack(anchor="w")
        self.entry_cargo_registro = tk.Entry(frame_registro, font=("Segoe UI", 12), width=30)
        self.entry_cargo_registro.pack(pady=(0, 10))

        tk.Label(frame_registro, text="Nome Completo:", font=("Segoe UI", 12), bg="#2c3e50", fg="#ecf0f1").pack(anchor="w")
        self.entry_nome_registro = tk.Entry(frame_registro, font=("Segoe UI", 12), width=30)
        self.entry_nome_registro.pack(pady=(0, 10))

        tk.Label(frame_registro, text="Senha:", font=("Segoe UI", 12), bg="#2c3e50", fg="#ecf0f1").pack(anchor="w")
        self.entry_senha_registro = tk.Entry(frame_registro, font=("Segoe UI", 12), width=30, show="*")
        self.entry_senha_registro.pack(pady=(0, 20))

        self.botao_registrar = tk.Button(
            frame_registro, text="Registrar", font=("Segoe UI", 12, "bold"),
            bg="#1abc9c", fg="#ffffff", command=self.registrar_usuario, relief="flat", width=20
        )
        self.botao_registrar.pack(pady=10)

        # Botão para ver todos os cargos
        self.botao_ver_cargos = tk.Button(
            frame_registro, text="Ver Todos os Cargos", font=("Segoe UI", 10),
            bg="#3498db", fg="#ffffff", command=self.mostrar_cargos, relief="flat", width=20
        )
        self.botao_ver_cargos.pack(pady=5)

        # Botão para voltar
        tk.Button(
            frame_registro, text="Voltar", font=("Segoe UI", 10),
            bg="#e74c3c", fg="#ffffff", command=self.criar_widgets_inicial, relief="flat", width=20
        ).pack(pady=5)

    def registrar_usuario(self):
        cargo_digitado = self.entry_cargo_registro.get().lower().strip()
        nome_usuario = self.entry_nome_registro.get().strip()
        senha_digitada = self.entry_senha_registro.get().strip()
        
        if not cargo_digitado or not nome_usuario or not senha_digitada:
            messagebox.showwarning("Entrada Inválida", "Por favor, preencha todos os campos.")
            return

        # Verifica se o cargo existe
        if cargo_digitado not in info_cargos:
            cargos_disponiveis = ", ".join(info_cargos.keys())
            messagebox.showerror(
                "Cargo não encontrado",
                f"O cargo '{cargo_digitado}' não foi encontrado.\n\nCargos disponíveis:\n{cargos_disponiveis}"
            )
            return

        # Verifica se o usuário já existe
        if cargo_digitado in self.usuarios_db:
            messagebox.showerror("Erro", "Este cargo já está registrado.")
            return

        # Registra o novo usuário
        self.usuarios_db[cargo_digitado] = {
            "nome_completo": nome_usuario,
            "senha": senha_digitada,
            "cargo": cargo_digitado
        }
        self.salvar_usuarios()
        
        messagebox.showinfo("Sucesso", "Usuário registrado com sucesso!")
        self.criar_widgets_login()

    def fazer_login(self):
        cargo_digitado = self.entry_cargo_login.get().lower().strip()
        senha_digitada = self.entry_senha_login.get().strip()
        
        if not cargo_digitado or not senha_digitada:
            messagebox.showwarning("Entrada Inválida", "Por favor, preencha todos os campos.")
            return

        # Verifica se o cargo existe
        if cargo_digitado not in info_cargos:
            cargos_disponiveis = ", ".join(info_cargos.keys())
            messagebox.showerror(
                "Cargo não encontrado",
                f"O cargo '{cargo_digitado}' não foi encontrado.\n\nCargos disponíveis:\n{cargos_disponiveis}"
            )
            return

        # Verifica senha
        if cargo_digitado not in self.usuarios_db:
            messagebox.showerror("Erro", "Usuário não registrado.")
            return
            
        if self.usuarios_db[cargo_digitado]["senha"] != senha_digitada:
            messagebox.showerror("Senha Incorreta", "Senha incorreta.")
            return
        
        self.usuario_logado = cargo_digitado
        self.usuario_atual = Usuario.from_dict(cargo_digitado, self.usuarios_db[cargo_digitado])
        self.iniciar_app()

    def mostrar_cargos(self):
        cargos_info = "\n".join([f"{cargo}: {info['descricao']}" for cargo, info in info_cargos.items()])
        messagebox.showinfo("Todos os Cargos", f"Cargos disponíveis:\n\n{cargos_info}")

    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def iniciar_app(self):
        self.limpar_tela()
        self.criar_widgets_principal()

    def criar_widgets_principal(self):
        # --- Frame do Título ---
        frame_titulo = tk.Frame(self.root, bg="#2c3e50")
        frame_titulo.pack(pady=10)
        
        # Mostra o dia da semana atual da simulação
        self.label_dia_semana = tk.Label(
            frame_titulo, text=f"Controle de Ponto - {DIAS_SEMANA_NOME[self.usuario_atual.data_atual.weekday()]}", font=("Segoe UI", 20, "bold"),
            bg="#2c3e50", fg="#ecf0f1"
        )
        self.label_dia_semana.pack()

        # Mostra a data completa
        self.label_data_completa = tk.Label(
            frame_titulo, text=f"Data: {self.usuario_atual.data_atual.strftime('%d/%m/%Y')}", font=("Segoe UI", 14),
            bg="#2c3e50", fg="#bdc3c7"
        )
        self.label_data_completa.pack()

        # --- Frame de Identificação ---
        frame_id = tk.LabelFrame(
            self.root, text="Identificação", font=("Segoe UI", 12),
            bg="#34495e", fg="#ecf0f1", padx=15, pady=15
        )
        frame_id.pack(pady=10, padx=20, fill="x")

        tk.Label(
            frame_id, text=f"Usuário: {self.usuario_atual.nome_completo}", font=("Segoe UI", 12),
            bg="#34495e", fg="#ecf0f1"
        ).pack(anchor="w")

        tk.Label(
            frame_id, text="Cargo:", font=("Segoe UI", 12),
            bg="#34495e", fg="#ecf0f1"
        ).pack(side="left", padx=5)

        self.entry_cargo = tk.Entry(frame_id, font=("Segoe UI", 12), width=25)
        self.entry_cargo.pack(side="left", padx=5, expand=True, fill="x")
        self.entry_cargo.insert(0, self.usuario_atual.cargo)

        self.botao_verificar = tk.Button(
            frame_id, text="Alterar Cargo", font=("Segoe UI", 12, "bold"),
            bg="#3498db", fg="#ffffff", command=self.alterar_cargo, relief="flat"
        )
        self.botao_verificar.pack(side="left", padx=10)

        # Botão para avançar o dia (movido para cá)
        self.botao_passar_dia = tk.Button(
            frame_id, text="Passar o Dia", font=("Segoe UI", 12, "bold"),
            bg="#1abc9c", fg="#ffffff", command=self.passar_dia_simulacao, relief="flat"
        )
        self.botao_passar_dia.pack(side="left", padx=10)

        # --- Frame de Status ---
        frame_status = tk.LabelFrame(
            self.root, text="Seu Status", font=("Segoe UI", 12),
            bg="#34495e", fg="#ecf0f1", padx=15, pady=15
        )
        frame_status.pack(pady=10, padx=20, fill="x")

        self.label_info_cargo = tk.Label(
            frame_status, text="Aguardando identificação...", font=("Segoe UI", 11),
            bg="#34495e", fg="#ecf0f1", justify="left", wraplength=500
        )
        self.label_info_cargo.pack(anchor="w")

        # --- Frame Financeiro ---
        frame_financeiro = tk.LabelFrame(
            self.root, text="Financeiro (Ciclo de 30 dias)", font=("Segoe UI", 12),
            bg="#34495e", fg="#ecf0f1", padx=15, pady=15
        )
        frame_financeiro.pack(pady=10, padx=20, fill="x")

        self.label_salario = tk.Label(
            frame_financeiro, text=f"Salário a Receber: R$ {self.usuario_atual.salario_acumulado:.2f}",
            font=("Segoe UI", 14, "bold"), bg="#34495e", fg="#2ecc71"
        )
        self.label_salario.pack(anchor="w", pady=5)

        self.label_dias_trabalhados = tk.Label(
            frame_financeiro, text=f"Dias trabalhados no ciclo: {30 - self.usuario_atual.dias_para_pagamento}",
            font=("Segoe UI", 12), bg="#34495e", fg="#ecf0f1"
        )
        self.label_dias_trabalhados.pack(anchor="w")

        self.label_dias_pagamento = tk.Label(
            frame_financeiro, text=f"Dias para o pagamento: {self.usuario_atual.dias_para_pagamento}",
            font=("Segoe UI", 12), bg="#34495e", fg="#ecf0f1"
        )
        self.label_dias_pagamento.pack(anchor="w")

        # Botão para ver todos os cargos
        self.botao_ver_cargos = tk.Button(
            frame_financeiro, text="Ver Todos os Cargos", font=("Segoe UI", 10),
            bg="#3498db", fg="#ffffff", command=self.mostrar_cargos, relief="flat"
        )
        self.botao_ver_cargos.pack(pady=5)

        # --- Frame de Ações e Clima ---
        frame_acoes = tk.LabelFrame(
            self.root, text="Ações e Clima", font=("Segoe UI", 12),
            bg="#34495e", fg="#ecf0f1", padx=15, pady=15
        )
        frame_acoes.pack(pady=10, padx=20, fill="x")

        self.label_clima = tk.Label(
            frame_acoes, text="Clima do dia...", font=("Segoe UI", 12),
            bg="#34495e", fg="#ecf0f1"
        )
        self.label_clima.pack(anchor="w", pady=(0, 10))

        # O botão foi removido daqui

        # Atualiza informações iniciais
        self.atualizar_info_cargo()
        self.atualizar_clima()

    def alterar_cargo(self):
        cargo_digitado = self.entry_cargo.get().lower().strip()
        if not cargo_digitado:
            messagebox.showwarning("Entrada Inválida", "Por favor, digite um cargo.")
            return

        if cargo_digitado in info_cargos:
            # Reinicia valores
            self.usuario_atual.salario_acumulado = 0.0
            self.usuario_atual.dias_para_pagamento = 30
            self.usuario_atual.cargo = cargo_digitado
            self.atualizar_info_cargo()
            self.atualizar_display_financeiro()
            messagebox.showinfo("Cargo Alterado", f"Seu cargo foi alterado para: {self.usuario_atual.cargo.upper()}")
        else:
            cargos_disponiveis = ", ".join(info_cargos.keys())
            messagebox.showerror(
                "Cargo não encontrado",
                f"O cargo '{cargo_digitado}' não foi encontrado.\n\nCargos disponíveis:\n{cargos_disponiveis}"
            )

    def atualizar_info_cargo(self):
        if self.usuario_atual.cargo:
            info = info_cargos[self.usuario_atual.cargo]
            self.label_info_cargo.config(text=f"Cargo: {self.usuario_atual.cargo.upper()}\n{info['descricao']}")

    def passar_dia_simulacao(self):
        if self.usuario_atual.dias_para_pagamento <= 0:
            messagebox.showinfo("Fim do Ciclo", f"O ciclo de 30 dias terminou!\nSalário final: R$ {self.usuario_atual.salario_acumulado:.2f}\nDias trabalhados: {30 - self.usuario_atual.dias_para_pagamento}")
            self.reiniciar_ciclo()
            return

        info = info_cargos[self.usuario_atual.cargo]
        dia_atual_simulado = self.usuario_atual.data_atual.weekday() # Usa weekday() da data
        
        # Verifica se é dia de trabalho
        if self.usuario_atual.cargo == "dono":
             messagebox.showinfo("Olá, Dono!", "Você não precisa bater ponto. Seu pagamento é garantido!")
             self.usuario_atual.salario_acumulado += info['salario_diario']
             self.atualizar_display_financeiro()
             self.avancar_dia()
             return

        if dia_atual_simulado in info["dias_trabalho"] or info["dias_trabalho"] == "flex":
            # Pergunta se vai trabalhar
            resposta = messagebox.askyesno(
                "Dia de Trabalho",
                "Hoje é seu dia de trabalho. Você vai trabalhar?"
            )
            if resposta:  # Sim
                self.usuario_atual.salario_acumulado += info['salario_diario']
                messagebox.showinfo("Bom Trabalho!", f"Ótimo trabalho! R$ {info['salario_diario']:.2f} foram adicionados ao seu salário.")
            else:  # Não
                self.lidar_com_ausencia()
        else:
            messagebox.showinfo("Dia de Folga", "Hoje não é seu dia de trabalho. Aproveite a folga!")

        self.atualizar_display_financeiro()
        self.avancar_dia()

    def avancar_dia(self):
        # Avança o dia da semana
        self.usuario_atual.data_atual += timedelta(days=1) # Avança um dia no calendário
        self.usuario_atual.dias_para_pagamento -= 1 # Decrementa os dias para o pagamento

        # Atualiza os labels na tela
        self.label_dia_semana.config(text=f"Controle de Ponto - {DIAS_SEMANA_NOME[self.usuario_atual.data_atual.weekday()]}")
        self.label_data_completa.config(text=f"Data: {self.usuario_atual.data_atual.strftime('%d/%m/%Y')}")
        self.atualizar_clima()

    def lidar_com_ausencia(self):
        motivo = simpledialog.askstring("Motivo da Ausência", "Por favor, informe o motivo da sua ausência:")
        salario_dia = info_cargos[self.usuario_atual.cargo]['salario_diario']

        if motivo:
            motivo_lower = motivo.lower().strip()
            # Verifica se o motivo contém alguma das palavras-chave
            justificado = any(keyword in motivo_lower for keyword in MOTIVOS_JUSTIFICADOS_KEYWORDS)
            
            if justificado:
                messagebox.showinfo(
                    "Ausência Justificada",
                    "Sua ausência foi registrada. Da próxima vez, avise com antecedência para evitar possíveis descontos."
                )
            else:
                # Pergunta se deseja descrever melhor
                resposta_descrever = messagebox.askyesno(
                    "Motivo Não Justificado",
                    "O motivo informado não parece justificável. Deseja descrever melhor o motivo?"
                )
                if resposta_descrever:
                    motivo_detalhado = simpledialog.askstring("Detalhe do Motivo", "Descreva brevemente o motivo:")
                    if motivo_detalhado:
                        motivo_detalhado_lower = motivo_detalhado.lower().strip()
                        justificado = any(keyword in motivo_detalhado_lower for keyword in MOTIVOS_JUSTIFICADOS_KEYWORDS)
                        if justificado:
                            messagebox.showinfo(
                                "Ausência Justificada",
                                "Sua ausência foi registrada. Da próxima vez, avise com antecedência para evitar possíveis descontos."
                            )
                        else:
                            self.usuario_atual.salario_acumulado -= salario_dia
                            messagebox.showerror(
                                "Falta Injustificada",
                                f"Motivo fútil. Um dia de salário (R$ {salario_dia:.2f}) foi descontado."
                            )
                    else:
                        self.usuario_atual.salario_acumulado -= salario_dia
                        messagebox.showerror(
                            "Falta Injustificada",
                            f"Motivo fútil. Um dia de salário (R$ {salario_dia:.2f}) foi descontado."
                        )
                else:
                    self.usuario_atual.salario_acumulado -= salario_dia
                    messagebox.showerror(
                        "Falta Injustificada",
                        f"Motivo fútil. Um dia de salário (R$ {salario_dia:.2f}) foi descontado."
                    )
        else:
            self.usuario_atual.salario_acumulado -= salario_dia
            messagebox.showerror(
                "Falta Injustificada",
                f"Motivo fútil. Um dia de salário (R$ {salario_dia:.2f}) foi descontado."
            )

    def atualizar_display_financeiro(self):
        self.label_salario.config(text=f"Salário a Receber: R$ {self.usuario_atual.salario_acumulado:.2f}")
        self.label_dias_trabalhados.config(text=f"Dias trabalhados no ciclo: {30 - self.usuario_atual.dias_para_pagamento}")
        self.label_dias_pagamento.config(text=f"Dias para o pagamento: {self.usuario_atual.dias_para_pagamento}")

    def reiniciar_ciclo(self):
        self.usuario_atual.salario_acumulado = 0.0
        self.usuario_atual.dias_para_pagamento = 30
        self.usuario_atual.cargo = None
        self.label_info_cargo.config(text="Aguardando identificação...")
        self.atualizar_display_financeiro()

    def atualizar_clima(self):
        # Simula o clima com base em uma lista pré-definida
        clima_simulado = random.choice(CLIMAS_POSSIVEIS)
        descricao_clima, tolerancia = clima_simulado
        self.usuario_atual.clima_atual = clima_simulado
        self.label_clima.config(text=f"Clima Simulado: {descricao_clima}\n{tolerancia}")

# --- Iniciar a Interface Gráfica ---
if __name__ == "__main__":
    root = tk.Tk()
    app = VerificadorApp(root)
    root.mainloop()
