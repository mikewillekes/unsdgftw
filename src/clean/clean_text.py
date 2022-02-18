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
from clean.phrase_matcher import initialize_phrase_matcher
from config import config
from metadata import paragraph_metadata

# Load Transformer model via Spacy
nlp = spacy.load('en_core_web_trf')
matcher = initialize_phrase_matcher(nlp)
is_using_gpu = spacy.prefer_gpu()
print (f'Using GPU: {is_using_gpu}')

# NER Entity types from the Spacy 'en_core_web_trf' model
ENTITY_TYPES = ['EVENT', 'FAC', 'GPE', 'LANGUAGE', 'LAW', 'LOC', 'NORP', 'ORG', 'PERSON', 'PRODUCT', 'WORK_OF_ART']


def main():
    clean_document_collection('IUCN')


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

        # 
        # We iterated page-by-page, but paragraphs span mulitiple pages.
        # Based on some simple rules we stitch-together mulitple paragraphs
        #
        #  - If a paragraph begins with a lowercase letter, append it to the prev. paragraph
        #
        current_chunk_page_number = 0
        current_chunk_paragraph_number = 0
        current_chunk_paragraph_text = ''

        #
        # Split into Pages and process each page
        #
        for page_number, page in enumerate(soup.find_all('div', class_='page')):
            print('.', end='')
            
            #
            # Split into Paragraphs and process each paragraph
            #
            for paragraph_number, paragraph in enumerate(page.find_all('p')):

                if paragraph.text:
                    raw_text = normalize_unicode(normalize_whitespace(paragraph.text))
                    
                    if not raw_text:
                        continue
                    
                    if  raw_text[0].isupper() or raw_text[0].isdigit():
                        
                        #
                        # A new paragraph beginning with a Capital letter or Number. 
                        # Process the previous paragraph and start a new chunk.
                        #
                        if (current_chunk_page_number > 0 and current_chunk_paragraph_number > 0):
                            current_result = process_chunk(document, current_chunk_page_number, current_chunk_paragraph_number, current_chunk_paragraph_text)
                            if current_result:
                                result.append(current_result)

                        # This means that a paragraphs that spans multiple pages will 
                        # be recorded as the Page Number and Paragraph Number of the first chunk        
                        current_chunk_page_number = page_number
                        current_chunk_paragraph_number = paragraph_number
                        current_chunk_paragraph_text = raw_text

                    else:
                        
                        #
                        # Likely this is a continuation of the previous paragraph
                        #
                        current_chunk_paragraph_text = current_chunk_paragraph_text + ' ' + raw_text

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


def process_chunk(document, page_number, paragraph_number, paragraph_text):

    clean_text = clean_parentheses(paragraph_text)

    # Discarding very short paragraphs could mean that we throw away some
    # headlines and fragments of sentences - but it's more important that we 
    # are generally cleaning and discarding junk like:
    #
    #    <div class="page"><p />
    #    <p>C
    #    O
    #    </p>
    #    <p>U
    #    N
    #    </p>
    #    <p>TR
    #    Y
    #    </p>
    #    <p>G
    #    en
    #    </p>
    #
    if len(clean_text) > config.NLP_MIN_PARAGRAPH_LENGTH:

        # Spacy Pipeline
        nlp_doc = nlp(clean_text)
        sentences = [sentence.text for sentence in nlp_doc.sents]
        entities = [(ent.text, ent.label_) for ent in nlp_doc.ents if ent.label_ in ENTITY_TYPES]
        
        # Match specific keyword/phrases from <resources/MatchPhrases.txt>
        # A quick-and-dirty way to capture rules-based entities without complex ML training
        matches = matcher(nlp_doc)
        phrase_matches = [nlp_doc[start:end].text for match_id, start, end in matches]

        # if nlp_doc.sents:
        #     for sent in nlp_doc.sents:
        #         print(f'{sent.text}')


        # if nlp_doc.ents:
        #     for ent in nlp_doc.ents:
        #         if ent.label_ in ENTITY_TYPES:
        #             print(f'{ent.text} >> {ent.label_} ({spacy.explain(ent.label_)})')
        # print(f'PAGE {page_number}, PARA {paragraph_number} : <p>{clean_text}</p>')

        return ParagraphMetadata(
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
            raw_text=paragraph_text,
            sentences=sentences,
            entities=entities,
            phrase_matches=phrase_matches)


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


if __name__ == "__main__":
    main()