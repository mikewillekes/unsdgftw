import re
import time

from sentence_transformers import SentenceTransformer,util
import torch

# Local application imports
from metadata.document_metadata import *
from metadata.paragraph_metadata import *
from metadata.nlp_metadata import *
from config import config
from sdgs.sustainable_development_goals import *
from clean.clean_text import normalize_unicode

embedder = SentenceTransformer('all-MiniLM-L6-v2')

sentence_corpus = []

def main():
    process_document_collections(['IPBES', 'IPCC', 'IUCN', 'MA', 'OKR', 'UNICEF'])
    #process_document_collections(['OKR', 'UNICEF'])


def process_document_collections(document_collections):
    
    #
    # Unlike the SDG --> Sentence semantic similarity, in this case
    # we need to process all the sentences at once
    #
    for document_collection_name in document_collections:

        print(f'{document_collection_name}')
        document_metadata_filename = config.get_document_metadata_filename(document_collection_name)
        documents = load_document_metadata(document_metadata_filename)
        
        for document in documents:
            print(f'{document.local_filename}')
            
            # Process document retuns a list of tuples of (document, paragraph, sentence)
            sentence_corpus.extend(process_document(document_collection_name, document))
            print(f'{len(sentence_corpus)} total sentences')
    
    # Build embeddings
    print(f'Encoding {len(sentence_corpus)} sentences; Please wait...')

    # Sentence embeddings for each sentence
    sentence_embeddings = embedder.encode(
        [s[2].text for s in sentence_corpus],
        batch_size=64,
        show_progress_bar=True,
        convert_to_tensor=True)


    print('Start clustering')
    start_time = time.time()

    # Two parameters to tune:
    #
    #   min_cluster_size: Only consider cluster that have at least 25 elements
    #   threshold: Consider sentence pairs with a cosine-similarity larger than threshold as similar
    clusters = util.community_detection(sentence_embeddings, min_community_size=25, threshold=0.6)

    print('Clustering done after {:.2f} sec'.format(time.time() - start_time))

    # Print for all clusters the top 3 and bottom 3 elements
    for i, cluster in enumerate(clusters):
        print(f'Cluster {i+1} : {len(cluster)}')
        for index in cluster[0:3]:
            document = sentence_corpus[index][0]
            paragraph = sentence_corpus[index][1]
            sentence = sentence_corpus[index][2] 
            print(f'{document.title} : {sentence.text}')


def process_document(document_collection_name, document):

    # For semantic similarty search we'll build a corpus of sentences and then 
    # match against collection of SDGs
    #
    # Build a collection of tuples (document, paragraph, sentence)
    return list(build_sentence_corpus(document_collection_name, document))


def build_sentence_corpus(document_collection_name, document):
    paragraph_metadata_filename = config.get_paragraph_metadata_filename(document_collection_name, document.local_filename)
    paragraphs = load_paragraph_metadata(paragraph_metadata_filename)

    for paragraph in paragraphs:
        for sentence in paragraph.sentences:
            yield (document, paragraph, sentence)


if __name__ == "__main__":
    main()