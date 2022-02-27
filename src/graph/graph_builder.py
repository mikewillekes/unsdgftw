import csv

# Local application imports
from metadata.corpus_metadata import *
from metadata.document_metadata import *
from metadata.paragraph_metadata import *
from metadata.nlp_metadata import *
from config import config
from sdgs.sustainable_development_goals import *


CORPUS_NODES = 'corpus_nodes' + config.GRAPH_EXTENSION
DOCUMENT_NODES = 'document_nodes' + config.GRAPH_EXTENSION
PARAGRAPH_NODES = 'paragraph_nodes' + config.GRAPH_EXTENSION
MENTION_NODES = 'mention_nodes' + config.GRAPH_EXTENSION
SENTENCE_NODES = 'sentence_nodes' + config.GRAPH_EXTENSION
ENTITY_NODES = 'entity_nodes' + config.GRAPH_EXTENSION
SDG_NODES = 'sdg_nodes' + config.GRAPH_EXTENSION

CORPUS_TO_DOCUMENT_EDGES = 'corpus_to_document_edges.csv' + config.GRAPH_EXTENSION
DOCUMENT_TO_PARAGRAPH_EDGES = 'document_to_paragraph_edges.csv' + config.GRAPH_EXTENSION
PARAGRAPH_TO_SENTENCE_EDGES = 'paragraph_to_sentence_edges.csv' + config.GRAPH_EXTENSION
SENTENCE_TO_SDG_EDGES = 'sentence_to_sdg_edges.csv' + config.GRAPH_EXTENSION
PARAGRAPH_TO_ENTITY_EDGES = 'paragraph_to_mention_edges.csv'  + config.GRAPH_EXTENSION
MENTION_TO_ENTITY_EDGES = 'mention_to_entity_edges.csv' + config.GRAPH_EXTENSION

def main():
    stage_graph_data('IUCN')


def stage_graph_data(document_collection_name):
    stage_nodes(document_collection_name)
    stage_edges(document_collection_name)


def build_writer(f, header_row):
    writer = csv.writer(f, delimiter=',', quotechar='"',  quoting=csv.QUOTE_MINIMAL)
    writer.writerow(header_row)
    return writer


def stage_nodes(document_collection_name):

    with open(f'{config.get_graph_staging_dir(document_collection_name)}/{CORPUS_NODES}', mode='w') as f:
        writer = build_writer(f, ['id', 'organization', 'source_url', 'summary'])
        for corpus in load_corpus_metadata(config.get_corpus_metadata_filename()):
            if corpus.id == document_collection_name:
                writer.writerow([corpus.id, corpus.organization, corpus.source_url, corpus.summary])

    with open(f'{config.get_graph_staging_dir(document_collection_name)}/{DOCUMENT_NODES}', mode='w') as f:
        writer = build_writer(f, ['id', 'organization', 'local_filename', 'about_url', 'download_url', 'title', 'summary', 'year'])
        for document in load_document_metadata(config.get_document_metadata_filename(document_collection_name)):
            writer.writerow([document.id, document.organization, document.local_filename, document.about_url, document.download_url, document.title, document.summary, document.year.year])

    with open(f'{config.get_graph_staging_dir(document_collection_name)}/{PARAGRAPH_NODES}', mode='w') as f:
        writer = build_writer(f, ['id', 'page_number', 'paragraph_number', 'paragraph_len', 'text'])
        for document in load_document_metadata(config.get_document_metadata_filename(document_collection_name)):
            paragraph_metadata_filename = config.get_paragraph_metadata_filename(document_collection_name, document.local_filename)
            paragraphs = load_paragraph_metadata(paragraph_metadata_filename)
            for paragraph in paragraphs:
                writer.writerow([paragraph.id, paragraph.page_number, paragraph.paragraph_number, paragraph.paragraph_len, paragraph.raw_text])

    with open(f'{config.get_graph_staging_dir(document_collection_name)}/{SENTENCE_NODES}', mode='w') as f:
        writer = build_writer(f, ['id', 'text'])
        for document in load_document_metadata(config.get_document_metadata_filename(document_collection_name)):
            paragraph_metadata_filename = config.get_paragraph_metadata_filename(document_collection_name, document.local_filename)
            paragraphs = load_paragraph_metadata(paragraph_metadata_filename)
            for paragraph in paragraphs:
                for sentence in paragraph.sentences:
                    writer.writerow([sentence.id, sentence.text])

    #
    # Paragraph --> Mentions --> Entity is a little counterintuitive; The same entity many be mentioned in a paragraph multiple
    # times, and we want to record that data - however Tigergraph doesn't allow duplicate edges so every Paragraph-->Entity 
    # relationship has to 'flow through' a Mention node. 
    #
    with open(f'{config.get_graph_staging_dir(document_collection_name)}/{MENTION_NODES}', mode='w') as f:
        writer = build_writer(f, ['id'])
        for document in load_document_metadata(config.get_document_metadata_filename(document_collection_name)):
            paragraph_metadata_filename = config.get_paragraph_metadata_filename(document_collection_name, document.local_filename)
            paragraphs = load_paragraph_metadata(paragraph_metadata_filename)
            for paragraph in paragraphs:
                for entity in paragraph.entities:
                    writer.writerow([entity.mention_id])

    with open(f'{config.get_graph_staging_dir(document_collection_name)}/{ENTITY_NODES}', mode='w') as f:
        writer = build_writer(f, ['id' ,'text', 'type'])
        for document in load_document_metadata(config.get_document_metadata_filename(document_collection_name)):
            paragraph_metadata_filename = config.get_paragraph_metadata_filename(document_collection_name, document.local_filename)
            paragraphs = load_paragraph_metadata(paragraph_metadata_filename)
            for paragraph in paragraphs:
                for entity in paragraph.entities:
                    writer.writerow([entity.id, entity.text, entity.label])


    with open(f'{config.get_graph_staging_dir(document_collection_name)}/{SDG_NODES}', mode='w') as f:
        writer = build_writer(f, ['id' ,'text'])
        sdgs = {}
        for sdg in load_sdgs():
            sdgs[sdg.goal_category_num] = f'{sdg.goal_category_short}, {sdg.goal_category_long}'
            sdgs[sdg.goal_num] = f'{sdg.goal}'
        for (k,v) in sdgs.items():
             writer.writerow([k, v])



def stage_edges(document_collection_name):
    print('')


if __name__ == "__main__":
    main()
