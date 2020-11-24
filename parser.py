import xml.etree.ElementTree as ET
from lxml import etree, html
import json
import re
import os
import sys
import csv

METADATA = ['title', 'author', 'date', 'length', 'frequency', 'tf-idf', 'human', 'machine', 'difficulty',
            'reading_time', 'readability']


class DocParser:

    def __init__(self, filename: str):
        self.topicId = filename.split('/')[-1]
        self.metadata_dict = {}
        self.txt_dict = {}
        self.trec_dict = {}
        self.sormunen_dict = {}
        self.docs = []

        self.load_scores()
        with open(filename) as f:
            doc_str = ''
            for line in f:
                if "<DOC>" in line or doc_str:
                    doc_str += line
                if "</DOC>" in line:
                    try:
                        doc = ET.fromstring(doc_str)
                    except ET.ParseError:
                        print(doc_str)
                        with open('error.log', 'w') as fp:
                            fp.write(doc_str)
                        sys.exit(3)
                    doc_str = ''

                    self.docs.append(doc)

    def load_scores(self):
        with open('./docListForExp.tom') as f:
            for i in f:
                data = json.loads(i)
                topic = data['topic']
                docs = data['doc']
                trec = data['trec']
                sormunen = data['sormunen']

                for j in range(len(docs)):
                    self.trec_dict[docs[j]] = trec[j]
                    self.sormunen_dict[docs[j]] = sormunen[j]

    def run(self):
        c = 0
        for doc in self.docs:
            doc_num = doc.find('DOCNO').text.strip()
            # print(f'processing {doc_num}')
            if doc_num.startswith("LA"):
                self.LA_parser(doc)
                c += 1
            elif doc_num.startswith("FB"):
                pass
                # self.FB_parser(doc)
            elif doc_num.startswith('FR'):
                self.FR_parser(doc)
            else:
                self.FT_parser(doc)
                c += 1
        print(f'{c} of {len(self.docs)} for topic {self.topicId}')
        return c

    def FB_parser(self, doc: ET.Element) -> None:
        metadata_dict = {i: None for i in METADATA}

        doc_num = doc.find('DOCNO').text.strip(" ")
        text_tag = doc.find('TEXT')
        text = text_tag.text
        print(text)

    def FR_parser(self, doc):
        pass

    def FT_parser(self, doc: ET.Element) -> None:

        metadata_dict = {i: None for i in METADATA}

        doc_num = doc.find('DOCNO').text.strip(" ")

        try:
            text = doc.find("TEXT").text.strip()
            length = len(re.findall(r'\w+', text))
            metadata_dict['length'] = length
        except AttributeError:
            print('no text')

        try:
            headline = doc.find('HEADLINE').text.strip()
            split = headline.split('/')[1].strip()
            metadata_dict['title'] = split
        except AttributeError:
            print('no headline')
        except IndexError:
            metadata_dict['title'] = headline

        try:
            date = headline.split('/')[0]
            date = re.search(r'\d+ \w+ \d+', date).group(0)
            metadata_dict['date'] = date
        except IndexError or AttributeError:
            print('no date')
            # TODO if try not working, extract date tag

        try:
            byline = doc.find('BYLINE').text.strip()
            metadata_dict['author'] = byline
        except AttributeError:
            pass

        self.metadata_dict[doc_num] = metadata_dict
        self.txt_dict[doc_num] = text

    def LA_parser(self, doc: ET.Element) -> None:

        metadata_dict = {i: None for i in METADATA}
        doc_num = doc.find('DOCNO').text.strip(" ")

        try:
            text = "".join(doc.find("TEXT").itertext())
            text = text.strip()

        except TypeError:
            print('no text')
        except AttributeError as e:
            print(e)
            print(doc_num)
            return

        try:
            date = doc.find('DATE')[0].text.strip()
            metadata_dict['date'] = date
        except TypeError:
            print('no date')

        try:
            length = doc.find('LENGTH')[0].text.strip().lower()
            if 'words' in length:
                length = length.split(" ")[0]
            metadata_dict['length'] = length
        except TypeError:
            metadata_dict['length'] = len(re.findall(r'\w+', text))
            print('no length')

        try:
            headline = doc.find('HEADLINE')[0].text.strip()
            metadata_dict['title'] = headline
        except TypeError:
            print('no headline')

        try:
            byline = doc.find('BYLINE')[0].text.strip()
            metadata_dict['author'] = byline
        except TypeError:
            pass

        self.metadata_dict[doc_num] = metadata_dict
        self.txt_dict[doc_num] = text

    def csv_writer(self):
        fields = METADATA.copy()
        fields.insert(0, 'doc_num')
        fields.insert(1, 'trec')
        fields.insert(2, 'sormunen')
        with open(f'out_{self.topicId}.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            k: str
            v: dict
            for k, v in self.metadata_dict.items():
                m = v.copy()
                m['doc_num'] = k
                m['trec'] = self.trec_dict[k]
                m['sormunen'] = self.sormunen_dict[k]
                writer.writerow(m)


if __name__ == '__main__':
    for file in os.listdir('./docsForExpByTopic/'):

        d = DocParser('./docsForExpByTopic/' + file)

        count = d.run()
        d.csv_writer()

