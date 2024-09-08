import os
import shutil
import requests
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from azure.storage.blob import BlobServiceClient
from config.settings import BASE_URL, DOWNLOAD_DIR, AZURE_CONNECTION_STRING, AZURE_CONTAINER_NAME

# Configuração do logging
logging.basicConfig(filename='logs/cnpj_downloader.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def clear_download_directory():
    if os.path.exists(DOWNLOAD_DIR):
        shutil.rmtree(DOWNLOAD_DIR)
    os.makedirs(DOWNLOAD_DIR)
    logging.info(f"Pasta de download limpa: {DOWNLOAD_DIR}")
    print(f"Pasta de download limpa: {DOWNLOAD_DIR}")

def download_file(url, filename, folder):
    new_filename = f"{folder}_{filename}"
    filepath = os.path.join(DOWNLOAD_DIR, new_filename)
    
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(filepath, 'wb') as file, tqdm(
        desc=new_filename,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as progress_bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            progress_bar.update(size)
    
    logging.info(f"Arquivo baixado: {new_filename}")
    print(f"Arquivo baixado: {new_filename}")
    return new_filename

def upload_to_azure(local_file_path, blob_name):
    if not AZURE_CONNECTION_STRING:
        logging.error("AZURE_CONNECTION_STRING não está definida.")
        print("Erro: AZURE_CONNECTION_STRING não está definida.")
        return False
    if not AZURE_CONTAINER_NAME:
        logging.error("AZURE_CONTAINER_NAME não está definido.")
        print("Erro: AZURE_CONTAINER_NAME não está definido.")
        return False

    try:
        logging.info(f"Tentando fazer upload do arquivo: {blob_name}")
        print(f"Iniciando upload do arquivo: {blob_name}")
        
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)
        
        with open(local_file_path, "rb") as data:
            container_client.upload_blob(name=blob_name, data=data, overwrite=True)
        
        logging.info(f"Arquivo enviado para o Azure: {blob_name}")
        print(f"Arquivo enviado para o Azure: {blob_name}")
        return True
    except Exception as e:
        logging.error(f"Erro ao fazer upload do arquivo {blob_name}: {str(e)}")
        logging.error(f"Tipo de exceção: {type(e).__name__}")
        print(f"Erro ao fazer upload do arquivo {blob_name}: {str(e)}")
        return False

def remove_local_file(file_path):
    try:
        os.remove(file_path)
        logging.info(f"Arquivo local removido: {file_path}")
        print(f"Arquivo local removido: {file_path}")
    except Exception as e:
        logging.error(f"Erro ao remover arquivo local {file_path}: {str(e)}")
        print(f"Erro ao remover arquivo local {file_path}: {str(e)}")

def download_and_upload_files(folder, files):
    logging.info(f"Iniciando processo para a pasta: {folder}")
    print(f"Iniciando processo para a pasta: {folder}")
    clear_download_directory()
    
    urls = [f"{BASE_URL}{folder}/{file}" for file in files]
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        download_futures = [executor.submit(download_file, url, file, folder) for url, file in zip(urls, files)]
        
        for future in as_completed(download_futures):
            filename = future.result()
            local_file_path = os.path.join(DOWNLOAD_DIR, filename)
            if upload_to_azure(local_file_path, filename):
                remove_local_file(local_file_path)

    logging.info("Download, upload e limpeza concluídos!")
    print("Download, upload e limpeza concluídos!")