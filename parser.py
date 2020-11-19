import xml.etree.ElementTree as ET
from lxml import etree, html
import json
import re

METADATA = ['title', 'author', 'date', 'length', 'frequency', 'tf-idf', 'human', 'machine', 'difficulty',
            'reading_time', 'readability']


class DocParser:

    def __init__(self, filename):
        self.topicId = filename
        self.metadata_list = []
        self.txt_list = []
        self.docs = []
        with open(filename) as f:
            doc_str = ''
            for line in f:
                if "<DOC>" in line or doc_str:
                    doc_str += line
                if "</DOC>" in line:
                    doc = ET.fromstring(doc_str)
                    doc_str = ''
                    doc_num = doc.find('DOCNO').text.strip()
                    print(doc_num)
                    # TODO the ET seems do not support attr with no quote, but this problem only happens in FB

                    self.docs.append(doc)

    def run(self):
        for doc in self.docs:
            doc_num = doc.find('DOCNO').text.strip()
            if doc_num.startswith("LA"):
                self.LA_parser(doc)
            elif doc_num.startswith("FB"):
                self.FB_parser(doc)
            elif doc_num.startswith('FR'):
                self.FR_parser(doc)
            else:
                self.FT_parser(doc)

    def FB_parser(self, doc):
        pass

    def FR_parser(self, doc):
        pass

    def FT_parser(self, doc):
        pass

    def LA_parser(self, doc: ET.Element) -> None:

        metadata_dict = {i: None for i in METADATA}
        txt_dict = {}

        doc_num = doc.find('DOCNO').text.strip(" ")

        try:
            text = "".join(doc.find("TEXT").itertext())
            text = text.strip()
            txt_dict[doc_num] = text
        except TypeError:
            print('no text')
        except AttributeError as e:
            print(e)

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
            metadata_dict['length'] = len(re.findall(r'\w+', txt_dict[doc_num]))
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
            print('no byline')

        print(metadata_dict)
        self.metadata_list.append(metadata_dict)
        self.txt_list.append(txt_dict)


if __name__ == '__main__':
    d = DocParser('./docsForExpByTopic/402')
    d.run()

