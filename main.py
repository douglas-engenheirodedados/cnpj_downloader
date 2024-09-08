from src.scraper import get_latest_folder, get_files_in_folder
from src.downloader import download_and_upload_files
import traceback
import logging

logging.basicConfig(filename='logs/cnpj_downloader.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    try:
        logging.info("Iniciando o processo de download e upload dos dados CNPJ")
        
        latest_folder = get_latest_folder()
        logging.info(f"Pasta mais recente identificada: {latest_folder}")
        
        files = get_files_in_folder(latest_folder)
        logging.info(f"Arquivos encontrados: {len(files)}")
        
        logging.info("Iniciando o download e upload dos arquivos...")
        download_and_upload_files(latest_folder, files)
        
        logging.info("Processo concluído com sucesso")
    except Exception as e:
        logging.error(f"Ocorreu um erro durante a execução: {str(e)}")
        logging.error("Detalhes do erro:")
        logging.error(traceback.format_exc())

if __name__ == "__main__":
    main()