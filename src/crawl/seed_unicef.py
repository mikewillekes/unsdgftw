from datetime import date

# Local application imports
from metadata.document_metadata import *
from config import config


document_collection_name = 'UNICEF'
filename = f'{config.CORPUS_DIR}/{document_collection_name}/{config.DOCUMENT_METADATA_FILENAME}'

save_document_metadata(filename, 
    [
        DocumentMetadata(
            generate_document_id('https://data.unicef.org/wp-content/uploads/2021/10/State-of-the-Worlds-Hand-Hygiene-report-2021.pdf'),
            'UNICEF',
            'unicef.org',
            'State-of-the-Worlds-Hand-Hygiene-report-2021.pdf',
            'https://data.unicef.org/resources/state-of-the-worlds-hand-hygiene/',
            'https://data.unicef.org/wp-content/uploads/2021/10/State-of-the-Worlds-Hand-Hygiene-report-2021.pdf',
            'State of the World\'s Hand Hygiene',
            'A global call to action to make hand hygiene a priority in policy and practice',
            date(2021, 10, 1)
        ),
        DocumentMetadata(
            generate_document_id('https://data.unicef.org/wp-content/uploads/2022/01/jmp-2021-wash-households_3.pdf'),
            'UNICEF',
            'unicef.org',
            'jmp-2021-wash-households_3.pdf',
            'https://data.unicef.org/resources/progress-on-household-drinking-water-sanitation-and-hygiene-2000-2020/',
            'https://data.unicef.org/wp-content/uploads/2022/01/jmp-2021-wash-households_3.pdf',
            'Progress on household drinking water, sanitation and hygiene, 2000-2020',
            'Five years into the SDGs',
            date(2021, 7, 1)
        )
    ]
)


