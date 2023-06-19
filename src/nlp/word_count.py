from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer, StopWordsRemover
from pyspark.sql.functions import concat_ws, explode, col
import nltk
from nltk.corpus import stopwords
import os


class WordCounter:
    def __init__(self, spark, folder_path):
        self.spark = spark
        self.folder_path = folder_path

    def count_words_in_file(self, file_path):
        # Download NLTK stop words
        nltk.download('stopwords')
        stop_words = stopwords.words('portuguese')

        # Ler o arquivo CSV
        df = self.spark.read.format('csv').option('header', 'true').load(file_path)

        # Converter todas as colunas em uma única coluna
        df = df.withColumn('doc', concat_ws(' ', *df.columns))

        # Tokenizar as palavras
        tokenizer = Tokenizer(inputCol='doc', outputCol='words')
        words_data = tokenizer.transform(df)

        # Remover stop words usando o NLTK stop words
        remover = StopWordsRemover(inputCol='words', outputCol='filtered_words', stopWords=stop_words)
        words_filtered = remover.transform(words_data)

        # Contar as palavras
        word_count = words_filtered.withColumn('word', explode(col('filtered_words'))) \
            .groupBy('word') \
            .count() \
            .sort('count', ascending=False)

        return word_count

    def count_words_in_folder(self):
        # Percorrer todos os arquivos na pasta
        for file_name in os.listdir(self.folder_path):
            if file_name.endswith('.csv'):
                file_path = os.path.join(self.folder_path, file_name)

                # Contar as palavras no arquivo
                word_count = self.count_words_in_file(file_path)

                print(f'Word counts in {file_name}:')
                word_count.show()


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
