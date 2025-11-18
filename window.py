from tkinter import Tk as tk
from tkinter import ttk
from tkinter import Button, Label, filedialog, messagebox, StringVar, Frame
from fileManager import FileManager as fm
from videoProcessing import videoProcessing as vp
from imageProcessing import ImageProcessing as ip
from tkinter import PhotoImage


class Window():
    ThumbNail = None
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
    selecionado = False
    #só é possível aplicar o filtros ou limpar cache se houver frames extraídos
    frames_extraidos= False

    #só é possível segmentar após aplicar o filtro preto e branco
    pre_processado = False
    
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
        self.root.geometry("1000x700")
        self.root.update_idletasks()
        self.root.wm_attributes("-topmost", True)
        self.video_path = StringVar()
        self.contador_var = StringVar()
        self.methods = ["Fundo mediano", "Diferença de Frames"]
        self.morpho = ["Dilatar", "Erodir"]
        self.folderChecks = {}

        #pre-process frame    
        self.TopFrame = Frame(self.root, width=950, height=300, bg="lightgray")
        self.image = PhotoImage(file="videoPlaceholder\\placeholder-video.png")
        self.image = self.image.subsample(2,2)

        self.ThumbLabel = Label(self.TopFrame, image= self.image, bg="lightgray")
        self.ThumbLabel.pack(pady=10, side="left", padx = "10")

        self.TopFrame.pack(side="top", pady=10, padx=10)
        self.TopFrame.pack_propagate(False)

        self.lbTopFrameTitle = Label(self.TopFrame, text="Pré-Processamento", font=("Arial", 16), bg= "lightgray")
        self.lbTopFrameTitle.pack(side = "top", pady= 10)
        self.bVideoSelect = Button(self.TopFrame, text="Selecionar vídeo", command=self.selecionar_video, width=30, )
        self.bVideoSelect.pack(side="top", padx= 10, pady= 10)

        
        
        self.label_video_path = Label(self.TopFrame, text="Nenhum vídeo selecionado", wraplength=500)
        self.label_video_path.pack(pady=5, side="top")

        self.bExtractFrames = Button(self.TopFrame, text="Extrair Frames", command=self.call_extrair_frames, width=30)
        self.bExtractFrames.pack(side="top", padx= 10, pady= 10)

        self.bApplyFilters = Button(self.TopFrame, text="Aplicar Filtros", command=self.call_aplicar_filtros, width=30)
        self.bApplyFilters.pack(side="top", padx= 10, pady= 10)

        ''' processamento frame  '''
        self.leftFrame = Frame(self.root, width=460, height=300, bg="lightgray")
        self.leftFrame.pack(side="left", pady=10, padx=25)
        self.leftFrame.pack_propagate(False)
        
        self.lbLftFrameTitle = Label(self.leftFrame, text="Processamento", font=("Arial", 16), bg= "lightgray")
        self.lbLftFrameTitle.pack(side="top", pady=10, padx=10)

        #radio buttons para escolher método de segmentação
        self.method_var = StringVar(value="Fundo mediano")

        for method in self.methods:
            radio_button = ttk.Radiobutton(self.leftFrame, text=method, variable=self.method_var, value=method)
            radio_button.pack(side="top", pady=5)

        #radio buttons para escolher operação morfológica
        self.morpho_var = StringVar(value="Dilatar")
        for operacao in self.morpho:
            radio_button = ttk.Radiobutton(self.leftFrame, text=operacao, variable=self.morpho_var, value=operacao)
            radio_button.pack(side="top", pady=5)

        self.leftFrameButtonProcess = Button(self.leftFrame, text="Aplicar método", command= self.call_aplicar_metodo, width=25)
        self.leftFrameButtonProcess.pack(side="left", pady=10, padx=20) 


        self.leftFrameButtonMorpho = Button(self.leftFrame, text="Operação morfológica", command= self.call_operacao_morfo, width=25)
        self.leftFrameButtonMorpho.pack(side="right", pady=10, padx=20)  
        
        """arquivos"""

        self.rightFrame = Frame(self.root, width=460, height=300, bg="lightgray")
        self.rightFrame.pack(side="right", pady=10, padx=25)
        self.rightFrame.pack_propagate(False)

        self.lbLftFrameTitle = Label(self.rightFrame, text="Arquivos", font=("Arial", 16), bg= "lightgray")
        self.lbLftFrameTitle.pack(side="top", pady=10, padx=10)

        #checkboxes para escolher quais pastas salvar
        for folder in self.fileMng.ALL:
            var = StringVar(value="0")
            chk = ttk.Checkbutton(self.rightFrame,text=folder,variable=var,
            onvalue="1",
            offvalue="0")
            chk = ttk.Checkbutton(self.rightFrame, text=folder, variable=var)
            chk.pack(side="top", pady=5)
            self.folderChecks[folder] = var 
        self.rightFrameButtonSaveCache = Button(self.rightFrame, text="Salvar Cache", command= self.call_salvar_cache, width=20)
        self.rightFrameButtonSaveCache.pack(side="top", pady=10)

        self.rightFrameButtonClearCache = Button(self.rightFrame, text="Limpar Cache", command= self.call_limpar_cache, width=20)
        self.rightFrameButtonClearCache.pack(side="top", pady=10)

        self.inicializar_flags()
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
        filetypes=[("Vídeo", ["*.mp4" , "*.mov", "*.avi",
                              "*.webm", "*.ogg", "*.mpeg", 
                              "*.flv", "*.wmv", "*.MOV", 
                              "*.MP4", "*.AVI", "*.WEBM",
                                "*.OGG", "*.MPEG", "*.FLV", "*.WMV"])])
        
        if caminho:
            self.video_path.set(caminho)
            self.label_video_path.config(text=f"Selecionado: {caminho}")  
            self.ThumbNail = PhotoImage(file=self.videoProcessing.get_firstFrame(caminho))
            self.ThumbLabel.config(image= self.ThumbNail)
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

   
   
    
    '''
    This method calls the imageProcessing to apply a black and white filter and bilateral filter to the extracted frames
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
    
<<<<<<< HEAD
    def call_applyMethod(self):
        if not self.pre_processado:
            messagebox.showerror("Não houve pré-processamento", "Aplique os filtros antes de executar um método de processamento")

=======
    def call_aplicar_metodo(self):
>>>>>>> 2286cffc853a19df29e948139d5f548ca5a2f068
        metodo = self.method_var.get()
        if(metodo == "Fundo mediano"):
            self.call_mascara_mediana()
        elif(metodo == "Diferença de Frames"):
            self.call_mascara_diferenca_frames()
        else:
            print("metodo não especificado")

<<<<<<< HEAD
    def call_morphoOperation(self):
        
        if not self.segmentado:
            messagebox.showerror("Não houve processamento", "Nenhum método foi utilizado para que possa ser pós-processado")
        
        metodo = self.method_var.get()
        print(metodo)
        
        if not self.fileMng.verificar_arquivos(metodo):
            messagebox.showerror("Arquivos inexistentes", f"O método {metodo} ainda não foi processado")    
            return
=======
    def call_operacao_morfo(self):
        operacao = self.morpho_var.get()
        if(operacao == "Dilatação"):
            self.call_dilatar_mascara()
        elif(operacao == "Erosão"):
            self.call_erosao_mascara()
>>>>>>> 2286cffc853a19df29e948139d5f548ca5a2f068

        operacao = self.morpho_var.get()
        print(operacao)
        
        if(operacao == "Dilatar"):
            self.call_dilatar_mascara(metodo)
        elif(operacao == "Erodir"):
            self.call_erosao_mascara(metodo)
        else:
            print("operação não especificada")

    def call_mascara_mediana(self):
        #primeiro é feito a modelagem do frame mediano
        self.imageProcessing.median_frame(self.fileMng.PASTA_FRAMES)
        if(not self.frames_extraidos):
            messagebox.showerror("Erro", "Nenhum frame extraído. Extraia frames primeiro.")
            return
        elif(not self.pre_processado):
            messagebox.showerror("Erro", "Frames não pré-processados. Aplique os filtros primeiro.")
            return
        if self.fileMng.verificar_diretorio(self.fileMng.PASTA_PRE_PROCESS):
            resultado, mensagem = self.imageProcessing.median_mask(self.fileMng.PASTA_PRE_PROCESS, self.fileMng.FRAME_MEDIANO)
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
        if self.fileMng.verificar_diretorio(self.fileMng.PASTA_PRE_PROCESS):
            resultado, mensagem = self.imageProcessing.diff_iterator()
            if resultado:
                messagebox.showinfo("Máscara aplicada", mensagem)
                self.segmentado = True
            else:
                messagebox.showerror("Erro ao aplicar máscara", mensagem)
        else:
            messagebox.showerror("fileMng.verificar_diretorio return false", "Não foi possível acessar ou criar a pasta de frames.")() 
            
        
     
        
    def call_dilatar_mascara(self, metodo):   
        print("chamada call dilatar") 
        if(metodo == "Fundo mediano"):
            folder = self.fileMng.PASTA_MEDIANO
        elif(metodo == "Diferença de Frames"):
            folder = self.fileMng.PASTA_DIFF
        resultado, mensagem = self.imageProcessing.iterar_dilatar(folder)
        if resultado:
            messagebox.showinfo("Dilatação aplicada", mensagem)
        else:
            messagebox.showerror("Erro ao aplicar dilatação", mensagem)       
    def call_erosao_mascara(self, metodo):
        print("chamada call erosao")        
        if(metodo == "Fundo mediano"):
            folder = self.fileMng.PASTA_MEDIANO
        elif(metodo == "Diferença de Frames"):
            folder = self.fileMng.PASTA_DIFF
        
        resultado, mensagem = self.imageProcessing.iterarar_erosao(folder)
        if resultado:
            messagebox.showinfo("Erosão aplicada", mensagem)
        else:
            messagebox.showerror("Erro ao aplicar erosão", mensagem)


    def call_limpar_cache(self):

        self.fileMng.iterar_limpar_cache()
        messagebox.showinfo("Cache limpo", "Pasta de frames apagada com sucesso.")
        self.inicializar_flags()
        

    def call_salvar_cache(self):
        pasta_destino = filedialog.askdirectory(title="Selecione a pasta de destino para salvar o cache")
        
        if not pasta_destino:
            return
        res, mensagem = self.fileMng.iterar_salvar_cache(pasta_destino, [folder for folder, var in self.folderChecks.items() if var.get() == "1"])

        if  res:           
            messagebox.showinfo("Cache salvo", f"Pastas salvas com sucesso em '{pasta_destino}'.")
        else:
            messagebox.showerror("Erro", mensagem)

    def inicializar_flags(self):

        for arquivos in self.fileMng.MAIN_FOLDERS:
            if self.fileMng.verificar_arquivos(arquivos):
                if arquivos == self.fileMng.PASTA_FRAMES:
                    self.frames_extraidos = True
                    print("frames extraidos set to TRUE")
                else:
                    self.frames_extraidos = False
                    print("frames extraidos set to FALSE")                    
                if arquivos == self.fileMng.PASTA_PRE_PROCESS:
                    self.pre_processado = True
                    print("pre processado set to TRUE")
                else:
                    print("pre processado set to FALSE")
                if arquivos in [self.fileMng.PASTA_MEDIANO, self.fileMng.PASTA_DIFF]:
                    self.segmentado = True
                    print("segmentado set to TRUE")
                else:
                    print("segmentado set to FALSE")