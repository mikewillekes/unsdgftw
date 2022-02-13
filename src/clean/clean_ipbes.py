from bs4 import BeautifulSoup
from dataclasses import dataclass
import dataclasses
import re
import spacy
from collections import Counter
from typing import List
import json
import unicodedata

""" Clean the IPES Global Assessment Report on Biodiversity and Ecosystem Services
"""

@dataclass
class Paragraph:
    page_number: int
    paragraph_number: int
    paragraph_len: int
    keywords: List[str]
    clean_text: str
    raw_text: str

def main():

    nlp = spacy.load('en_core_web_lg')


    result = []

    # Extract Raw and Cleaned (ready for NLP) paragraphs from the XHTML text document
    for p in clean_document('./corpus/IPBES/2-text/202111_2020 IPBES GLOBAL REPORT_FULL_DIGITAL_NOV 2021.pdf.xml'):
        if len(p.clean_text) > 500:
            p.keywords = get_keywords(p.clean_text, nlp)
            # print(f'{p.page_number}:{p.paragraph_number}:{p.keywords}\n{p.clean_text}')
            print(f'{p.page_number}:{p.paragraph_number}:{p.keywords}')
            result.append(json.dumps(dataclasses.asdict(p)) + '\n')

    open('./corpus/IPBES/3-cleantext/202111_2020 IPBES GLOBAL REPORT_FULL_DIGITAL_NOV 2021.jsonl', 'w').writelines(result)


# Very naive Keyword / Hashtag extraction using POS tagging to pull out
# Proper nouns, Adjectives and Nouns.
# https://betterprogramming.pub/extract-keywords-using-spacy-in-python-4a8415478fbf
def get_keywords(text, nlp):
    keywords = []
    for token in nlp(text.lower()):
        if token.pos_ in ['PROPN', 'ADJ', 'NOUN']:
            keywords.append(f'{token.text}')
    return [('#' + keyword[0]) for keyword in Counter(keywords).most_common(5)]
    

def clean_document(filename):
    with open(filename) as fin:
        soup = BeautifulSoup(fin, 'html.parser')
        for page_number, page in enumerate(soup.find_all('div', class_='page')):
            for paragraph_number, paragraph in enumerate(page.find_all('p')):

                raw_text = normalize_whitespace(paragraph.text)
                clean_text = clean_paragraph_text(raw_text)

                yield Paragraph(
                    page_number=page_number,
                    paragraph_number=paragraph_number,
                    paragraph_len=len(clean_text),
                    keywords=[],
                    clean_text=clean_text,
                    raw_text=raw_text)

def normalize_whitespace(s):
    # Normalize all whitespace and newlines to a single line
    return ' '.join(s.split())


def clean_paragraph_text(text):

    # A lot of the source PDFs are academic papers - so have a lot of
    # endnote references. Like:
    #
    #    Plastic is also accumulating along the shorelines
    #    (UNEP, 2016a). The ratio of plastic to fish by weight
    #    in the oceans was 1:5 in 2014 (Ellen MacArthur Foundation, 2013). 
    #
    # Though valuable for academics, we want the pure prose for NLP

    #
    # Note: Originally there were three separare RegExes - but would
    # occasinally run into an issue of too many whitespaces when 
    # multiple sets of parens were back-to-back like this:
    # 
    #   some (value) {section} (reference) thing happened.
    #
    # became
    #
    #   some    thing happened.
    #
    # So I collapsed the regexs into one with | to OR the clauses together
    # however I've left the orginal code in place b/c that big regex is
    # just too difficult to understand otherwise

    # Regular Parens ()
    #text = re.sub(r'\s+\([^()]*\)', '', text)

    # Curly Parens {}
    #text = re.sub(r'\s+{[^{}]*}', '', text)

    # Square Parens []
    #text = re.sub(r'\s+\[[^\[\]]*\]', '', text)

    # Look at the size of this thing!!!
    text = re.sub(r'\s+(({[^{}]*})|(\([^()]*\))|(\[[^\[\]]*\]))', '', text)

    # Collapse to ASCII where possible
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode()

    return text


if __name__ == "__main__":
    main()