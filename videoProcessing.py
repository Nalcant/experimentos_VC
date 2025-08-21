import cv2
import os

class videoProcessing():

    def __init__(self):
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
            