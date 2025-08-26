from tkinter import Tk as tk
from tkinter import ttk
from tkinter import Button, Label, filedialog, messagebox, StringVar, Frame
from fileManager import FileManager as fm
from videoProcessing import videoProcessing as vp
from imageProcessing import imageProcessing as ip


class Window():
    
    def __init__(self):
        self.fileMng = fm()
        self.videoProcessing = vp()
        self.imageProcessing = ip()
        contador_var = 0
        self.root = tk()
        # Configurações da janela principal
        self.root.title("Processamento de vídeo") 
        self.root.geometry("550x280")
        self.root.resizable(False, False)
        self.video_path = StringVar()
        self.contador_var = StringVar()
        # Arrumar médotos do fileManager para usar constante PASTA_FRAMES
        self.atualizar_contador_frames(self.fileMng.contar_frames(self.fileMng.PASTA_FRAMES))
        Label(self.root, text="Ferramenta de Extração de Frames", font=("Arial", 12)).pack(pady=10)

        Button(self.root, text="Selecionar vídeo MP4", command=self.selecionar_video, width=30).pack()
        self.label_video_path = Label(self.root, text="Nenhum vídeo selecionado", wraplength=500)
        self.label_video_path.pack(pady=5)

        Button(self.root, text="Processar vídeo (Extrair Frames)", command= self.call_extrair_frames, width=30).pack(pady=5)

        # Frame horizontal para botão + contador
        self.filtro_frame = Frame(self.root)
        self.filtro_frame.pack(pady=5)

        Button(self.filtro_frame, text="Aplicar filtro preto e branco", command=self.call_aplicar_filtro_pb, width=30).pack(side="left")
        Label(self.filtro_frame, textvariable=contador_var, fg="blue", font=("Arial", 10, "bold"), padx=10).pack(side="left")
        Button(self.root, text="Limpar cache de frames", command=self.call_limpar_cache, width=30).pack(pady=5)
        self.root.mainloop()

    def atualizar_contador_frames(self,contagem):
        self.contador_var.set(f"Frames extraídos: {contagem}")

    def selecionar_video(self):
        caminho = filedialog.askopenfilename(
        title="Selecione um arquivo de vídeo",
        #.mp4.avi.mov.webm.ogg.mpeg.flv.wmv
        filetypes=[("Vídeo", ["*.mp4" , "*.mov", "*.avi", "*.webm", "*.ogg", "*.mpeg", "*.flv", "*.wmv", "*.MOV", "*.MP4", "*.AVI", "*.WEBM", "*.OGG", "*.MPEG", "*.FLV", "*.WMV"])]
    )
        if caminho:
            self.video_path.set(caminho)
            self.label_video_path.config(text=f"Selecionado: {caminho}")       
    
    def call_extrair_frames(self):
        if self.fileMng.verificar_diretorio(self.video_path.get()):
            resultado, frame_count = self.videoProcessing.extrair_frames(self.fileMng.PASTA_FRAMES, self.video_path.get())
            if resultado:
                self.atualizar_contador_frames(frame_count)
                messagebox.showinfo("Concluído", f"{frame_count} frames salvos em '{fm.PASTA_FRAMES}'")
            if not resultado:
                messagebox.showerror("VideoProcessing.extrair_Frames return false", "Não foi possível processar o vídeo.")
        else:
            messagebox.showerror("fileMng.verificar_diretorio return false", "Não foi possível acessar ou criar a pasta de frames.")
    
    def call_limpar_cache(self):
        if self.fileMng.limpar_cache(self.fileMng.PASTA_FRAMES):
            self.atualizar_contador_frames(0)
            messagebox.showinfo("Cache limpo", "Pasta de frames apagada com sucesso.")
        else:
            messagebox.showinfo("Cache limpo", "Nenhuma pasta de frames foi encontrada.")
   
    def call_aplicar_filtro_pb(self):
        if self.fileMng.verificar_diretorio(self.fileMng.PASTA_FRAMES):
            resultado, mensagem = self.imageProcessing.aplicar_filtro_pb(self.fileMng.PASTA_FRAMES)
            if resultado:
                messagebox.showinfo("Filtro aplicado", mensagem)
            else:
                messagebox.showerror("Erro ao aplicar filtro", mensagem)
        else:
            messagebox.showerror("fileMng.verificar_diretorio return false", "Não foi possível acessar ou criar a pasta de frames.")()