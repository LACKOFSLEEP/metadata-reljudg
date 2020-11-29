from xml.etree import ElementTree
import re
import json
import os


def read_docs(path) -> str:
    with open(path) as f:
        raw = f.read()
        raw = f"<ROOT>{raw}</ROOT>"
        return raw


def parse_doc(xml: str) -> None:
    xml = re.sub('<!--[^>]*-->', '', xml).strip()
    xml = re.sub('&[^>]*;', ' ', xml).strip()

    docs = []

    root = ElementTree.fromstring(xml)
    doc: ElementTree.Element
    for doc in root:
        doc_id = doc.find('DOCNO').text.strip()
        text = ''
        try:
            # LA
            text = "".join(doc.find('TEXT').itertext()).strip()
        except AttributeError:
            pass

        docs.append(
            {doc_id: text}
        )

    with open('./index_pre/' + doc_id, 'w', encoding='utf-8') as f:
        json.dump(docs, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    p = './disk5/LATIMES/LA/'
    for fp in os.listdir(p):
        if fp.startswith("LA"):
            print(f'processing {fp}')
            parse_doc(read_docs(p + fp))






