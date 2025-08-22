import cv2 as cv2
import os
import numpy as np

class imageProcessing:

    def __init__(self):
        pass

    def aplicar_filtro_pb(self, diretorio):
        imagens = [f for f in os.listdir(diretorio) if f.endswith(".jpg")]
        if not imagens:
           #enviar mensagem de falta de imagens
            return False, "Não há imagens para aplicar o filtro."
        for img_nome in imagens:
            caminho_img = os.path.join(diretorio, img_nome)
            imagem = cv2.imread(caminho_img)
            pb = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(caminho_img, pb)
            return True, "Filtro preto e branco aplicado com sucesso."
  
    def linear_medio(self, diretorio):
        imagens = [f for f in os.listdir(diretorio) if f.endswith(".jpg")]
        if not imagens:
            return False, "Não há imagens para aplicar o filtro."
        frames = []
        for img_nome in imagens:
           frames.append(cv2.imread(os.path.join(diretorio, img_nome)))
        frameMedio = np.median(frames, axis=0).astype(np.uint8)

        return True, "Filtro linear médio aplicado com sucesso."
