# Local application imports
from nlp.semantic_search import process_document_collection


def main():
    process_document_collection('IPBES')
    process_document_collection('IUCN')
    process_document_collection('IPCC')
    process_document_collection('MA')


if __name__ == "__main__":
    main()