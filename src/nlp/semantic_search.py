import re

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


def main():
    process_document_collection('IUCN')


def process_document_collection(document_collection_name):
    print(f'{document_collection_name}')
    document_metadata_filename = config.get_document_metadata_filename(document_collection_name)
    documents = load_document_metadata(document_metadata_filename)
    
    for document in documents:
        print(f'{document.local_filename}')
        nlp_metadata_filename = config.get_nlp_metadata_filename(document_collection_name, document.local_filename)
        save_nlp_metadata(nlp_metadata_filename, process_document(document_collection_name, document))


def process_document(document_collection_name, document):

    # For semantic similarty search we'll build a corpus of sentences and then 
    # match against collection of SDGs
    #
    # Build a collection of tuples (document, paragraph, sentence)

    sentence_corpus = list(build_sentence_corpus(document_collection_name, document))
    
    # Sentence embeddings for each sentence
    sentence_embeddings = embedder.encode(
        [s[2].text for s in sentence_corpus],
        convert_to_tensor=True)

    top_k = min(500, len(sentence_corpus))
    result = []

    # Query corpus from SDGs
    query_corpus = build_query_corpus()
    for query in query_corpus:

        # Encode the query sentence
        sdg_embedding = embedder.encode(query[1], convert_to_tensor=True)

        # We use cosine-similarity and torch.topk to find the highest scores
        cos_scores = util.cos_sim(sdg_embedding, sentence_embeddings)[0]
        top_results = torch.topk(cos_scores, k=top_k)
        
        print(f'{query[0]} {query[1]}')

        for score, index in zip(top_results[0], top_results[1]):
            if score > 0.5:
                document = sentence_corpus[index][0]
                paragraph = sentence_corpus[index][1]
                sentence = sentence_corpus[index][2] 
                result.append(NLPMetadata(
                    query[0],
                    query[1],
                    score.item(), # Its a single-item tensor
                    sentence.text,
                    sentence.id))

                #print("(Score: {:.4f})".format(score), document.local_filename, paragraph.entities, sentence)
    
    return result


def build_sentence_corpus(document_collection_name, document):
    paragraph_metadata_filename = config.get_paragraph_metadata_filename(document_collection_name, document.local_filename)
    paragraphs = load_paragraph_metadata(paragraph_metadata_filename)

    for paragraph in paragraphs:
        for sentence in paragraph.sentences:
            yield (document, paragraph, sentence)


def build_query_corpus():

    query_corpus={}
    sdgs = load_sdgs()

    for sdg in sdgs:
        query_corpus[sdg.goal_num] = clean_query_text(f'{sdg.goal}')

    return list(query_corpus.items())

    
def clean_query_text(s):
    clean = normalize_unicode(s)
    return remove_sdg_dates(clean)


def remove_sdg_dates(s):
    # Remove all the date references like "By 2030, " because it causes the model 
    # to find other matches by similar date - rather than just other semantic context
    return re.sub(r'([Bb]y )*([\d]){4},\s', '', s)


if __name__ == "__main__":
    main()