
# =========================
# Paths of the raw and processed documents
CORPUS_DIR = 'corpus'
RAW_DIR = '1-raw'
TEXT_DIR = '2-text'
CLEANTEXT_DIR = '3-cleantext'
NLP_DIR = '4-nlp'

# =========================
# Filenames
DOCUMENT_METADATA_FILENAME = 'metadata.jsonl'

# =========================
# File extensions

# RAW_EXTENSION is excluded b/c it can be anything that TIKA can support parsing
TEXT_EXTENSION = '.xml'
CLEANTEXT_EXTENSION = '.jsonl'

# =========================
# NLP Pipeline Vars

# Ignore Paragraphs shorter than
NLP_MIN_PARAGRAPH_LENGTH = 200


def get_document_metadata_filename(document_collection_name):
    return f'{CORPUS_DIR}/{document_collection_name}/{DOCUMENT_METADATA_FILENAME}'


def get_document_xhtml_filename(document_collection_name, local_document_filename):
    return f'{CORPUS_DIR}/{document_collection_name}/{TEXT_DIR}/{local_document_filename}{TEXT_EXTENSION}'


def get_paragraph_metadata_filename(document_collection_name, local_document_filename):
    return f'{CORPUS_DIR}/{document_collection_name}/{CLEANTEXT_DIR}/{local_document_filename}{CLEANTEXT_EXTENSION}'