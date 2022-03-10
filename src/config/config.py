
# =========================
# Paths of the raw and processed documents
CORPUS_DIR = 'corpus'
RAW_DIR = '1-raw'
TEXT_DIR = '2-text'
CLEANTEXT_DIR = '3-cleantext'
NLP_DIR = '4-nlp'
GRAPH_DIR = '5-graph'


# =========================
# Other Pathnames and Filenames
CORPUS_METADATA_FILENAME = 'metadata.jsonl'
DOCUMENT_METADATA_FILENAME = 'metadata.jsonl'
TOPIC_METADATA_FILENAME = 'topics.jsonl'
SDGS_FILENAME = f'{CORPUS_DIR}/resources/Sustainable Development Goals Feb 2022.csv'
MATCH_PHRASES_FILENAME = f'{CORPUS_DIR}/resources/MatchPhrases.txt'

# =========================
# File extensions

# RAW_EXTENSION is excluded b/c it can be anything that TIKA can support parsing
TEXT_EXTENSION = '.xml'
CLEANTEXT_EXTENSION = '.jsonl'
NLP_EXTENSION = '.jsonl'
GRAPH_EXTENSION = '.csv'

# =========================
# NLP Pipeline Vars

# Ignore Paragraphs shorter than (Characters)
NLP_MIN_PARAGRAPH_LENGTH = 100

# Ignore Sentences shorter than (Characters)
NLP_MIN_SENTENCE_LENGTH = 30

# Max number of pages to process per document (helpful to speed things
# up during developement). There are some 3000+ page docs in the corpus!
MAX_PAGES_PER_DOCUMENT = 500


# =========================
# TigerGraph Config
GRAPH_NAME = 'UNSDGs'

def get_corpus_metadata_filename():
    return f'{CORPUS_DIR}/{CORPUS_METADATA_FILENAME}'


def get_document_metadata_filename(document_collection_name):
    return f'{CORPUS_DIR}/{document_collection_name}/{DOCUMENT_METADATA_FILENAME}'


def get_document_xhtml_filename(document_collection_name, local_document_filename):
    return f'{CORPUS_DIR}/{document_collection_name}/{TEXT_DIR}/{local_document_filename}{TEXT_EXTENSION}'


def get_paragraph_metadata_filename(document_collection_name, local_document_filename):
    return f'{CORPUS_DIR}/{document_collection_name}/{CLEANTEXT_DIR}/{local_document_filename}{CLEANTEXT_EXTENSION}'


def get_nlp_metadata_filename(document_collection_name, local_document_filename):
    return f'{CORPUS_DIR}/{document_collection_name}/{NLP_DIR}/{local_document_filename}{NLP_EXTENSION}'

def get_topic_metadata_filename(document_collection_name):
    return f'{CORPUS_DIR}/{document_collection_name}/{NLP_DIR}/{TOPIC_METADATA_FILENAME}'


def get_graph_staging_dir(document_collection_name):
    return f'{CORPUS_DIR}/{document_collection_name}/{GRAPH_DIR}'
