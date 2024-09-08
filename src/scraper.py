import requests
from bs4 import BeautifulSoup
from config.settings import BASE_URL

def get_latest_folder():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    folders = [link.text.strip('/') for link in soup.find_all('a') if link.text.startswith('20')]
    latest_folder = max(folders)
    
    return latest_folder

def get_files_in_folder(folder):
    url = f"{BASE_URL}{folder}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    files = [link.text for link in soup.find_all('a') if link.text.endswith('.zip')]
    
    return files