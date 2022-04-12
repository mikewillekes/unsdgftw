import re
import time
import csv

from bertopic import BERTopic

# Local application imports
from metadata.document_metadata import *
from metadata.paragraph_metadata import *
from metadata.topic_metadata import *
from config import config


model = BERTopic(embedding_model='all-MiniLM-L6-v2', min_topic_size=100)

paragraph_corpus = []

def main():
    process_document_collections(['IPBES', 'IPCC', 'IUCN', 'MA', 'OKR', 'UNICEF'])
    #process_document_collections(['UNICEF'])


def process_document_collections(document_collections):
    
    paragraph_topics = {}

    #
    # Unlike the SDG --> Sentence semantic similarity, in this case
    # we need to process all the docs at once
    #
    for document_collection_name in document_collections:

        print(f'{document_collection_name}')
        document_metadata_filename = config.get_document_metadata_filename(document_collection_name)
        documents = load_document_metadata(document_metadata_filename)
        paragraph_topics[document_collection_name] = []
        
        for document in documents:
            print(f'{document.local_filename}')
            
            # Process document retuns a list of tuples of (document, paragraph)
            paragraph_corpus.extend(process_document(document_collection_name, document))
            print(f'{len(paragraph_corpus)} total paragraphs')
    
    # Build topic model and fit to current corpus
    print(f'Topic Modelling {len(paragraph_corpus)} paragraphs; Please wait...')
    topic_numbers, probabilities = model.fit_transform([p[1].clean_text for p in paragraph_corpus])

    #
    # Write a mapping file that we'll later user to include/exclude and rename topics
    #
    with open(f'{config.CORPUS_DIR}/resources/topic_mapping.csv', 'w') as fout:
        writer = csv.reader(fout, delimiter=',', quotechar='"',  quoting=csv.QUOTE_MINIMAL)
        for topic_number in model.get_topics():

            if topic_number == 0:
                continue

            #
            # First column writes a 1 by default (include this topic in graph),
            # to exclude topic change to a 0 in ./resources/topic_mapping.csv
            # before running graph builder
            #
            writer.writerow([
                1, 
                'Friendly Name',
                topic_number, 
                model.get_topic_info(topic_number)['Name'].item(),
                '|'.join([t[0] for t in model.get_topic(topic_number)])
            ])

    for (topic_number, topic_probability, document_collection_name, paragraph_id, paragraph_clean_text) in zip(
        topic_numbers,
        probabilities,
        [p[0].corpus_id for p in paragraph_corpus],
        [p[1].id for p in paragraph_corpus],
        [p[1].clean_text for p in paragraph_corpus]):

            if (topic_number > 0):
                paragraph_topics[document_collection_name].append(TopicMetadata(
                    model.get_topic_info(topic_number)['Name'].item(),  # It's a Pandas Series, use .item() to fetch the string value
                    topic_number,
                    topic_probability,
                    [t[0] for t in model.get_topic(topic_number)],
                    paragraph_id,
                    paragraph_clean_text))

    for document_collection_name in document_collections:
        save_topic_metadata(config.get_topic_metadata_filename(document_collection_name), paragraph_topics[document_collection_name])


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