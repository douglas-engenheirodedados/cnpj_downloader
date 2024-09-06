import requests
import os
from tqdm import tqdm
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

def baixar_arquivo(url: str, caminho_local: str) -> str:
    """
    Baixa um arquivo de uma URL específica e o salva localmente.

    Args:
        url (str): A URL do arquivo a ser baixado.
        caminho_local (str): O caminho local onde o arquivo será salvo.

    Returns:
        str: Uma mensagem indicando o sucesso ou falha do download.

    Raises:
        requests.RequestException: Se ocorrer um erro durante o download.
    """
    tamanho_existente = os.path.getsize(caminho_local) if os.path.exists(caminho_local) else 0
    headers = {'Range': f'bytes={tamanho_existente}-'}
    
    try:
        resposta = requests.get(url, headers=headers, stream=True)
        resposta.raise_for_status()
        
        tamanho_total = int(resposta.headers.get('content-length', 0)) + tamanho_existente
        modo = 'ab' if tamanho_existente > 0 else 'wb'
        
        with open(caminho_local, modo) as f:
            for chunk in resposta.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return f"Arquivo {os.path.basename(caminho_local)} baixado com sucesso."
    except requests.RequestException as e:
        return f"Erro ao baixar {os.path.basename(caminho_local)}: {str(e)}"

def baixar_arquivos_em_paralelo(tarefas: list, num_workers: int) -> None:
    """
    Baixa múltiplos arquivos em paralelo usando um pool de threads.

    Args:
        tarefas (list): Uma lista de tuplas (url, caminho_local) para cada arquivo a ser baixado.
        num_workers (int): O número máximo de threads a serem usadas para downloads paralelos.

    Returns:
        None
    """
    sucessos = 0
    falhas = 0
    
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futuros = [executor.submit(baixar_arquivo, url, caminho) for url, caminho in tarefas]
        
        for futuro in tqdm(as_completed(futuros), total=len(futuros), desc="Progresso total", unit="arquivo"):
            resultado = futuro.result()
            if "sucesso" in resultado.lower():
                sucessos += 1
            else:
                falhas += 1
            logging.info(resultado)

    logging.info(f"Download concluído. Sucessos: {sucessos}, Falhas: {falhas}")
