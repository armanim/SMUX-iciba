__author__ = 'xudongwu'

import sys
import urllib
import json
import cgi
import re

url_base = "http://dict-co.iciba.com/api/dictionary.php?key=50047AA12F0CBAF069B6052DC978EDAE&type=json&w="
index = {}

def create_index():
    with open("WordNet_3_0_mini.txt", "r") as f:
        searchlines = f.readlines()
        for i, line in enumerate(searchlines):
            if line[0].lower() in index:
                index[line[0].lower()] = [index[line[0].lower()][0], i]
            else:
                index[line[0].lower()] = [i, i]

def definition_en(word):
    result = ""
    with open("WordNet_3_0_mini.txt", "r") as f:
        searchlines = f.readlines()

        for i, line in enumerate(searchlines[index[word[0].lower()][0]:index[word[0].lower()][1]]):
            if re.search("^" + word + "\s$", line):
                result += searchlines[index[word[0].lower()][0] + i + 1]
                break
    return "<b>" + word + "</b><br/>" + re.sub("</?trn>", '', result)

# main
create_index()
out = open(sys.argv[2], mode='w')
for line in open(sys.argv[1]):
    word = line.translate(None, '\n')
    result = json.loads(cgi.escape(urllib.urlopen(url_base + word).read()))
    if 'word_name' in result:
        word_name = result['word_name']
        definition = result['symbols'][0]
        pronunciation = definition['ph_am']
        parts = definition['parts']

        out.write("Q: " + word + '\n' )
        if pronunciation is None:
            out.write(("A: " + word_name + "<br/>").encode('utf8'))
        else:
            out.write(("A: " + word_name + " | " + pronunciation + "<br/>").encode('utf8'))

        for part in parts:
            form = part['part']
            meaning = part['means']

            out.write(("<br/>" + form + " " + ";".join(meaning)).encode('utf8'))

        out.write("<br/>" + definition_en(word_name))

        out.write('\n\n\n')

