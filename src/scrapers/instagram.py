from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


class InstagramScraper:
    def __init__(self, username, password, profile, posts_to_scrape):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        self.username = username
        self.password = password
        self.profile = profile
        self.posts_to_scrape = posts_to_scrape
        self.contents = []

    def login(self):
        self.driver.get('https://www.instagram.com/accounts/login/')

        input_base_xpath = '/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/section/main/div/div/div[1]/div[' \
                           '2]/form/div/'

        # Wait for the login page to load

        self.wait.until(EC.presence_of_element_located((By.XPATH, input_base_xpath + 'div[1]/div/label/input')))

        user_input = self.driver.find_element(By.XPATH, input_base_xpath + 'div[1]/div/label/input')
        user_input.send_keys(self.username)

        pass_input = self.driver.find_element(By.XPATH, input_base_xpath + 'div[2]/div/label/input')
        pass_input.send_keys(self.password)

        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

        # Don't save login info
        login_info_xpath = '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/div/div'
        self.wait.until(EC.presence_of_element_located((By.XPATH, login_info_xpath)))
        self.driver.find_element(By.XPATH, login_info_xpath).click()

        # Don't turn on notifications
        notification_xpath = '/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]'
        self.wait.until(EC.presence_of_element_located((By.XPATH, notification_xpath)))
        self.driver.find_element(By.XPATH, notification_xpath).click()

    def scrape(self):
        self.driver.get(f'https://www.instagram.com/{self.profile}/')
        posts = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/div[3]/article/div[1]/div')))
        post_rows = posts.find_elements(By.TAG_NAME, 'div')
        post_links = []
        for row in post_rows:
            post_elements = row.find_elements(By.TAG_NAME, 'a')
            links = [elem.get_attribute('href') for elem in post_elements]
            post_links.extend(links)

        print(post_links)

        for link in post_links:
            self.driver.get(link)
            post = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
            print(post.text)
            self.contents.append(post.text)

    def quit(self):
        self.driver.quit()

    def save_contents_to_file(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(self.contents))


if __name__ == '__main__':
    username = "gutessitore"
    password = os.environ["INSTA_PASS"]
    profile = "cnnviagemegastronomia"
    posts_to_scrape = 10
    scraper = InstagramScraper(username, password, profile, posts_to_scrape)
    scraper.login()
    scraper.scrape()
    scraper.quit()
    scraper.save_contents_to_file(profile + '.txt')
