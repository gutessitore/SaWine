from abc import abstractmethod
from selenium import webdriver
from contextlib import closing


class BaseScraper:
    contents = []

    @abstractmethod
    def collect_post_links(self):
        ...

    @abstractmethod
    def collect_post_contents(self):
        ...

    def save_contents_to_file(self, filename):
        # save file on project root / src / data
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(self.contents))

    def scrape(self):
        with closing(webdriver.Chrome()) as self.driver:
            self.collect_post_links()
            self.collect_post_contents()
