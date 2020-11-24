import json
import os
import re


def read_topic(filename):
    topics = list()
    with open(filename) as f:
        for i in f:
            data = json.loads(i)
            topics.append(data)
    return topics


def generate_chunk(topics):
    for topic in topics:
        t_name = topic['topic']
        docs = topic['doc']
        num = len(topic['doc'])
        count = 0
        for doc in docs:

            # print('Processing ' + doc)
            doc_str = '<DOC>\n'
            stopper = '</DOC>'

            files = []
            if doc.startswith('FT'):
                files = [i for i in os.listdir('./docsInS4/') if i.startswith(doc.split('-')[0])]

            elif doc.startswith('FB'):
                files = [i for i in os.listdir('./docsInS4/') if i.startswith('FB' + doc.split('-')[0][-1])]

            elif doc.startswith('FR'):
                files.append(doc.split('-')[0] + '.' + doc.split('-')[1])
            else:
                files.append(doc.split('-')[0])
            for file_name in files:
                with open('docsInS4/' + file_name, 'r') as f:
                    for line in f:
                        if doc in line:
                            if re.match(r'^<DOCNO>\s*{}\s*</DOCNO>$'.format(doc), line):
                                # print('Found.')
                                count += 1
                                doc_str += line
                        if len(doc_str) > 6:
                            line = re.sub(r"<\w* \w*=\w*>", "<F>", line)
                            line = re.sub(r"&\w*;", "", line)
                            line = re.sub(r"<\w* \w*=(\w|-)*>", "<FIG>", line)
                            doc_str += line
                        if len(doc_str) > 6 and stopper in line:
                            break
                if len(doc_str) > 6:
                    break

            with open('./docsForExpByTopic/' + str(t_name), 'a') as f:
                f.write(doc_str)
        print("topic" + str(t_name) + 'done.')
        print(f'Found {count} of {num}')



if __name__ == '__main__':
    generate_chunk(read_topic("docListForExp.tom"))
