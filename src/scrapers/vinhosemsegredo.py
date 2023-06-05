from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from base_scraper import BaseScraper


class BlogPostScraper(BaseScraper):

    def __init__(self, base_url):
        self.base_url = base_url
        self.links = []
        self.contents = []
        self.driver = None

    def collect_post_links(self):
        self.driver.get(self.base_url)
        archives = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/ul/li[3]/ul")

        for element in archives.find_elements(By.TAG_NAME, "li"):
            href = element.find_element(By.TAG_NAME, 'a').get_attribute("href")
            self.links.append(href)

    def collect_post_contents(self):
        for link in self.links:
            self.driver.get(link)
            wait = WebDriverWait(self.driver, 10)
            post_content = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'entry')))
            self.contents.append(post_content.text)


# Uso da classe
scraper = BlogPostScraper("https://www.vinhosemsegredo.com/")
scraper.scrape()
scraper.save_contents_to_file('vinhosemsegredo.txt')