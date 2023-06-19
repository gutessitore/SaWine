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
    # Contar a quantidade de parágrafos
    p_qtd = contar_paragrafos(div)
    # Criar uma variavel para armazenar os parágrafos para no final ter um texto só com todos os parágrafos
    texto = ''
    # Coletar os parágrafos
    for i in range(1,p_qtd):
        try:
            # Coletar o parágrafo
            paragrafo = driver.find_element(By.XPATH, div + f'/p[{i}]').text
            # Adicionar o paraágrafo na variável texto
            texto += paragrafo
        except:
            continue
    # Retornar a lista de textos
    return texto


# Função para calcular a quantidade de parágrafos
def contar_paragrafos(div):
    # Conta a quantidade de parágrafos dentro das divs através do método find element
    div_element = driver.find_element(By.XPATH, div)
    # Conte a quantidade de elementos de parágrafo dentro da div
    paragrafos = div_element.find_elements(By.CSS_SELECTOR, "p")
    paragrafos_qtd = len(paragrafos)
    # Retorna o número de parágrafos
    return paragrafos_qtd

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
def acessar_publicacoes(url, botao, div_xpath):
    # Acessar a página de publicações
    driver.get(url)
    # Esperar a pagina carregar
    time.sleep(5)
    # Carregar meus cookies com a função load_cookie
    load_cookies()
    # Clicar no botão "Carregar mais"
    carregar_mais(botao)
    # Acessar a div que contém as publicações
    div_element = driver.find_element(By.XPATH, div_xpath)
    # Coletar os links das publicações do blog
    links = div_element.find_elements(By.CSS_SELECTOR, "a")
    # Criar uma lista vazia para armazenar os links
    links_list = []
    # Coletar os links das publicações
    for link in links:
        links_list.append(link.get_attribute('href'))
    # Eliminando elementos duplicados
    links_list = list(set(links_list))
    # Retornar a lista de links
    return links_list

# Função para transformar o dicionário em dataframe
def dict_to_df(dict):
    df = pd.DataFrame.from_dict(dict, orient='index')
    df = df.reset_index()
    df = df.rename(columns={'index':'url', 0:'texto'})
    return df

# Função para rolar a página para baixo
def scroll_down():
    driver.execute_script("window.scrollBy(0, 500);")
    return

# Função para carregar os cookies
def load_cookies():
    # Carregar os cookies
    cookies = pickle.load(open("..\data\cookies.pkl", "rb"))
    # Adicionar os cookies ao navegador
    for cookie in cookies:
        driver.add_cookie(cookie)
    return

# Função geral para raspar o site
def raspagem(site, url, botao, div_xpath, div):
    # montando todo o script com minhas funções e salvando os textos
    links = acessar_publicacoes(url, botao, div_xpath)
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
url_blog = 'https://www.estadao.com.br/paladar/blog-da-belle/'
page_div_xpath = '//*[@id="content"]/div[1]'
blog_div_xpath = '//*[@id="fusion-app"]/div/div[1]/div/div/div/div[1]/div/div[2]/div/div[2]'
botao_xpath = '//*[@id="fusion-app"]/div/div[1]/div/div/div/div[1]/div/div[2]/div/div[3]/button'
cookies_xpath = '//*[@id="root"]/div/div/div/div[2]/button'
# Se não houver o chromedriver instalado ele irá instalar, caso já tenha ele encontrará o caminho
s = Service(ChromeDriverManager().install())
# Abrir a página web
driver = webdriver.Chrome(service=s)
# Raspagem do site
raspagem('blog_belle', url_blog, botao_xpath, blog_div_xpath, page_div_xpath)