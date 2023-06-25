import os

import nltk
from nltk.corpus import stopwords
from pyspark.ml.feature import Tokenizer, StopWordsRemover
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, col, trim


class WordCounter:
    def __init__(self, spark, folder_path):
        self.spark = spark
        self.folder_path = folder_path

    def count_words_in_file(self, file_path):
        # Download NLTK stop words
        # nltk.download('stopwords')
        stop_words = stopwords.words('portuguese')

        # Ler o arquivo TXT
        df = self.spark.read.text(file_path)

        # Tokenizar as palavras
        tokenizer = Tokenizer(inputCol='value', outputCol='words')
        words_data = tokenizer.transform(df)

        # Remover stop words usando o NLTK stop words
        remover = StopWordsRemover(inputCol='words', outputCol='filtered_words', stopWords=stop_words)
        words_filtered = remover.transform(words_data)

        # Explodir a coluna 'filtered_words' para criar uma linha para cada palavra
        words_exploded = words_filtered.select(explode(col('filtered_words')).alias('word'))

        # Filtrar palavras com base em uma lista
        words_to_filter = ["", "-", "url:", "artigo:", "r$", "this:", "e,", "pra", "tá", "vai"]  # Substitua com as palavras que deseja filtrar
        filtered_words = words_exploded.filter(~col('word').isin(words_to_filter))

        # Contar as palavras
        word_count = filtered_words.groupBy('word').count().sort('count', ascending=False)

        return word_count

    def count_words_in_folder(self):
        # Percorrer todos os arquivos na pasta
        for file_name in os.listdir(self.folder_path):
            if file_name.endswith('.txt'):
                file_path = os.path.join(self.folder_path, file_name)

                # Contar as palavras no arquivo
                word_count = self.count_words_in_file(file_path)

                print(f'Word counts in {file_name}:')
                word_count.show()
                word_count.toPandas().to_csv(f'../data/word_count_{file_name.replace(".txt", "")}.csv', index=False)


def main():
    # Inicializar a sessão Spark
    spark = SparkSession.builder.appName('WordCount').getOrCreate()

    # Pasta onde estão os arquivos CSV
    project_root = os.path.abspath(__file__).split('src')[0]
    folder_path = os.path.join(project_root, 'src', 'data')

    # Instanciar a classe WordCounter
    word_counter = WordCounter(spark, folder_path)

    # Contar as palavras nos arquivos
    word_counter.count_words_in_folder()

    # Parar a sessão Spark
    spark.stop()


if __name__ == '__main__':
    main()
