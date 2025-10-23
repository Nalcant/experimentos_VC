import os 
import shutil

class FileManager:
    PASTA_FRAMES = "frames_extraidos"
    FRAME_MEDIANO = "frame_mediano"
    PASTA_PRE_PROCESS = "gauss_Gray"
    PASTA_DIFF= "mascaras_FrameDiff"
    ALL = [PASTA_FRAMES, FRAME_MEDIANO, PASTA_PRE_PROCESS, PASTA_DIFF]

    def __init__(self):
           self.criar_pasta(self.PASTA_FRAMES)

    def criar_pasta(self, diretorio):
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)
            print(f"Pasta '{diretorio}' criada com sucesso.")
        #else:
            #print(f"A pasta '{diretorio}' já existe.")
            
    def contar_frames(self, caminho):
        if os.path.exists(caminho):
            return len([f for f in os.listdir(FileManager.PASTA_FRAMES) if f.endswith(".jpg")])
        return 0

    def limpar_cache(self, caminho):
        if os.path.exists(caminho):
            shutil.rmtree(caminho)
            print("Cache limpo: Pasta de frames apagada com sucesso.")
        else:
            print("Cache limpo: Nenhuma pasta de frames foi encontrada.")
        return FileManager.contar_frames()
    
    #esse método deve ser chamado para tratar erros de caminho
    def verificar_diretorio(self,caminho):
        if not os.path.exists(caminho):
            #mudar tratativa do erro para retornar False
           self.criar_pasta_frames(caminho)
        return True
    
    def salvar_pasta(caminho_origem, caminho_destino):
        try:
            if not os.path.exists(caminho_destino):
                shutil.copytree(caminho_origem, caminho_destino)
                print(f"Pasta copiada de '{caminho_origem}' para '{caminho_destino}' com sucesso.")
            else:
                print(f"A pasta de destino '{caminho_destino}' já existe.")
        except Exception as e:
            print(f"Erro ao copiar a pasta: {e}")
         
    

