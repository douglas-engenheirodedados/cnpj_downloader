from src.scraper import get_latest_folder, get_files_in_folder
from src.downloader import download_and_upload_files
import traceback
import logging

logging.basicConfig(filename='logs/cnpj_downloader.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    try:
        print("Iniciando o processo de download e upload dos dados CNPJ")
        logging.info("Iniciando o processo de download e upload dos dados CNPJ")
        
        latest_folder = get_latest_folder()
        print(f"Pasta mais recente identificada: {latest_folder}")
        logging.info(f"Pasta mais recente identificada: {latest_folder}")
        
        files = get_files_in_folder(latest_folder)
        print(f"Arquivos encontrados: {len(files)}")
        logging.info(f"Arquivos encontrados: {len(files)}")
        
        print("Iniciando o download e upload dos arquivos...")
        logging.info("Iniciando o download e upload dos arquivos...")
        download_and_upload_files(latest_folder, files)
        
        print("Processo concluído com sucesso")
        logging.info("Processo concluído com sucesso")
    except Exception as e:
        print(f"Ocorreu um erro durante a execução: {str(e)}")
        logging.error(f"Ocorreu um erro durante a execução: {str(e)}")
        print("Detalhes do erro:")
        logging.error("Detalhes do erro:")
        print(traceback.format_exc())
        logging.error(traceback.format_exc())

if __name__ == "__main__":
    main()