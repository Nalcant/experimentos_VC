import os 
import shutil

class FileManager:
    PASTA_FRAMES = "frames_extraidos"

    def __init__(self):
        if not os.path.exists(self.PASTA_FRAMES):
            os.makedirs(self.PASTA_FRAMES)
            print(f"Pasta '{self.PASTA_FRAMES}' criada com sucesso.")

    def criar_pasta_frames(self):
        if not os.path.exists(self.PASTA_FRAMES):
            os.makedirs(self.PASTA_FRAMES)
            print(f"Pasta '{self.PASTA_FRAMES}' criada com sucesso.")
        else:
            print(f"A pasta '{self.PASTA_FRAMES}' já existe.")
            
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
            raise FileNotFoundError(f"O caminho '{caminho}' não existe.")
        return True
    
    def limpar_cache(self,caminho):
        #chamar verificar_diretorio antes de limpar o cache
        if os.path.exists(caminho):
            shutil.rmtree(caminho)
            #messagebox.showinfo("Cache limpo", "Pasta de frames apagada com sucesso.")
            return True
        else:
            return False
            #messagebox.showinfo("Cache limpo", "Nenhuma pasta de frames foi encontrada.")
        #atualizar_contador_frames()
    

