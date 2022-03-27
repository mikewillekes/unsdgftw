import os
import json
from dotenv import load_dotenv
import pyTigerGraph as tg

# Local application imports
from config import config
from graph import graph_config

load_dotenv()

# Connect and built schema
conn = tg.TigerGraphConnection(
    host=f'{os.environ.get("tg_host")}', 
    graphname=f'{config.GRAPH_NAME}', 
    apiToken=f'{os.environ.get("tg_token")}')

print(conn.echo())

def main():
    load_graph_data('UNICEF')


def load_graph_data(document_collection_name):

    load_file(document_collection_name, graph_config.CORPUS_NODES, 'load_job_corpus_nodes_csv')
    load_file(document_collection_name, graph_config.DOCUMENT_NODES, 'load_job_document_nodes_csv')
    load_file(document_collection_name, graph_config.PARAGRAPH_NODES, 'load_job_paragraph_nodes_csv')
    load_file(document_collection_name, graph_config.SENTENCE_NODES, 'load_job_sentence_nodes_csv')
    load_file(document_collection_name, graph_config.SDG_NODES, 'load_job_sdg_nodes_csv')
    load_file(document_collection_name, graph_config.MENTION_NODES, 'load_job_mention_nodes_csv')
    load_file(document_collection_name, graph_config.ENTITY_NODES, 'load_job_entity_nodes_csv')

    load_file(document_collection_name, graph_config.CORPUS_TO_DOCUMENT_EDGES, 'load_job_corpus_to_document_edges_csv')
    load_file(document_collection_name, graph_config.DOCUMENT_TO_PARAGRAPH_EDGES, 'load_job_document_to_paragraph_edges_csv')
    load_file(document_collection_name, graph_config.PARAGRAPH_TO_SENTENCE_EDGES, 'load_job_paragraph_to_sentence_edges_csv')
    load_file(document_collection_name, graph_config.SENTENCE_TO_SDG_EDGES, 'load_job_sentence_to_sdg_edges_csv')
    load_file(document_collection_name, graph_config.PARAGRAPH_TO_MENTION_EDGES, 'load_job_paragraph_to_mention_edges_csv')
    load_file(document_collection_name, graph_config.MENTION_TO_ENTITY_EDGES, 'load_job_mention_to_entity_edges_csv')

    # Note: Topic nodes and Edges are in the same CSV file
    load_file(document_collection_name, graph_config.TOPIC_NODES, 'load_job_topic_nodes_csv')
    load_file(document_collection_name, graph_config.TOPIC_NODES, 'load_job_paragraph_to_topic_edges_csv')


def load_file(document_collection_name, filename, tg_job_name):
    res = conn.uploadFile(
        f'{config.get_graph_staging_dir(document_collection_name)}/{filename}', 
        fileTag='MyDataSource',
        jobName=tg_job_name)
    print(json.dumps(res, indent=2))


def build_comention_edges():
    res = conn.runInstalledQuery('Build_Comention_Edges')
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
