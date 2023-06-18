from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import re
import pandas as pd
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from openpyxl import Workbook

# Definir o caminho para o ChromeDriver
chrome_driver_path = r'C:\Users\pedro\OneDrive\Documentos\ChromeDriver\chromedriver.exe'

# Definir as opções do ChromeDriver
chrome_options = Options()
#chrome_options.add_argument("--headless")

# Configurar o serviço do ChromeDriver
service = Service(chrome_driver_path)

# Inicializar o driver do Selenium
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://www.vivino.com/explore?e=eJzLLbI11rNQy83MszU1UMtNrLA1MjBQS660dQpSSwYSPmoFtoZq6Wm2ZYlFmakliTlq-UUptmr5SZW2auXF0bG2xgCWghSP"

nome_arquivo = "extracao_vivino_amarone_italiano.xlsx"

def WebScrapingVivino(url):
    # Abrir o site no navegador
    driver.get(url, nome_arquivo)

    # Aguardar a página carregar
    driver.implicitly_wait(5)

    contador_principal = 1
    contador_secundario = 1

    df_extracao_vinhos = pd.DataFrame(columns=['Nome Vinho', 'Localidade', 'Harmoniza', 'Avaliação'])

    while True:
        seletor_wine_cards = f'//*[@id="explore-page-app"]/div/div/div[2]/div[2]/div[1]/div[{contador_principal}]/div/a'
        try: 
            if driver.find_element(By.XPATH,seletor_wine_cards):
                # Obter o URL do link
                element = driver.find_element(By.XPATH,seletor_wine_cards)
                link_url = element.get_property("href")
                driver.execute_script("window.scrollBy(0, 400);")
                seletor_nome_vinho = f'//*[@id="explore-page-app"]/div/div/div[2]/div[2]/div[1]/div[{contador_principal}]/div/a/div/div[2]/div/div[1]'
                seletor_localidade = f'//*[@id="explore-page-app"]/div/div/div[2]/div[2]/div[1]/div[{contador_principal}]/div/a/div/div[2]/div/div[2]'
                nome_vinho = driver.find_element(By.XPATH,seletor_nome_vinho).text
                nome_vinho = re.sub(r'\n', ' ', nome_vinho)
                localidade = driver.find_element(By.XPATH,seletor_localidade).text
                localidade = re.sub(r'\n', ' ', localidade)
                # Executar o código JavaScript para abrir o link em uma nova guia
                driver.execute_script(f"window.open('{link_url}', '_blank');")
                # Alternar para a nova aba aberta
                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(1)
                lista_harmonizacao = []
                # Obter a altura total da página
                total_height = driver.execute_script("return document.body.scrollHeight")
                # Definir a posição de destino como metade da altura total
                target_position = total_height / 2
                # Executar o código JavaScript para rolar até a posição de destino
                driver.execute_script(f"window.scrollTo(0, {target_position});")
                proximo_vinho = False

                while True:
                    if proximo_vinho == False:
                        seletor_prato_nome_tipo1 = f'//*[@id="wine-page-lower-section"]/div[2]/div/div[7]/div/div[3]/div/a[{contador_secundario}]/div[2]'
                        seletor_prato_nome_tipo2 = f'//*[@id="wine-page-lower-section"]/div[1]/div/div[3]/div/div[3]/div/a[{contador_secundario}]/div[2]'
                        try:
                            try:
                                pratos = driver.find_element(By.XPATH, seletor_prato_nome_tipo1)
                            except:
                                pratos = driver.find_element(By.XPATH, seletor_prato_nome_tipo2)
                            lista_harmonizacao.append(pratos.text)
                            contador_secundario = contador_secundario + 1
                        except:
                            seletor_botao_mostrar_avaliacao = '//*[@id="all_reviews"]/div[2]/div[1]/button'
                            string_harmonizacao = ', '.join(lista_harmonizacao)
                            botao_mostrar_avaliacao = driver.find_element(By.XPATH, seletor_botao_mostrar_avaliacao)
                            botao_mostrar_avaliacao.click()
                            contador_avaliação = 1
                            time.sleep(1)

                            while True:
                                seletor_avaliação = f'//*[@id="baseModal"]/div/div[2]/div[3]/div[{contador_avaliação}]/div/div[1]/div[1]/a/span[2]'
                                try:
                                    driver.switch_to.window(driver.window_handles[1])
                                    driver.execute_script("window.scrollBy(0, 500);")
                                    avaliação = driver.find_element(By.XPATH,seletor_avaliação).text
                                    lista_vinhos = pd.DataFrame({'Nome Vinho': [nome_vinho], 'Localidade': [localidade], 'Harmoniza': [string_harmonizacao], 'Avaliação': [avaliação]})
                                    df_extracao_vinhos = pd.concat([df_extracao_vinhos, lista_vinhos], ignore_index=True)
                                    contador_avaliação = contador_avaliação + 1

                                except:
                                    driver.close()
                                    driver.switch_to.window(driver.window_handles[0])
                                    contador_secundario = 1
                                    contador_principal = contador_principal + 1
                                    proximo_vinho = True
                                    break
            
                    else:
                        break
        except: 
            df_extracao_vinhos.to_excel(nome_arquivo, index=False)
            break
