from abc import abstractmethod
from selenium import webdriver
from contextlib import closing
import os


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
        project_root = os.path.abspath(__file__).split('src')[0]
        filename = os.path.join(project_root, 'src', 'data', filename)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(self.contents))

    def scrape(self):
        with closing(webdriver.Chrome()) as self.driver:
            self.collect_post_links()
            self.collect_post_contents()
