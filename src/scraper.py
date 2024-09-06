import requests
from bs4 import BeautifulSoup
import urllib.parse

def obter_pasta_mais_recente(url_base: str) -> str:
    """
    Obtém a URL da pasta mais recente a partir da URL base fornecida.

    Args:
        url_base (str): A URL base onde as pastas estão listadas.

    Returns:
        str: A URL completa da pasta mais recente.

    Raises:
        requests.RequestException: Se ocorrer um erro ao acessar a URL base.
    """
    resposta = requests.get(url_base)
    resposta.raise_for_status()
    soup = BeautifulSoup(resposta.content, 'html.parser')
    
    pastas = [link.get('href') for link in soup.find_all('a') if link.get('href').endswith('/')]
    pasta_mais_recente = sorted(pastas, reverse=True)[0]
    
    return urllib.parse.urljoin(url_base, pasta_mais_recente)

def listar_arquivos_na_pasta(url_pasta: str) -> list:
    """
    Lista todos os arquivos em uma pasta específica.

    Args:
        url_pasta (str): A URL da pasta a ser analisada.

    Returns:
        list: Uma lista com os nomes dos arquivos encontrados na pasta.

    Raises:
        requests.RequestException: Se ocorrer um erro ao acessar a URL da pasta.
    """
    resposta = requests.get(url_pasta)
    resposta.raise_for_status()
    soup = BeautifulSoup(resposta.content, 'html.parser')
    
    return [link.get('href') for link in soup.find_all('a') if not link.get('href').endswith('/')]
