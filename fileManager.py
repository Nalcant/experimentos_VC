import os 
import shutil

class FileManager:

    '''beware of the folder structure when saving masks, each method saves to its own folder'''
    PASTA_FRAMES = "frames_extraidos"
    FRAME_MEDIANO = "frame_mediano"
    PASTA_PRE_PROCESS = "bilateral_gray"
    PASTA_MEDIANO= "mascaras_mediano"
    PASTA_DIFF= "mascaras_frameDiff"
    MAIN_FOLDERS = [PASTA_FRAMES, PASTA_PRE_PROCESS, PASTA_MEDIANO, PASTA_DIFF]
    ALL = [PASTA_FRAMES, FRAME_MEDIANO, PASTA_PRE_PROCESS, PASTA_DIFF, PASTA_MEDIANO]

    def __init__(self):
        self.restart()
   
    def restart(self):
        for pasta in self.ALL:
            self.criar_pasta(pasta)
        
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
            if os.path.exists(caminho) and self.verificar_arquivos(caminho):
                shutil.rmtree(caminho)
                print(f"Cache limpo: {caminho} apagado com sucesso.")
            elif not self.verificar_arquivos(caminho):
                print(f"O cache já está vazio em {caminho}")
            else: 
                print(f"Nenhuma pasta foi encontrada em {caminho}.")

    
    def iterar_limpar_cache(self):
        for pasta in self.ALL:
            self.limpar_cache(pasta)
        self.restart()


    
    #esse método deve ser chamado para tratar erros de caminho
    def verificar_diretorio(self,caminho):
        if not os.path.exists(caminho):
            #mudar tratativa do erro para retornar False
           self.criar_pasta_frames(caminho)
        return True
    
    def salvar_cache(self, caminho_origem, caminho_destino):
        try:
            if os.path.exists(caminho_origem):
                shutil.copytree(caminho_origem, caminho_destino, dirs_exist_ok=True)
                print(f"Cache salvo: Pasta copiada de '{caminho_origem}' para '{caminho_destino}' com sucesso.")
                return True
            else:
                print(f"Erro ao salvar cache: A pasta de origem '{caminho_origem}' não existe.")
                return False
        except Exception as e:
            print(f"Erro ao salvar o cache: {e}")
            return False
        
    def iterar_salvar_cache(self, caminho_destino_base, selected_folders):
        errors = []
        for pasta in selected_folders:
            caminho_destino = os.path.join(caminho_destino_base, pasta)
            if self.salvar_cache(pasta, caminho_destino):
                continue
            else:
                errors.append(pasta)
        if errors:
            return False, f"Erro ao salvar cache para as pastas: {', '.join(errors)}"
        return True, "Todas as pastas salvas com sucesso."
    
    def verificar_arquivos(self, caminho):
        if os.path.exists(caminho):
            arquivos = os.listdir(caminho)
            return len(arquivos) > 0 
        return False
    
         
    

