# CNPJ Data Downloader e Uploader

Este projeto baixa os dados abertos da Receita Federal do Brasil, que estão em formato .zip, descompacta-os em .csv e faz o upload para um Azure Data Lake Storage.

## Funcionalidades

- Identifica automaticamente a pasta mais recente de dados disponíveis
- Baixa todos os arquivos .zip da pasta mais recente
- Faz upload dos arquivos para o Azure Blob Storage
- Remove os arquivos locais após o upload bem-sucedido
- Registra logs detalhados do processo

## Requisitos

- Python 3.7+
- Bibliotecas Python (veja `requirements.txt`)
- Conta no Azure com um Blob Storage configurado

## Configuração

1. Clone o repositório:
   ```
   git clone https://github.com/douglas-engenheirodedados/cnpj_downloader
   cd seu-repositorio
   ```

2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

3. Configure as variáveis de ambiente no arquivo `.env`:
   ```
   AZURE_CONNECTION_STRING=sua_connection_string_aqui
   AZURE_CONTAINER_NAME=nome_do_seu_container
   DOWNLOAD_DIR=data/downloads
   ```

## Uso

Execute o script principal:

```
python main.py
```


O script irá verificar se há novos dados disponíveis e baixá-los se necessário.

## Configuração

Edite o arquivo `config/settings.py` para ajustar as configurações, como o número de workers para download paralelo.

## Logs

Os logs do processo são salvos em `logs/cnpj_downloader.log`. Verifique este arquivo para obter informações detalhadas sobre cada execução.

## Estrutura do Projeto
projeto_cnpj/
│
├── config/
│ └── settings.py
├── src/
│ ├── init.py
│ ├── scraper.py
│ └── downloader.py
├── logs/
│ └── cnpj_downloader.log
├── main.py
├── requirements.txt
└── README.md

## Contribuição

Contribuições são bem-vindas! Por favor, abra uma issue para discutir mudanças importantes antes de fazer um pull request.

