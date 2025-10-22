from tkinter import Tk as tk
from tkinter import ttk
from tkinter import Button, Label, filedialog, messagebox, StringVar, Frame
from fileManager import FileManager as fm
from videoProcessing import videoProcessing as vp
from imageProcessing import imageProcessing as ip


class Window():

    '''
    Flags to control which operations are available based on previous steps
    in the processing pipeline

    selecionado = a frame can only be processed if a video is selected
    frames_extraidos = filters or cache clearing can only be applied if frames have been extracted
    pre_processado = segmentation can only be done after applying the black and white filter
    segmentado = post processing can only be done after segmentation

    Remember to manually update these flags back to false when manual testing
    '''
    #só é possível processar frames se o vídeo for selecionado
    selecionado = True
    #só é possível aplicar o filtros ou limpar cache se houver frames extraídos
    frames_extraidos= True

    #só é possível segmentar após aplicar o filtro preto e branco
    pre_processado = True
    
    # só é possível pós processar após segmentar
    segmentado = False



    def __init__(self):
        self.fileMng = fm()
        self.videoProcessing = vp()
        self.imageProcessing = ip()
        contador_var = 0
        self.root = tk()
        # Configurações da janela principal
        self.root.title("Processamento de vídeo") 
        self.root.geometry("700x350")
        self.root.resizable(False, False)
        self.root.update_idletasks()
        self.root.minsize(self.root.winfo_width(), self.root.winfo_height())
        self.video_path = StringVar()
        self.contador_var = StringVar()
        # Arrumar médotos do fileManager para usar constante PASTA_FRAMES
        self.atualizar_contador_frames(self.fileMng.contar_frames(self.fileMng.PASTA_FRAMES))
        Label(self.root, text="Ferramenta de Extração e Segmentação de Frames", font=("Arial", 12)).pack(pady=10)

        Button(self.root, text="Selecionar vídeo MP4", command=self.selecionar_video, width=30).pack()
        self.label_video_path = Label(self.root, text="Nenhum vídeo selecionado", wraplength=500)
        self.label_video_path.pack(pady=5)

        Button(self.root, text="Processar vídeo (Extrair Frames)", command= self.call_extrair_frames, width=30).pack(pady=5)
        
        # Frame horizontal para botão + contador
        self.filtro_frame = Frame(self.root)

        self.filtro_frame.pack(pady=5)

        Button(self.filtro_frame, text="Aplicar filtro grayscale + bilateral", command=self.call_aplicar_filtros, width=30).pack(pady=5)
        Label(self.filtro_frame, textvariable=contador_var, fg="blue", font=("Arial", 10, "bold"), padx=10).pack(pady=5)

        Button(self.filtro_frame, text="Máscara Mediana", command=self.call_aplicar_mascara_mediana, width=30).pack(side="left", pady=5)

        Button(self.filtro_frame, text="Máscara Diferença de Frames", command=self.call_mascara_diferenca_frames, width=30).pack(side="left", pady=5)

        Button(self.root, text="Limpar cache de frames", command=self.call_limpar_cache, width=30).pack(pady=5)
        self.root.mainloop()

    '''
    This method must be called after any file operation that involves add or remove frame files in system folders
    User save folders are an exception, as they are not monitored for changes
    It updates the frame counter in the GUI and the frames_extraidos flag
    '''
    def atualizar_contador_frames(self,contagem):
        self.contador_var.set(f"Frames extraídos: {contagem}")
        if(contagem>0):
            self.frames_extraidos = True

    def selecionar_video(self):
        caminho = filedialog.askopenfilename(
        title="Selecione um arquivo de vídeo",
        #.mp4.avi.mov.webm.ogg.mpeg.flv.wmv
        filetypes=[("Vídeo", ["*.mp4" , "*.mov", "*.avi", "*.webm", "*.ogg", "*.mpeg", "*.flv", "*.wmv", "*.MOV", "*.MP4", "*.AVI", "*.WEBM", "*.OGG", "*.MPEG", "*.FLV", "*.WMV"])]
    )
        
        if caminho:
            self.video_path.set(caminho)
            self.label_video_path.config(text=f"Selecionado: {caminho}")  
            self.selecionado = True     
    
    '''
     This method calls the videoProcessing to extract frames from the selected video
     It first checks if a video is selected and if the frames directory is accessible
     If successful, it updates the frame counter in the GUI
     '''

    def call_extrair_frames(self):
        if(self.selecionado == False):
            messagebox.showerror("Erro", "Nenhum vídeo selecionado. Selecione um vídeo primeiro.")
            return
        if self.fileMng.verificar_diretorio(self.video_path.get()):
            resultado, frame_count = self.videoProcessing.extrair_frames(self.fileMng.PASTA_FRAMES, self.video_path.get())
            if resultado:
                self.atualizar_contador_frames(frame_count)
                messagebox.showinfo("Concluído", f"{frame_count} frames salvos em '{fm.PASTA_FRAMES}'")
            if not resultado:
                messagebox.showerror("VideoProcessing.extrair_Frames return false", "Não foi possível processar o vídeo.")
        else:
            messagebox.showerror("fileMng.verificar_diretorio return false", "Não foi possível acessar ou criar a pasta de frames.")
    
    '''
    This method calls  clears the cache of extracted frames
    if user confirms, it calls the fileManager to save the cache
    if not, it just clears the cache
    If successful, it updates the frame counter in the GUI
    '''

    def call_limpar_cache(self):

        if self.fileMng.limpar_cache(self.fileMng.PASTA_FRAMES):
            self.atualizar_contador_frames(0)
            messagebox.showinfo("Cache limpo", "Pasta de frames apagada com sucesso.")
            self.pre_processado = False
            self.frames_extraidos = False 
            self.segmentado = False
        else:
            messagebox.showinfo("Cache limpo", "Nenhuma pasta de frames foi encontrada.")
   
    
    '''
    This method calls the imageProcessing to apply a black and white filter to the extracted frames
    It first checks if there are extracted frames and if the frames directory is accessible
    If successful, it shows a success message
    '''
    def call_aplicar_filtros(self):
        if(not self.frames_extraidos):
            messagebox.showerror("Erro", "Nenhum frame extraído. Extraia frames primeiro.")
            return
        if self.fileMng.verificar_diretorio(self.fileMng.PASTA_FRAMES):
            resultado, mensagem = self.imageProcessing.aplicar_filtros(self.fileMng.PASTA_FRAMES)
            if resultado:
                messagebox.showinfo("Filtro aplicado", mensagem)
                self.pre_processado = True
            else:
                messagebox.showerror("Erro ao aplicar filtro", mensagem)
        else:
            messagebox.showerror("fileMng.verificar_diretorio return false", "Não foi possível acessar ou criar a pasta de frames.")()
    
    def call_aplicar_mascara_mediana(self):
        self.imageProcessing.median_frame(self.fileMng.PASTA_FRAMES)
        if(not self.frames_extraidos):
            messagebox.showerror("Erro", "Nenhum frame extraído. Extraia frames primeiro.")
            return
        elif(not self.pre_processado):
            messagebox.showerror("Erro", "Frames não pré-processados. Aplique os filtros primeiro.")
            return
        if self.fileMng.verificar_diretorio(self.fileMng.PASTA_FRAMES):
            resultado, mensagem = self.imageProcessing.median_mask(self.fileMng.PASTA_FRAMES, self.fileMng.FRAME_MEDIANO)
            if resultado:
                messagebox.showinfo("Máscara aplicada", mensagem)
                self.segmentado = True
            else:
                messagebox.showerror("Erro ao aplicar máscara", mensagem)
        else:
            messagebox.showerror("fileMng.verificar_diretorio return false", "Não foi possível acessar ou criar a pasta de frames.")()

    def call_mascara_diferenca_frames(self):
        if(not self.frames_extraidos):
            messagebox.showerror("Erro", "Nenhum frame extraído. Extraia frames primeiro.")
            return
        if(not self.pre_processado):
            messagebox.showerror("Erro", "Frames não pré-processados. Aplique os filtros primeiro.")
            return
        if self.fileMng.verificar_diretorio(self.fileMng.PASTA_FRAMES):
            resultado, mensagem = self.imageProcessing.mascara_diferenca_frames(self.fileMng.PASTA_FRAMES)
            if resultado:
                messagebox.showinfo("Máscara aplicada", mensagem)
                self.segmentado = True
            else:
                messagebox.showerror("Erro ao aplicar máscara", mensagem)
        else:
            messagebox.showerror("fileMng.verificar_diretorio return false", "Não foi possível acessar ou criar a pasta de frames.")() 