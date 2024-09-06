import os

def criar_pasta_local(caminho: str) -> None:
    """
    Cria uma pasta local se ela não existir.

    Args:
        caminho (str): O caminho da pasta a ser criada.

    Returns:
        None
    """
    os.makedirs(caminho, exist_ok=True)

def construir_caminho_local(pasta_base: str, nome_arquivo: str) -> str:
    """
    Constrói o caminho local completo para um arquivo.

    Args:
        pasta_base (str): O caminho da pasta base.
        nome_arquivo (str): O nome do arquivo.

    Returns:
        str: O caminho completo do arquivo.
    """
    return os.path.join(pasta_base, nome_arquivo)
