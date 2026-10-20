import tkinter as tk
from tkinter import scrolledtext, messagebox
from groq import Groq

# Insira sua chave de API da Groq aqui
GROQ_API_KEY = ""

# Inicializa o cliente Groq
try:
    client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    client = None

# Prompt do Sistema Otimizado para o Carlão
SYSTEM_PROMPT = """
<system_instruction>
  <role>
    Você é Carlão, um produtor musical renomado, especialista na cultura Hip-Hop, com foco profundo nos subgêneros Rap, Trap e Boombap.
  </role>
  <tone_and_style>
    - Empático, atencioso, profissional e extrovertido.
    - Linguagem autêntica do meio musical urbano, mantendo o respeito e a clareza técnica.
  </tone_and_style>
  <core_competencies>
    1. Direção artística: Define o estilo, sonoridade e identidade de músicas ou álbuns.
    2. Acompanhamento de estúdio: Orienta MCs e músicos durante a gravação para extrair a melhor performance.
    3. Arranjo e beatmaking: Orienta sobre bases instrumentais, timbres, sintetizadores e batidas.
    4. Mixagem e masterização: Orienta sobre volumes, equalização e efeitos para nível profissional.
  </core_competencies>
  <boundaries>
    - Mantenha o equilíbrio: seja carismático e use gírias leves sem exagerar nas brincadeiras.
    - Nunca seja grosseiro; tenha empatia com as dificuldades dos artistas.
  </boundaries>
</system_instruction>
"""

class CarlãoStudioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Carlão Studio - Produtor Musical (Groq AI)")
        self.root.geometry("700x550")
        self.root.minsize(600, 450)
        
        # Configuração de Cores (Tema Estúdio / Dark)
        self.bg_color = "#1e1e1e"
        self.fg_color = "#ffffff"
        self.accent_color = "#ffb703"
        
        self.root.configure(bg=self.bg_color)
        
        # Histórico de conversas para manter o contexto
        self.chat_history = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
        
        self.create_widgets()

    def create_widgets(self):
        # Título
        title_label = tk.Label(
            self.root, 
            text="🎧 Carlão Beatmaker & Producer", 
            font=("Helvetica", 16, "bold"),
            bg=self.bg_color, 
            fg=self.accent_color
        )
        title_label.pack(pady=10)

        # Área de Chat (ScrolledText)
        self.chat_area = scrolledtext.ScrolledText(
            self.root, 
            wrap=tk.WORD, 
            font=("Arial", 11),
            bg="#2d2d2d", 
            fg=self.fg_color,
            insertbackground="white"
        )
        self.chat_area.pack(padx=15, pady=5, fill=tk.BOTH, expand=True)
        self.chat_area.config(state=tk.DISABLED)

        # Frame inferior para Entrada de Texto e Botão
        input_frame = tk.Frame(self.root, bg=self.bg_color)
        input_frame.pack(padx=15, pady=10, fill=tk.X)

        # Campo de Entrada
        self.entry_field = tk.Entry(
            input_frame, 
            font=("Arial", 12),
            bg="#3a3a3a", 
            fg=self.fg_color,
            insertbackground="white"
        )
        self.entry_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.entry_field.bind("<Return>", lambda event: self.send_message())

        # Botão Enviar
        send_button = tk.Button(
            input_frame, 
            text="Enviar", 
            font=("Arial", 11, "bold"),
            bg=self.accent_color, 
            fg="#000000",
            command=self.send_message,
            cursor="hand2"
        )
        send_button.pack(side=tk.RIGHT)
        
        # Mensagem inicial do bot na tela
        self.append_chat("Carlão", "E aí, meu mano! Carlão na voz. Qual é a boa pro som de hoje? Bora triturar esse beat ou acertar a lírica?")

    def append_chat(self, sender, message):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)

    def send_message(self):
        user_msg = self.entry_field.get().strip()
        if not user_msg:
            return
        
        if not GROQ_API_KEY or GROQ_API_KEY == "sua_chave_api_aqui":
            messagebox.showerror("Erro", "Por favor, insira uma chave de API válida da Groq no código.")
            return

        # Exibe a mensagem do usuário na interface
        self.append_chat("Você", user_msg)
        self.entry_field.delete(0, tk.END)

        # Adiciona ao histórico do chat
        self.chat_history.append({"role": "user", "content": user_msg})

        # Chamada à API da Groq em background/main thread
        try:
            resposta = client.chat.completions.create(
                model='openai/gpt-oss-120b',  # Mantido conforme o seu modelo de preferência
                messages=self.chat_history
            )
            
            bot_reply = resposta.choices[0].message.content
            
            # Adiciona a resposta do assistente ao histórico
            self.chat_history.append({"role": "assistant", "content": bot_reply})
            
            # Exibe a resposta na interface
            self.append_chat("Carlão", bot_reply)
            
        except Exception as e:
            messagebox.showerror("Erro na API", f"Ocorreu um erro ao comunicar com a Groq:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CarlãoStudioApp(root)
    root.mainloop()