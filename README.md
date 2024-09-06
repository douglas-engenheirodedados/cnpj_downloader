# CNPJ Downloader

Este script Python baixa dados de CNPJ do site da Receita Federal do Brasil.

## Requisitos

- Python 3.7+
- pip

## Instalação

1. Clone o repositório:
```
git clone https://github.com/seu-usuario/cnpj-downloader.git
cd cnpj-downloader
```

2. Instale as dependências:

```
pip install -r requirements.txt
```

## Uso

Execute o script principal:

```
python main.py
```


O script irá verificar se há novos dados disponíveis e baixá-los se necessário.

## Configuração

Edite o arquivo `config/settings.py` para ajustar as configurações, como o número de workers para download paralelo.

