from bs4 import BeautifulSoup
from dataclasses import dataclass
from collections import Counter
import dataclasses
import re
import json
import unicodedata
import hashlib

# Spacy for NLP
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

            # Guard againt very long documents during development
            if page_number > config.MAX_PAGES_PER_DOCUMENT:
                break

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


def remove_punctuation(s):
    return re.sub(r'[^\w\s]', '', s)


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


def remove_stopwords(s):
    tokens = [token for token in s.split() if token.lower() not in nlp.Defaults.stop_words]
    return ' '.join(tokens)


def is_prose(nlp_doc):

    # TODO: Turn this into a supervised ML model!

    """
        We want to be able to identify paragraphs of unstructured prose that are good candidates
        for sentence segmentation and NLP.
        This is a simple, rules-based way to use Part-of-Speech tagging and simple hueristics to identify

        a paragraph that is likely a references block:

            Powell, B., Thilsted, S. H., Ickowitz, A., Termote, C., Sunderland, T., & Herforth, A.. Improving diets with wild and
            cultivated biodiversity from across the landscape. Food Security, 7(3), 535554.
            https://doi.org/10.1007/s12571- 015-0466-5
            Counter({'PUNCT': 17, 'PROPN': 15, 'NUM': 7, 'NOUN': 3, 'ADP': 3, 'CCONJ': 2, 'ADJ': 2, 'VERB': 1, 'DET': 1, 'X': 1})

        vs.

            Chapter 3 addresses the questions of How much progress has been made towards the Aichi Biodiversity Targets and the
            objectives of other biodiversity-related agreements, and how do nature and its contributions to people contribute to
            the implementation of the Sustainable Development Goals? Building upon findings from chapter 2 and additional evidence
            from analyses of indicators and literature reviews, the chapter assesses progress towards meeting major international
            objectives related to biodiversity and sustainable development, with special attention given to the Aichi Biodiversity
            Targets and to relevant Sustainable Development Goals. The chapter also examines the objectives of other biodiversity-
            related agreements: Convention on Migratory Species, Convention on International Trade in Endangered Species, Ramsar
            Convention on Wetlands, Convention to Combat Desertification, World Heritage Convention, International Plant Protection
            Convention, Convention on the Conservation of
            Counter({'PROPN': 34, 'NOUN': 27, 'ADP': 21, 'PUNCT': 13, 'VERB': 12, 'DET': 10, 'ADJ': 9, 'CCONJ': 7, 'SCONJ': 3, 'AUX': 3, 'NUM': 2, 'PRON': 1, 'ADV': 1, 'PART': 1})

        Apply POS Tagging and then look at the ratio of PUNCT and PROPN to count of tokens.   
    """
    pos_tokens = [token.pos_ for token in nlp_doc] 
    counter = Counter(pos_tokens)

    # Score = ratio of Proper Nouns & Punct to all tokens
    score = 1 - (counter['PROPN'] + counter['PUNCT']) / len(pos_tokens)
    
    #
    # Calculate weighted (by length of string) average position of PROPN.
    # If Proper Nouns tend to occur in the first half of the string then
    # likely this string is a collection of endnote references
    #
    positions = [index for index, token in enumerate(nlp_doc) if token.pos_ in ['PROPN']]
    if len(positions) == 0:
        # no proper nouns
        return True

    average_position = (sum(positions) / len(positions)) / len(pos_tokens)

    if score < 0.6 and average_position < 0.5:
        # Not Prose
        return False
    else:
        # Yes Prose
        return True


def generate_entity_id(entity_text):
    """
        Generate a unique id for the document by normalizing and hashing 
        the entity text field.
    """
    s = entity_text.lower()
    s = remove_punctuation(s)
    s = s.strip()
    s = remove_stopwords(s.lower())
    #print(f'{entity_text} >>> {s}')
    return hashlib.sha256(s.encode('utf-8')).hexdigest()


def process_chunk(document, page_number, paragraph_number, paragraph_text):
    """
        return None if the chunk is skipped (i.e. too short, poor-quality text) 
    """

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
    #
    if len(clean_text) <= config.NLP_MIN_PARAGRAPH_LENGTH:
        return None

    # Spacy Pipeline
    nlp_doc = nlp(clean_text)

    # Check for density of Prose in the paragraph
    if not is_prose(nlp_doc):
        return None

    #
    # Process result of NLP pipeline
    # 
    sentences = [
        Sentence(generate_sentence_id(document.id, page_number, paragraph_number, sentence_numeber), sentence.text) for sentence_numeber, sentence in enumerate(nlp_doc.sents) 
        if len(sentence) > config.NLP_MIN_SENTENCE_LENGTH]

    entities = [Entity(
        generate_entity_id(ent.text),
        generate_mention_id(document.id, page_number, paragraph_number, ent.label_, entity_number),
        ent.text, 
        ent.label_) for entity_number, ent in enumerate(nlp_doc.ents) if ent.label_ in ENTITY_TYPES]
    
    # Match specific keyword/phrases from <resources/MatchPhrases.txt>
    # A quick-and-dirty way to capture rules-based entities without complex ML training
    matches = matcher(nlp_doc)
    entities.extend([
        Entity(
            generate_entity_id(nlp_doc[match[1]:match[2]].text),
            generate_mention_id(document.id, page_number, paragraph_number, 'PHRASE', entity_number),
            nlp_doc[match[1]:match[2]].text,
            'PHRASE') for entity_number, match in enumerate(matches)])

    # if nlp_doc.sents:
    #     for sent in nlp_doc.sents:
    #         print(f'{sent.text}')


    # if nlp_doc.ents:
    #     for ent in nlp_doc.ents:
    #         if ent.label_ in ENTITY_TYPES:
    #             print(f'{ent.text} >> {ent.label_} ({spacy.explain(ent.label_)})')
    # print(f'PAGE {page_number}, PARA {paragraph_number} : <p>{clean_text}</p>')

    return ParagraphMetadata(
        generate_paragraph_id(document.id, page_number, paragraph_number),
        document.id,
        page_number,
        paragraph_number,
        len(clean_text),
        clean_text=clean_text,
        raw_text=paragraph_text,
        sentences=sentences,
        entities=entities)


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