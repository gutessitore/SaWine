import json
import string
from collections import Counter

import nltk
from nltk.corpus import stopwords
from tqdm import tqdm

nltk.download('stopwords')


class TextProcessor:
    def __init__(self, filepath, process=None, language='portuguese'):
        self.filepath = filepath
        self.language = language
        self.stopwords = stopwords.words(self.language)
        self.process = process or self._process()

    def _process(self):
        with open(self.filepath, encoding='utf-8') as file:
            text = file.read()
        text = text.lower()

        # Remove punctuation
        translator = str.maketrans('', '', string.punctuation)
        text = text.translate(translator)

        word_list = text.split()

        # Remove stopwords
        word_list = [word for word in word_list if word not in self.stopwords]

        return word_list

    def word_frequencies(self):
        word_list = self.process
        return Counter(word_list)

    def sorted_word_frequencies(self):
        word_count = self.word_frequencies()
        return dict(sorted(word_count.items(), key=lambda item: item[1], reverse=True))

    def print_word_frequencies(self):
        word_count = self.sorted_word_frequencies()
        print(json.dumps(word_count, indent=4, ensure_ascii=False))

    def find_next_word(self, word, n=1):
        word_list = self.process
        next_words = []
        for i in range(len(word_list) - n):
            if word_list[i] == word:
                next_words.append(word_list[i + n])
        return next_words


class SubProcessor(TextProcessor):
    def __init__(self, filepath, word, n=1, language='portuguese'):
        super().__init__(filepath, language=language)
        self.word = word
        self.n = n
        self.process = self.find_next_word(self.word, self.n)

    def get_word_frequencies(self):
        word_count = self.sorted_word_frequencies()
        return {self.word: word_count}


# Usage:
processor = TextProcessor('../../../../../SaWine/src/scrapers/blogdosvinhos.txt')
processor_result = processor.sorted_word_frequencies()


results = {}

search_words = [
    'vinho', 'carne', 'peixe', 'frango', 'massa', 'queijo', 'sobremesa', 'fruta',
    'salada', 'churrasco', 'pizza', 'hamburguer', 'risoto'
]

for word in tqdm(processor_result.keys()):
    sub_processor = SubProcessor('../../../../../SaWine/src/scrapers/blogdosvinhos.txt', word)
    results.update(sub_processor.get_word_frequencies())

print(json.dumps(results, indent=4, ensure_ascii=False))
