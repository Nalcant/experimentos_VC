import cv2
import os
import shutil
from tkinter import Tk, Button, Label, filedialog, messagebox, StringVar, Frame

PASTA_FRAMES = "frames_extraidos"

def atualizar_contador_frames():
    if os.path.exists(PASTA_FRAMES):
        total = len([f for f in os.listdir(PASTA_FRAMES) if f.endswith(".jpg")])
    else:
        total = 0
    contador_var.set(f"Frames disponíveis: {total}")

def limpar_cache():
    if os.path.exists(PASTA_FRAMES):
        shutil.rmtree(PASTA_FRAMES)
        messagebox.showinfo("Cache limpo", "Pasta de frames apagada com sucesso.")
    else:
        messagebox.showinfo("Cache limpo", "Nenhuma pasta de frames foi encontrada.")
    atualizar_contador_frames()

def selecionar_video():
    caminho = filedialog.askopenfilename(
        title="Selecione um arquivo de vídeo",
        #.mp4.avi.mov.webm.ogg.mpeg.flv.wmv
        filetypes=[("MP4", "*.mp4"), ("MOV", "*.mov", ), ("AVI", "*.avi"), ("WEBM", "*.webm"), ("OGG", "*.ogg"), ("MPEG", "*.mpeg"), ("FLV", "*.flv"), ("WMV", "*.wmv")]
    )
    if caminho:
        video_path.set(caminho)
        label_video_path.config(text=f"Selecionado: {caminho}")

def extrair_frames():
    caminho_video = video_path.get()
    if not caminho_video or not os.path.exists(caminho_video):
        messagebox.showerror("Erro", "Selecione um vídeo válido antes de processar.")
        return

    os.makedirs(PASTA_FRAMES, exist_ok=True)

    cap = cv2.VideoCapture(caminho_video)
    if not cap.isOpened():
        messagebox.showerror("Erro", "Não foi possível abrir o vídeo.")
        return

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        caminho_frame = os.path.join(PASTA_FRAMES, f"frame_{frame_count:04d}.jpg")
        cv2.imwrite(caminho_frame, frame)
        frame_count += 1

    cap.release()
    atualizar_contador_frames()
    messagebox.showinfo("Concluído", f"{frame_count} frames salvos em '{PASTA_FRAMES}'")

def aplicar_filtro_pb():

    if not os.path.exists(PASTA_FRAMES): # Verifica se a pasta existe
        messagebox.showerror("Erro", "Nenhum frame encontrado. Extraia primeiro.")
        return

    imagens = [f for f in os.listdir(PASTA_FRAMES) if f.endswith(".jpg")] # Lista os arquivos de imagem na pasta
    if not imagens:
        messagebox.showinfo("Aviso", "Não há imagens para aplicar o filtro.")
        return

    for img_nome in imagens:
        caminho_img = os.path.join(PASTA_FRAMES, img_nome)
        imagem = cv2.imread(caminho_img)
        pb = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(caminho_img, pb)

    messagebox.showinfo("Filtro aplicado", "Filtro preto e branco aplicado com sucesso.")

def main():
    global video_path, label_video_path, contador_var
    root = Tk()
    # Configurações da janela principal
    root.title("Extrator de Frames MP4") 
    root.geometry("550x280")
    root.resizable(False, False)

    video_path = StringVar()
    contador_var = StringVar()
    atualizar_contador_frames()

    Label(root, text="Ferramenta de Extração de Frames", font=("Arial", 12)).pack(pady=10)

    Button(root, text="Selecionar vídeo MP4", command=selecionar_video, width=30).pack()
    label_video_path = Label(root, text="Nenhum vídeo selecionado", wraplength=500)
    label_video_path.pack(pady=5)

    Button(root, text="Processar vídeo (Extrair Frames)", command=extrair_frames, width=30).pack(pady=5)

    # Frame horizontal para botão + contador
    filtro_frame = Frame(root)
    filtro_frame.pack(pady=5)

    Button(filtro_frame, text="Aplicar filtro preto e branco", command=aplicar_filtro_pb, width=30).pack(side="left")
    Label(filtro_frame, textvariable=contador_var, fg="blue", font=("Arial", 10, "bold"), padx=10).pack(side="left")

    Button(root, text="Limpar cache de frames", command=limpar_cache, width=30).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
