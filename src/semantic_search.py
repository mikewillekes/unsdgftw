# Local application imports
from metadata.document_metadata import *
from metadata.paragraph_metadata import *
from config import config
from sdgs.sustainable_development_goals import *
import re
from sentence_transformers import SentenceTransformer,util
import torch

embedder = SentenceTransformer('all-MiniLM-L6-v2')

document_collection_name = 'MA'

document_metadata_filename = config.get_document_metadata_filename(document_collection_name)
documents = load_document_metadata(document_metadata_filename)

corpus = []    
for document in documents:
    paragraph_metadata_filename = config.get_paragraph_metadata_filename(document_collection_name, document.local_filename)
    paragraphs = load_paragraph_metadata(paragraph_metadata_filename)
    for paragraph in paragraphs:
        for sentence in paragraph.sentences:
          corpus.append((document, paragraph, sentence))

sentences = [c[2] for c in corpus]
corpus_embeddings = embedder.encode(sentences, convert_to_tensor=True)

top_k = min(500, len(corpus))

sdgs = load_sdgs()

for sdg in sdgs:
    #goal_sentence = f'{sdg.goal}'
    #goal_sentence = f'{sdg.goal_category_short}, {sdg.goal_category_long}, {sdg.goal}'
    goal_sentence = f'{sdg.goal_category_short}, {sdg.goal_category_long}'
    

    # Remove all the date references like "By 2030, " because it causes the model 
    # to find other matches by similar date
    goal_sentence = re.sub(r'([Bb]y )*([\d]){4},\s', '', goal_sentence)
    sdg_embedding = embedder.encode(goal_sentence, convert_to_tensor=True)

    # We use cosine-similarity and torch.topk to find the highest 5 scores
    cos_scores = util.cos_sim(sdg_embedding, corpus_embeddings)[0]
    top_results = torch.topk(cos_scores, k=top_k)
    
    print("\n\n======================\n\n")
    print("SDG:", goal_sentence)

    for score, index in zip(top_results[0], top_results[1]):
        if score > 0.5:
            document = corpus[index][0]
            paragraph = corpus[index][1]
            sentence = corpus[index][2]    
            print("(Score: {:.4f})".format(score), document.local_filename, paragraph.entities, sentence)

    print('\n\n')