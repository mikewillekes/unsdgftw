from bs4 import BeautifulSoup
from dataclasses import dataclass
import dataclasses
import re
import json
import unicodedata

# Local application imports
from metadata.document_metadata import *
from metadata.paragraph_metadata import *
from config import config


def clean_document_collection(document_collection_name):

    document_metadata_filename = config.get_document_metadata_filename(document_collection_name)
    documents = load_document_metadata(document_metadata_filename)
    
    for document in documents:
        paragraph_metadata_filename = config.get_paragraph_metadata_filename(document_collection_name, document.local_filename)
        paragraphs = clean_xhtml_document(document_collection_name, document)
        save_paragraph_metadata(paragraph_metadata_filename, paragraphs)
   

def clean_xhtml_document(document_collection_name, document):

    xhtml_filename = config.get_document_xhtml_filename(document_collection_name, document.local_filename)
    print(f'\n{document_collection_name} >> {document.title} >> {xhtml_filename} ', end='')

    result = []

    with open(xhtml_filename) as fin:
        soup = BeautifulSoup(fin, 'html.parser')
        for page_number, page in enumerate(soup.find_all('div', class_='page')):
            print('.', end='')
            for paragraph_number, paragraph in enumerate(page.find_all('p')):

                if paragraph.text:
                    raw_text = normalize_unicode(normalize_whitespace(paragraph.text))
                    clean_text = clean_parentheses(raw_text)

                    if len(clean_text) > config.NLP_MIN_PARAGRAPH_LENGTH:
                        result.append(ParagraphMetadata(
                            document.organization,
                            document.local_filename,
                            document.about_url,
                            document.download_url,
                            document.title,
                            document.summary,
                            document.year,
                            page_number,
                            paragraph_number,
                            len(clean_text),
                            clean_text=clean_text,
                            raw_text=raw_text))

    print('')
    return result


def normalize_whitespace(s):
    # Normalize all whitespace and newlines to a single line
    return ' '.join(s.split())


def normalize_unicode(s):
    # Normalize/collapse unicode characters to the best ASCII equivilent
    return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()


def clean_parentheses(s):

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
    #s = re.sub(r'\s+\([^()]*\)', '', s)

    # Curly Parens {}
    #s = re.sub(r'\s+{[^{}]*}', '', s)

    # Square Parens []
    #s = re.sub(r'\s+\[[^\[\]]*\]', '', s)

    # Look at the size of this thing!!!
    return re.sub(r'\s+(({[^{}]*})|(\([^()]*\))|(\[[^\[\]]*\]))', '', s)
