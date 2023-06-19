from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pickle

# Se não houver o chromedriver instalado ele irá instalar, caso já tenha ele encontrará o caminho
s = Service(ChromeDriverManager().install())
# Abrir a página web
driver = webdriver.Chrome(service=s)

#getting the cookies
url_blog = 'https://www.estadao.com.br/paladar/blog-da-belle/'
#accessing the page
driver.get(url_blog)
#waiting for the page to load and clicking on the button manually
time.sleep(20)
#save the cookies
pickle.dump(driver.get_cookies(), open("..\data\cookies_estadao.pkl", "wb"))
#close the browser
driver.quit()