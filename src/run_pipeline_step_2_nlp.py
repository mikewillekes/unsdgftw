# Local application imports
from nlp.semantic_search import process_document_collection
from nlp.semantic_topics import process_document_collections

def main():

    # Sentence to SDG similarity
    process_document_collection('IPBES')
    process_document_collection('IUCN')
    process_document_collection('IPCC')
    process_document_collection('MA')
    process_document_collection('OKR')
    process_document_collection('UNICEF')

    # Semantic topic modelleing with BERTopic
    process_document_collections(['IPBES', 'IPCC', 'IUCN', 'MA', 'OKR', 'UNICEF'])

if __name__ == "__main__":
    main()