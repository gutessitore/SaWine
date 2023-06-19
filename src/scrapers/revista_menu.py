# Importando as libs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd
import pickle

# Função para coletar os textos dos sites
def pegar_texto(url, div):
    # Atualiza a página com o site indicado
    driver.get(url)
    # Espera a página carregar
    time.sleep(5)
    # Acessar cada p da div e coletar o texto
    div_element = driver.find_element(By.XPATH, div)
    # Acessar todos os elementos de parágrafo dentro da div
    paragrafos = div_element.find_elements(By.CSS_SELECTOR, "p")
    # armazenar todos os textos de um link juntos para não ficar um texto por coluna
    texto = ""
    # Coletar os textos e retornar um dict com os links e os textos (que são os parágrafos juntos)
    for paragrafo in paragrafos:
        try:
            texto += paragrafo.text
        except:
            continue
    texto = texto.replace("\n", ". ")
    return texto

# Função para carregar mais publicações do blog
def carregar_mais(xpath):
    # Clicar no botão 5 vezes usando uma variável de controle
    controle = 0
    while controle < 5:
        # Clicar no botão "Carregar mais"
        botao = driver.find_element(By.XPATH, xpath)
        botao.click()
        # Esperar a página carregar
        time.sleep(5)
        # Atualizar o controle
        controle += 1
    return

# Função para acessar as publicações do blog
def acessar_publicacoes(url, div_xpath,  botao = None, cookies_name = None):
    # Acessar a página de publicações
    driver.get(url)
    # Esperar a pagina carregar
    time.sleep(5)
    # Carregar meus cookies com a função load_cookie
    if cookies_name != None:
        load_cookies(cookies_name)
    else:
        pass
    # Clicar no botão "Carregar mais"
    if botao != None:
        carregar_mais(botao)
    else:
        pass
    # Acessar a div que contém as publicações
    div_element = driver.find_element(By.XPATH, div_xpath)
    # Acessar todas as figures da div e pegar o link da publicação para não ter links duplicados
    figures = div_element.find_elements(By.CSS_SELECTOR, "figure")
    # Criar uma lista para armazenar os links
    links_list = []
    # Coletar os links
    for figure in figures:
        try:
            link = figure.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            links_list.append(link)
        except:
            continue
    # Eliminando elementos duplicados
    links_list = list(set(links_list))
    # Retornar a lista de links
    return links_list
# Função para transformar o dicionário em dataframe
def dict_to_df(dict):
    # Transformando o dicionário em dataframe
    df = pd.DataFrame.from_dict(dict, orient='index')
    df.reset_index(inplace=True)
    df.columns = ["url", "texto"]
    return df

# Função para rolar a página para baixo
def scroll_down():
    driver.execute_script("window.scrollBy(0, 500);")
    return

# Função para carregar os cookies
def load_cookies(cookies_name):
    # Carregar os cookies
    cookies = pickle.load(open(f"..\data\{cookies_name}.pkl", "rb"))
    # Adicionar os cookies ao navegador
    for cookie in cookies:
        driver.add_cookie(cookie)
        time.sleep(2)
    return

# Função geral para raspar o site
def raspagem(site, url, div_xpath, div, botao = None, cookies_name = None):
    # montando todo o script com minhas funções e salvando os textos
    links = acessar_publicacoes(url, div_xpath, botao, cookies_name)
    # Criar um dicionário para armazenar os links e os textos
    dict = {}
    for link in links:
        dict.update({link: pegar_texto(link, div)})
    driver.quit()
    # Transformando a lista em dataframe
    df = dict_to_df(dict)
    # Salvando o dataframe em um arquivo csv
    df.to_csv(f"..\data\{site}.csv", index=False)
    return df

# Definindo as variáveis e abrindo a página
url_blog = 'https://revistamenu.com.br/ultimas/'
page_div_xpath = '/html/body'
blog_div_xpath = '//*[@id="site"]/div/section/div'
# Iniciando o driver
s = Service(ChromeDriverManager().install())
# Abrir a página web
driver = webdriver.Chrome(service=s)
# Raspagem do site
raspagem('revista', url_blog, blog_div_xpath, page_div_xpath)