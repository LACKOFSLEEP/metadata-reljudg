import xml.etree.ElementTree as ET
import json

KEYS = ['docNum', 'docId', 'date', 'section', 'length', 'headline', 'byline', 'type', 'graphic', 'text']


def read_docs(filename, out=False):
	content = list()

	with open(filename) as f:
		xml = '<data>' + f.read() + '</data>'

		root = ET.fromstring(xml)

		for doc in root.findall('DOC'):
			single_doc = {key: None for key in KEYS}
			# doc num & docId
			try:
				docNum = doc.find('DOCNO').text.strip(" ")
				single_doc['docNum'] = docNum

				docId = doc.find('DOCID').text.strip(" ")
				single_doc['docId'] = docId

			except TypeError:
				print('no doc essentials')
				continue

			try:
				date = doc.find('DATE')[0].text.strip()
				single_doc['date'] = date
			except TypeError:
				print('no date')

			try:
				section = doc.find('SECTION')[0].text.strip()
				single_doc['section'] = section
			except TypeError:
				print('no section')

			try:
				length = doc.find('LENGTH')[0].text.strip().lower()
				if 'words' in length:
					length = length.split(" ")[0]
				single_doc['length'] = length
			except TypeError:
				print('no length')

			try:
				headline = doc.find('HEADLINE')[0].text.strip()
				single_doc['headline'] = headline
			except TypeError:
				print('no headline')

			try:
				byline = doc.find('BYLINE')[0].text.strip()
				single_doc['byline'] = byline
			except TypeError:
				print('no byline')

			try:
				t = doc.find('type')[0].text.strip()
				single_doc['type'] = t
			except TypeError:
				print('no type')

			try:
				graph = doc.find('GRAPHIC')[0].text.strip()
				single_doc['graphic'] = graph
			except TypeError:
				print('no graphic')

			try:
				text = "".join(doc.find("TEXT").itertext())
				text = text.strip()
				single_doc['text'] = text
			except TypeError:
				print('no text')
				continue
			except AttributeError as e:
				print(e)
				print(headline)

			content.append(single_doc)

	if out:
		with open('data.json', 'w') as f:
			json.dump(content, f)
	return content


if __name__ == '__main__':
	read_docs('LA022290', True)
