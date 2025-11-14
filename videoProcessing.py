import cv2
import os
from fileManager import FileManager

class videoProcessing():

    def __init__(self):
        self.fm = FileManager()
        pass

    def extrair_frames(self, pasta_frames, caminho_video):
            framePointer = cv2.VideoCapture(caminho_video)
            if not framePointer.isOpened():
                #messagebox.showerror("Erro", "Não foi possível abrir o vídeo.")
                return [False, 0]

            frame_count = 0
            while True:
                ret, frame = framePointer.read()
                if not ret:
                    break
                caminho_frame = os.path.join(pasta_frames, f"frame_{frame_count:04d}.jpg")
                cv2.imwrite(caminho_frame, frame)
                frame_count += 1

            framePointer.release()
           # atualizar_contador_frames() 
           # messagebox.showinfo("Concluído", f"{frame_count} frames salvos em '{PASTA_FRAMES}'")
            return [True, frame_count]
    
    def get_firstFrame(self, caminho_video):
        framePointer = cv2.VideoCapture(caminho_video)
        ret, frame = framePointer.read()

        if not ret:
            print("Não foi possível pegar o primeiro frame")
            return
        else:
             self.fm.criar_pasta("thumbnail")
             caminho_thumbNail = os.path.join("thumbnail", "thumbnail.png")
             frame = cv2.resize(frame, (400, 250))
             cv2.imwrite(caminho_thumbNail, frame)
             return caminho_thumbNail

         