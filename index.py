from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import json
import os


class Index:
    def __init__(self, path):
        self.stopwords = set(stopwords.words('english'))
        self.index = {}
        self.current_file = []
        self.files = []
        self.load_files(path)

    def run(self):
        for f in self.files:
            self.read_file(f)
            self.parse_docs()
        with open('test.json', 'w') as f:
            json.dump(self.index, f)

    def load_files(self, path):
        for file in os.listdir(path):
            self.files.append(path + file)

    def read_file(self, file) -> list:

        with open(file, 'r') as f:
            d = json.load(f)

        self.current_file = d

    def parse_docs(self):
        if not self.current_file:
            return

        for doc in self.current_file:
            self.parse_doc(doc)

    def parse_doc(self, doc: dict) -> None:
        # stopwords
        doc_id = list(doc.keys())[0]
        text = doc[doc_id]
        stopped = self.stop_words(text)
        for w in stopped:
            if w not in self.index:
                self.index[w] = 0

            self.index[w] += 1

    def stop_words(self, text: str) -> list:
        filtered = list()
        text = word_tokenize(text)
        ps = PorterStemmer()
        for w in text:
            w = ps.stem(w)
            if w not in self.stopwords:
                filtered.append(w)
        return filtered


if __name__ == '__main__':
    p = './index_pre/'
    i = Index(p)
    i.run()

