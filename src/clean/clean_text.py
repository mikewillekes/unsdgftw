from bs4 import BeautifulSoup
from dataclasses import dataclass
import dataclasses
import re
import json
import unicodedata
import spacy

# Local application imports
from metadata.document_metadata import *
from metadata.paragraph_metadata import *
from config import config

# Load Transformer model via Spacy
nlp = spacy.load('en_core_web_trf')
is_using_gpu = spacy.prefer_gpu()
print (f'Using GPU: {is_using_gpu}')

ENTITY_TYPES = ['EVENT', 'FAC', 'GPE', 'LANGUAGE', 'LAW', 'LOC', 'NORP', 'ORG', 'PERSON', 'PRODUCT', 'WORK_OF_ART']


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

                        # Spacy Pipeline
                        nlp_doc = nlp(clean_text)
                        sentences = [sentence.text for sentence in nlp_doc.sents]
                        entities = [(ent.text, ent.label_) for ent in nlp_doc.ents if ent.label_ in ENTITY_TYPES]

                        # if nlp_doc.sents:
                        #     for sent in nlp_doc.sents:
                        #         print(f'{sent.text}')


                        # if nlp_doc.ents:
                        #     for ent in nlp_doc.ents:
                        #         if ent.label_ in ENTITY_TYPES:
                        #             print(f'{ent.text} >> {ent.label_} ({spacy.explain(ent.label_)})')



                        result.append(ParagraphMetadata(
                            document.organization,
                            document.local_filename,
                            document.about_url,
                            document.download_url,
                            document.title,
                            document.year,
                            page_number,
                            paragraph_number,
                            len(clean_text),
                            clean_text=clean_text,
                            raw_text=raw_text,
                            sentences=sentences,
                            entities=entities))

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


def util_print_ner_types(nlp):
    # en_core_web_trf has:
    #
    # CARDINAL Numerals that do not fall under another type
    # DATE Absolute or relative dates or periods
    # EVENT Named hurricanes, battles, wars, sports events, etc.
    # FAC Buildings, airports, highways, bridges, etc.
    # GPE Countries, cities, states
    # LANGUAGE Any named language
    # LAW Named documents made into laws.
    # LOC Non-GPE locations, mountain ranges, bodies of water
    # MONEY Monetary values, including unit
    # NORP Nationalities or religious or political groups
    # ORDINAL "first", "second", etc.
    # ORG Companies, agencies, institutions, etc.
    # PERCENT Percentage, including "%"
    # PERSON People, including fictional
    # PRODUCT Objects, vehicles, foods, etc. (not services)
    # QUANTITY Measurements, as of weight or distance
    # TIME Times smaller than a day
    # WORK_OF_ART Titles of books, songs, etc.
    for label in nlp.get_pipe('ner').labels:
        print(f'{label} {spacy.explain(label)}')