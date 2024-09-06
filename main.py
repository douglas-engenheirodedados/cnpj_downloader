import os
import logging
import shutil
from src.scraper import obter_pasta_mais_recente, listar_arquivos_na_pasta
from src.downloader import baixar_arquivo, baixar_arquivos_em_paralelo
from config.settings import URL_BASE, NUM_WORKERS

# Configuração do logging
log_dir = '/home/gittil/Documents/workspace/cnpj/logs'
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename=os.path.join(log_dir, 'cnpj_downloader.log'))

def verificar_e_preparar_download(url_base):
    pasta_mais_recente = obter_pasta_mais_recente(url_base)
    nome_pasta_atual = pasta_mais_recente.split('/')[-2]
    
    diretorio_downloads = 'data/downloads'
    os.makedirs(diretorio_downloads, exist_ok=True)
    pastas_existentes = [d for d in os.listdir(diretorio_downloads) if os.path.isdir(os.path.join(diretorio_downloads, d))]
    
    if pastas_existentes:
        ultima_pasta_local = max(pastas_existentes)
        
        if ultima_pasta_local == nome_pasta_atual:
            logging.info(f"Dados já estão atualizados (pasta {nome_pasta_atual}). Nenhum download necessário.")
            return False
        else:
            logging.info(f"Nova pasta disponível: {nome_pasta_atual}. Removendo pasta antiga: {ultima_pasta_local}")
            shutil.rmtree(os.path.join(diretorio_downloads, ultima_pasta_local))
    else:
        logging.info(f"Nenhuma pasta de download existente. Iniciando download para {nome_pasta_atual}.")
    
    return True

def verificar_arquivos_existentes(pasta_destino, arquivos):
    arquivos_existentes = []
    for arquivo in arquivos:
        caminho_arquivo = os.path.join(pasta_destino, arquivo)
        if os.path.exists(caminho_arquivo):
            arquivos_existentes.append(arquivo)
    return arquivos_existentes

def main():
    url_base = URL_BASE
    
    if verificar_e_preparar_download(url_base):
        pasta_mais_recente = obter_pasta_mais_recente(url_base)
        arquivos = listar_arquivos_na_pasta(pasta_mais_recente)
        
        pasta_destino = os.path.join('data', 'downloads', pasta_mais_recente.split('/')[-2])
        os.makedirs(pasta_destino, exist_ok=True)
        
        arquivos_existentes = verificar_arquivos_existentes(pasta_destino, arquivos)
        
        if arquivos_existentes:
            logging.info(f"Os seguintes arquivos já existem e não serão baixados novamente:")
            for arquivo in arquivos_existentes:
                logging.info(f"- {arquivo}")
            
            arquivos_para_download = [a for a in arquivos if a not in arquivos_existentes]
        else:
            arquivos_para_download = arquivos
        
        if not arquivos_para_download:
            logging.info("Todos os arquivos já existem. Nenhum download necessário.")
        else:
            logging.info(f"Iniciando o download de {len(arquivos_para_download)} arquivos.")
            tarefas = [(pasta_mais_recente + arquivo, os.path.join(pasta_destino, arquivo)) 
                       for arquivo in arquivos_para_download]
            baixar_arquivos_em_paralelo(tarefas, NUM_WORKERS)
    else:
        logging.info("Nenhuma ação necessária. Encerrando o programa.")

if __name__ == "__main__":
    main()
