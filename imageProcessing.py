import cv2 as cv2
import os
import numpy as np

class imageProcessing:

    def __init__(self):
        pass

    def aplicar_filtro_pb(self, diretorio):
        #acessa os arquivos da pasta de frames
        imagens = [f for f in os.listdir(diretorio) if f.endswith(".jpg")]
        print(len(imagens))
        if not imagens:
           #enviar mensagem de falta de imagens
            return False, "Não há imagens para aplicar o filtro."
        #aplica o filtro preto e branco em cada imagem encontrada no diretório
        for img_nome in imagens:
            caminho_img = os.path.join(diretorio, img_nome) #caminho completo da imagem
            imagem = cv2.imread(caminho_img) #lê a imagem
            pbImg = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY) #converte para preto e branco
            biFilterImg = cv2.bilateralFilter(pbImg,9,75,75) #imagem, diametro, intensidade, distancia
             #salva a imagem convertida, sobrescrevendo a original
            cv2.imwrite(caminho_img, biFilterImg)

        self.median_frame(diretorio)
        return True, "Filtro preto e branco aplicado com sucesso."
    
  
    def median_frame(self, diretorio):
        #acessa os arquivos da pasta de frames 
        imagens = [f for f in os.listdir(diretorio) if f.endswith(".jpg")]
        if not imagens:
            return False, "não há imagens para calcular o frame médio"
        frames = []
        indice = 0
        #atribui a cada indice frames um frame para o cálculo do frame mediano
        for  img_nome in imagens:
            if indice >= len(imagens):
                break
            caminho_img = os.path.join(diretorio, imagens[indice])
            print("Caminho da imagem no indice {} : {}".format(indice, caminho_img))
            frames.append(cv2.imread(caminho_img))
            indice += 100 # distancia de frames pode resultar em resultados diferentes
        print("Total de frames:"+str(len(frames)))