import re
import time

from bertopic import BERTopic
from sentence_transformers import SentenceTransformer,util
import torch

# Local application imports
from metadata.document_metadata import *
from metadata.paragraph_metadata import *
from metadata.nlp_metadata import *
from config import config
from sdgs.sustainable_development_goals import *
from clean.clean_text import normalize_unicode

#embedder = SentenceTransformer('all-MiniLM-L6-v2')

model = BERTopic(embedding_model='all-MiniLM-L6-v2')

paragraph_corpus = []

def main():
    #process_document_collections(['IPBES', 'IPCC', 'IUCN', 'MA', 'OKR', 'UNICEF'])
    process_document_collections(['OKR', 'UNICEF'])


def process_document_collections(document_collections):
    
    #
    # Unlike the SDG --> Sentence semantic similarity, in this case
    # we need to process all the docs at once
    #
    for document_collection_name in document_collections:

        print(f'{document_collection_name}')
        document_metadata_filename = config.get_document_metadata_filename(document_collection_name)
        documents = load_document_metadata(document_metadata_filename)
        
        for document in documents:
            print(f'{document.local_filename}')
            
            # Process document retuns a list of tuples of (document, paragraph)
            paragraph_corpus.extend(process_document(document_collection_name, document))
            print(f'{len(paragraph_corpus)} total paragraphs')
    
    # Build embeddings
    print(f'Topic Modelling {len(paragraph_corpus)} paragraphs; Please wait...')

    topics, probabilities = model.fit_transform([p[1].clean_text for p in paragraph_corpus])
    
    for t in model.get_topics():
        print(t[0], t[1])
    
        



def process_document(document_collection_name, document):
    # Build a collection of tuples (document, paragraph)
    return list(build_paragraph_corpus(document_collection_name, document))


def build_paragraph_corpus(document_collection_name, document):
    paragraph_metadata_filename = config.get_paragraph_metadata_filename(document_collection_name, document.local_filename)
    paragraphs = load_paragraph_metadata(paragraph_metadata_filename)

    for paragraph in paragraphs:
        yield (document, paragraph)


if __name__ == "__main__":
    main()