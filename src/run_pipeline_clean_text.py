# Local application imports
from clean.clean_text import clean_document_collection


def main():
    clean_document_collection('IPBES')
    clean_document_collection('IUCN')
    clean_document_collection('IPCC')
    clean_document_collection('MA')


if __name__ == "__main__":
    main()