from config import config

CORPUS_NODES = 'corpus_nodes' + config.GRAPH_EXTENSION
DOCUMENT_NODES = 'document_nodes' + config.GRAPH_EXTENSION
PARAGRAPH_NODES = 'paragraph_nodes' + config.GRAPH_EXTENSION
MENTION_NODES = 'mention_nodes' + config.GRAPH_EXTENSION
SENTENCE_NODES = 'sentence_nodes' + config.GRAPH_EXTENSION
ENTITY_NODES = 'entity_nodes' + config.GRAPH_EXTENSION
SDG_NODES = 'sdg_nodes' + config.GRAPH_EXTENSION

CORPUS_TO_DOCUMENT_EDGES = 'corpus_to_document_edges' + config.GRAPH_EXTENSION
DOCUMENT_TO_PARAGRAPH_EDGES = 'document_to_paragraph_edges' + config.GRAPH_EXTENSION
PARAGRAPH_TO_SENTENCE_EDGES = 'paragraph_to_sentence_edges' + config.GRAPH_EXTENSION
SENTENCE_TO_SDG_EDGES = 'sentence_to_sdg_edges' + config.GRAPH_EXTENSION
PARAGRAPH_TO_MENTION_EDGES = 'paragraph_to_mention_edges'  + config.GRAPH_EXTENSION
MENTION_TO_ENTITY_EDGES = 'mention_to_entity_edges' + config.GRAPH_EXTENSION