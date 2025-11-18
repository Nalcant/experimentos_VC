import cv2 as cv2
import os
import numpy as np
import fileManager as fm
class ImageProcessing:
    frameDir = fm.FileManager.PASTA_FRAMES
    
    def __init__(self):
        pass


    '''
     This method applies a grayscale filter to all images in the specified directory
     afterter converting to grayscale, it applies a bilateral filter to reduce noise while keeping edges sharp
    
    returns: boolean success flag, message

     '''
    def aplicar_filtros(self, diretorio):
        #acessa os arquivos da pasta de frames
        imagens = [f for f in os.listdir(diretorio) if f.endswith(".jpg")]
        print(len(imagens))
        if not imagens:
           #enviar mensagem de falta de imagens
            return False, "Não há imagens para aplicar o filtro."
        #aplica o filtro grayscale em cada imagem encontrada no diretório
        for img_nome in imagens:
            caminho_img = os.path.join(diretorio, img_nome) #caminho completo da imagem
            print("Caminho da imagem: {}".format(caminho_img))
            imagem = cv2.imread(caminho_img) #lê a imagem
            if(imagem is None):
                print(f"Erro ao ler a imagem: {caminho_img}")
                continue
            grImg = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY) #converte para grayscale
            biFilterImg = cv2.bilateralFilter(grImg,9,150,150) #imagem, diametro, intensidade, distancia
             #salva a imagem convertida, sobrescrevendo a original
            print("aplicando filtro bilateral e grayscale na imagem: {}".format(img_nome))
            print("Salvando imagem processada em: {}".format(os.path.join(fm.FileManager.PASTA_PRE_PROCESS, img_nome))) 
            output_path = os.path.join(fm.FileManager.PASTA_PRE_PROCESS, img_nome)
            cv2.imwrite(output_path, biFilterImg)

       # self.median_frame(diretorio)
        return True, "Filtro preto e branco aplicado com sucesso."
    
    '''
    this method calculates the median frame from all frames in the specified directory
    and saves it in the FRAME_MEDIANO directory
    it must be called after extracting frames
    and before calculating the masks for segmentation using median masking
    
    it saves the median frame as "frame_mediano.jpg" in the FRAME_MEDIANO directory
    returns: boolean success flag, message
    '''

    def median_frame(self, diretorio):
        imagens = [f for f in os.listdir(diretorio) if f.endswith(".jpg")]
        if not imagens:
            return False, "não há imagens para calcular o frame médio"
        frames = []
        indice = 0
        for  img_nome in imagens:
            if indice >= len(imagens):
                break
            caminho_img = os.path.join(diretorio, imagens[indice])
            print("Caminho da imagem no indice {} : {}".format(indice, caminho_img))
            frames.append(cv2.imread(caminho_img))
            indice += 30 #em caso de comparação entre os métodos, esse valor deve ser igual ao usado em diff_iterator
        median_frame = np.median(frames, axis=0).astype(dtype=np.uint8)
        fm.FileManager.criar_pasta(None, fm.FileManager.FRAME_MEDIANO)
        caminho = os.path.join(fm.FileManager.FRAME_MEDIANO, "frame_mediano.jpg")
        cv2.imwrite(caminho, median_frame)
        print("Total de frames:"+str(len(frames)))

    
    '''
    this method calculates the median mask for each frame in the specified directory
    using the median frame stored in diretorioFrameMediano


    
    '''
    def median_mask(self, diretorioFrames, diretorioFrameMediano):
        imagens = [f for f in os.listdir(diretorioFrames) if f.endswith(".jpg")]

    # Ordena para garantir sequência correta (frame_0001, frame_0002...)
        imagens.sort()
        
        if not imagens:
            return False, "não há imagens para calcular a máscara"

    # carrega o frame mediano
        caminho_frame_medio = os.path.join(diretorioFrameMediano, "frame_mediano.jpg")
        frame_medio = cv2.imread(caminho_frame_medio)

        if frame_medio is None:
            print(f"Erro ao ler a imagem do frame médio: {caminho_frame_medio}")
            return False, "erro ao ler a imagem do frame médio"

        # processa apenas a cada 30 frames
        for i, img in enumerate(imagens):

            # só processa a cada 30 frames
            if i % 30 != 0:
                continue

            caminho_img = os.path.join(diretorioFrames, img)
            frame = cv2.imread(caminho_img)

            if frame is None:
                print(f"Erro ao ler a imagem: {caminho_img}")
                return False, "erro ao ler a imagem do frame atual"

            if frame.shape != frame_medio.shape:
                print(f"Erro: Dimensões incompatíveis entre o frame atual e o frame médio para a imagem: {caminho_img}")
                return False, "dimensões incompatíveis entre o frame atual e o frame médio"

            # diferença absoluta entre o frame e o frame médio
            diferenca = cv2.absdiff(frame, frame_medio)

            # limiarização
            _, mascara = cv2.threshold(
                cv2.cvtColor(diferenca, cv2.COLOR_BGR2GRAY),
                30, 255,
                cv2.THRESH_BINARY
            )

            # salva a máscara
            caminho_mascara = os.path.join(
                fm.FileManager.PASTA_MEDIANO,
                f"mascara_mediana_{img}"
            )
            cv2.imwrite(caminho_mascara, mascara)
            print(f"Máscara salva em: {caminho_mascara}")

        return True, "máscaras calculadas com sucesso"
#median_mask(fm.FileManager.PASTA_FRAMES, os.path.join(fm.FileManager.FRAME_MEDIANO, "frame_mediano.jpg"))
    


    '''
    this method iterates through all frames in the specified directory
    and computes the frame difference between consecutive frames.
    It saves the resulting difference images in a new directory called "FrameDiff".
    '''
    def diff_iterator(self):
        preProcess = fm.FileManager.PASTA_PRE_PROCESS
        framePaths = [f for f in os.listdir(preProcess) if f.endswith(".jpg")] #lista de frames na pasta
        previousFrame = []
        currentFrame = []
        nextFrame = []
        if(not framePaths):
            return False, "não há imagens para realizar o frame diff"
        for i, currentPath in enumerate(framePaths):
        #ler imagem do frame atual
            print("Processando frame: {}".format(currentPath))
            print("Caminho completo: {}".format(os.path.join(preProcess, currentPath)))
            fullPath = os.path.join(self.frameDir, currentPath)
            currentFrame = cv2.imread(fullPath)
        # se não houver frame anterior, atribuir frameAtual ao anterior e seguir para a próxima iteração
            if  len(previousFrame) == 0:
                previousFrame = currentFrame
            else:
            # se houver posterior, ler posterior
                print(type(currentFrame))
                print(type(self.frameDir))
                if i+30 < len(framePaths):
                    fullPath = os.path.join(preProcess, framePaths[i+30])
                    nextFrame = cv2.imread(fullPath)
                else:
                    print("fim do frameDiff no frame: {}".format(fullPath))
                print(len(previousFrame))
                print(len(currentFrame))
                print(len(nextFrame))
                diffMask = self.frame_diff(previousFrame, currentFrame, nextFrame)
                threshold_value, diffMask = cv2.threshold(cv2.cvtColor(diffMask, cv2.COLOR_BGR2GRAY), 30, 255, cv2.THRESH_BINARY)
                caminho = os.path.join(fm.FileManager.PASTA_DIFF, f"diff_{currentPath}")
                cv2.imwrite(caminho, diffMask)
                previousFrame = currentFrame
                return True, "máscaras de diferença entre frames calculadas com sucesso"

    '''
     This method calculates the difference between three frames: previous, current, and 
     next. It computes the absolute difference between the current frame and both the previous
     and next frames, then combines these differences using a bitwise AND operation to highlight
     '''
    
    #diferenciar com o próximo e o anterior, gerar um frame basedo operação AND entre as duas diferenças
    def frame_diff(self,prev_frame, cur_frame, next_frame):
        diff_frames_1 = cv2.absdiff(next_frame, cur_frame)
        diff_frames_2 = cv2.absdiff(cur_frame, prev_frame)
        return cv2.bitwise_and(diff_frames_1, diff_frames_2) 
    
    '''
    what comes below is experimental code for other image processing techniques
    using single file methods (one frame)
    they can be adapted to iterate through folders later
    '''
    
    '''
    logical operations between images
    AND, OR, NOT, XOR'''

    '''
    In my test subjects, logical operation have not achieved 
    significant results, because the first method (median masking) have produced 
    to wide masks, in constrast with the  thin lines produced by the second method (frame difference).
    the results must be something close to images that nullify one of the entry methods
    or something that barely shows the differences between them.

    img1_path: path to first image (From a method, e.g., median masking
    img2_path: path to second image (From another method, e.g., frame difference
    returns: boolean success flag, message)
    saves the resulting images in the current directory
    '''

    def logical_operations(img1_path, img2_path):
        img1 = cv2.imread(img1_path)
        img2 = cv2.imread(img2_path)
        and_img = cv2.bitwise_and(img1, img2)
        or_img = cv2.bitwise_or(img1, img2)
        not_img1 = cv2.bitwise_not(img1)
        not_img2 = cv2.bitwise_not(img2)
        xor_img = cv2.bitwise_xor(img1, img2)
        cv2.imwrite("and_image.jpg", and_img)
        cv2.imwrite("or_image.jpg", or_img)
        cv2.imwrite("not_image1.jpg", not_img1)
        cv2.imwrite("not_image2.jpg", not_img2)
        cv2.imwrite("xor_image.jpg", xor_img)
        return True, "Operações lógicas aplicadas com sucesso."
    
    '''
    morphological operations: erosion and dilation
    '''

    '''
    this one actuallys workds well to refine masks
    specially dilation
    the application of erodion first results in nullified masks in frame difference method

    folder_path: path to the folder containing images to process
    operation: "erode" or "dilate"
    kernel_size: size of the structuring element
    returns: boolean success flag, message
    saves the resulting image in the current directory
    '''

<<<<<<< HEAD
    def iterarar_erosao(self, caminho):
        print("chamada iterar erosão")
        frames = [f for f in os.listdir(caminho) if f.endswith(".jpg")]
        for frame in frames:
            caminho_frame = os.path.join(caminho, frame)
            res, mensagem = self.erode_image(caminho_frame)
            if not res:
                return res, mensagem
        mensagem = "iterar dilatação concluída com sucesso!"
        return res, mensagem
=======
    def iterate_morphological_operation(folder_path, operation, kernel_size=5):
        imagens = [f for f in os.listdir(folder_path) if f.endswith(".jpg")]
        if not imagens:
            return False, "não há imagens para aplicar a operação morfológica"
        for img_nome in imagens:
            caminho_img = os.path.join(folder_path, img_nome)
            if operation == "erode":
                success, message = ImageProcessing.erode_image(caminho_img, kernel_size)
            elif operation == "dilate":
                success, message = ImageProcessing.dilate_image(caminho_img, kernel_size)
            else:
                return False, "Operação inválida. Use 'erode' ou 'dilate'."
            if not success:
                return False, f"Erro ao aplicar {operation} na imagem {img_nome}: {message}"
        return True, f"Operação {operation} aplicada com sucesso em todas as imagens."

>>>>>>> 2286cffc853a19df29e948139d5f548ca5a2f068
    
    def iterar_dilatar(self, caminho):
        print("chamada iterar dilatar")
        frames = [f for f in os.listdir(caminho) if f.endswith(".jpg")]
        for frame in frames:
            caminho_frame = os.path.join(caminho, frame)
            res, mensagem = self.dilate_image(caminho_frame)
            if not res:
                return res, mensagem
        
        mensagem = "iterar dilatação concluída com sucesso!"
        return res, mensagem
    
    def erode_image(self, img_path, kernel_size=5):
        frame = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        eroded_img = cv2.erode(frame, kernel, iterations=1)  
        print("erosao: "+ img_path)
        cv2.imwrite(img_path, eroded_img) #overites the original image
        return True, "Erosão aplicada com sucesso."
    
    def dilate_image(self, img_path, kernel_size=5):
        frame = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        dilated_img = cv2.dilate(frame, kernel, iterations=1)  
        print("dilatação: "+img_path)
        cv2.imwrite(img_path, dilated_img) #overites the original image
        return True, "Dilatação aplicada com sucesso."

    

    