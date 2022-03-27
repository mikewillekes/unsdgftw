import csv

# Local application imports
from metadata.corpus_metadata import *
from metadata.document_metadata import *
from metadata.paragraph_metadata import *
from metadata.nlp_metadata import *
from metadata.topic_metadata import *
from config import config
from graph import graph_config
from sdgs.sustainable_development_goals import *


def main():
    stage_graph_data('UNICEF')


def stage_graph_data(document_collection_name):
    stage_nodes(document_collection_name)
    stage_edges(document_collection_name)


def build_writer(f, header_row):
    writer = csv.writer(f, delimiter=',', quotechar='"',  quoting=csv.QUOTE_MINIMAL)
    # There's a bug where pyTigerGraph loading jobs are not skipping header rows
    # even with  USING header="true" - so temporarily disable writing header rows.
    #
    # https://dev.tigergraph.com/forum/t/why-does-a-load-job-load-table-headers-as-nodes-into-the-database/1744/2
    #
    # writer.writerow(header_row)
    return writer


def stage_nodes(document_collection_name):

    with open(f'{config.get_graph_staging_dir(document_collection_name)}/{graph_config.CORPUS_NODES}', mode='w') as f:
        writer = build_writer(f, ['id', 'organization', 'sourceURL', 'summary'])
        for corpus in load_corpus_metadata(config.get_corpus_metadata_filename()):
            if corpus.id == document_collection_name:
                writer.writerow([corpus.id, corpus.organization, corpus.source_url, corpus.summary])

    with open(f'{config.get_graph_staging_dir(document_collection_name)}/{graph_config.DOCUMENT_NODES}', mode='w') as f:
        writer = build_writer(f, ['id', 'organization', 'localFilename', 'aboutURL', 'downloadURL', 'title', 'summary', 'year'])
        for document in load_document_metadata(config.get_document_metadata_filename(document_collection_name)):
            writer.writerow([document.id, document.organization, document.local_filename, document.about_url, document.download_url, document.title, document.summary, document.year.year])

    with open(f'{config.get_graph_staging_dir(document_collection_name)}/{graph_config.PARAGRAPH_NODES}', mode='w') as f:
        writer = build_writer(f, ['id', 'pageNumber', 'paragraphNumber', 'paragraphLength', 'text'])
        for document in load_document_metadata(config.get_document_metadata_filename(document_collection_name)):
            paragraph_metadata_filename = config.get_paragraph_metadata_filename(document_collection_name, document.local_filename)
            paragraphs = load_paragraph_metadata(paragraph_metadata_filename)
            for paragraph in paragraphs:
                writer.writerow([paragraph.id, paragraph.page_number, paragraph.paragraph_number, paragraph.paragraph_len, paragraph.raw_text])

    with open(f'{config.get_graph_staging_dir(document_collection_name)}/{graph_config.SENTENCE_NODES}', mode='w') as f:
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
    with open(f'{config.get_graph_staging_dir(document_collection_name)}/{graph_config.MENTION_NODES}', mode='w') as f:
        writer = build_writer(f, ['id'])
        for document in load_document_metadata(config.get_document_metadata_filename(document_collection_name)):
            paragraph_metadata_filename = config.get_paragraph_metadata_filename(document_collection_name, document.local_filename)
            paragraphs = load_paragraph_metadata(paragraph_metadata_filename)
            for paragraph in paragraphs:
                for entity in paragraph.entities:
                    writer.writerow([entity.mention_id])

    with open(f'{config.get_graph_staging_dir(document_collection_name)}/{graph_config.ENTITY_NODES}', mode='w') as f:
        writer = build_writer(f, ['id' ,'text', 'type'])
        for document in load_document_metadata(config.get_document_metadata_filename(document_collection_name)):
            paragraph_metadata_filename = config.get_paragraph_metadata_filename(document_collection_name, document.local_filename)
            paragraphs = load_paragraph_metadata(paragraph_metadata_filename)
            for paragraph in paragraphs:
                for entity in paragraph.entities:
                    # the 0 at the end is a placeholder for the lid ("label-id") that will
                    # be calculated later via label propagation community detection algorithm
                    writer.writerow([entity.id, entity.text, entity.label, 0])


    with open(f'{config.get_graph_staging_dir(document_collection_name)}/{graph_config.SDG_NODES}', mode='w') as f:
        writer = build_writer(f, ['id' ,'text'])
        sdgs = {}
        for sdg in load_sdgs():
            sdgs[sdg.goal_category_num] = f'{sdg.goal_category_short}, {sdg.goal_category_long}'
            sdgs[sdg.goal_num] = f'{sdg.goal}'
        for (k,v) in sdgs.items():
            # the 0 at the end is a placeholder for the lid ("label-id") that will
            # be calculated later via label propagation community detection algorithm
            writer.writerow([k, v, 0])


    with open(f'{config.get_graph_staging_dir(document_collection_name)}/{graph_config.TOPIC_NODES}', mode='w') as f:
        writer = build_writer(f, ['paragraph', 'id', 'probability', 'topic', 'term1', 'term2', 'term3', 'term4', 'term5', 'term6', 'term7', 'term8', 'term9', 'term10'])
        for topic in load_topic_metadata(config.get_topic_metadata_filename(document_collection_name)):
            # the 0 at the end is a placeholder for the lid ("label-id") that will
            # be calculated later via label propagation community detection algorithm
            row = list([topic.paragraph_id, topic.id, topic.topic_probability, topic.topic_number, 0])
            row.extend([t for t in topic.terms])
            writer.writerow(row)



def stage_edges(document_collection_name):

    with open(f'{config.get_graph_staging_dir(document_collection_name)}/{graph_config.CORPUS_TO_DOCUMENT_EDGES}', mode='w') as f:
        writer = build_writer(f, ['corpus', 'document'])
        for document in load_document_metadata(config.get_document_metadata_filename(document_collection_name)):
            writer.writerow([document.corpus_id, document.id])

    with open(f'{config.get_graph_staging_dir(document_collection_name)}/{graph_config.DOCUMENT_TO_PARAGRAPH_EDGES}', mode='w') as f:
        writer = build_writer(f, ['document', 'paragraph'])
        for document in load_document_metadata(config.get_document_metadata_filename(document_collection_name)):
            paragraph_metadata_filename = config.get_paragraph_metadata_filename(document_collection_name, document.local_filename)
            for paragraph in load_paragraph_metadata(paragraph_metadata_filename):
                for sentence in paragraph.sentences:
                    writer.writerow([paragraph.document_id, paragraph.id])

    with open(f'{config.get_graph_staging_dir(document_collection_name)}/{graph_config.PARAGRAPH_TO_SENTENCE_EDGES}', mode='w') as f:
        writer = build_writer(f, ['paragraph', 'sentence'])
        for document in load_document_metadata(config.get_document_metadata_filename(document_collection_name)):
            paragraph_metadata_filename = config.get_paragraph_metadata_filename(document_collection_name, document.local_filename)
            for paragraph in load_paragraph_metadata(paragraph_metadata_filename):
                for sentence in paragraph.sentences:
                    writer.writerow([paragraph.id, sentence.id])

    with open(f'{config.get_graph_staging_dir(document_collection_name)}/{graph_config.SENTENCE_TO_SDG_EDGES}', mode='w') as f:
        writer = build_writer(f, ['sentence', 'sdg', 'similarity'])
        for document in load_document_metadata(config.get_document_metadata_filename(document_collection_name)):
            nlp_metadata_filename = config.get_nlp_metadata_filename(document_collection_name, document.local_filename)
            for record in load_nlp_metadata(nlp_metadata_filename):
                writer.writerow([record.sentence_id, record.sdg_id, record.similarity])

    with open(f'{config.get_graph_staging_dir(document_collection_name)}/{graph_config.PARAGRAPH_TO_MENTION_EDGES}', mode='w') as f:
        writer = build_writer(f, ['paragraph', 'mention'])
        for document in load_document_metadata(config.get_document_metadata_filename(document_collection_name)):
            paragraph_metadata_filename = config.get_paragraph_metadata_filename(document_collection_name, document.local_filename)
            for paragraph in load_paragraph_metadata(paragraph_metadata_filename):
                for entity in paragraph.entities:
                    writer.writerow([paragraph.id, entity.mention_id])

    with open(f'{config.get_graph_staging_dir(document_collection_name)}/{graph_config.MENTION_TO_ENTITY_EDGES}', mode='w') as f:
        writer = build_writer(f, ['mention', 'entity'])
        for document in load_document_metadata(config.get_document_metadata_filename(document_collection_name)):
            paragraph_metadata_filename = config.get_paragraph_metadata_filename(document_collection_name, document.local_filename)
            for paragraph in load_paragraph_metadata(paragraph_metadata_filename):
                for entity in paragraph.entities:
                    writer.writerow([entity.mention_id, entity.id])

if __name__ == "__main__":
    main()
