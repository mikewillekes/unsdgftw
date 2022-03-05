from datetime import date

# Local application imports
from metadata.document_metadata import *
from config import config


document_collection_name = 'OKR'
filename = f'{config.CORPUS_DIR}/{document_collection_name}/{config.DOCUMENT_METADATA_FILENAME}'

save_document_metadata(filename, 
    [
        DocumentMetadata(
            generate_document_id('https://openknowledge.worldbank.org/bitstream/handle/10986/36912/9781464818127.pdf?sequence=2&isAllowed=y'),
            'OKR',
            'World Bank Group Open Knowledge Repository',
            '9781464818127.pdf',
            'https://openknowledge.worldbank.org/handle/10986/36912',
            'https://openknowledge.worldbank.org/bitstream/handle/10986/36912/9781464818127.pdf?sequence=2&isAllowed=y',
            'Blue Skies, Blue Seas : Air Pollution, Marine Plastics, and Coastal Erosion in the Middle East and North Africa',
            'This book shows how virtually all forms of natural capital, but particularly “blue” natural capital – skies and seas – has been degrading in the Middle East and North Africa (MENA) region over the last three decades, and focuses on the three challenges of air pollution, marine plastics, and coastal erosion.',
            date(2022, 2, 7)
        ),
        DocumentMetadata(
            generate_document_id('https://openknowledge.worldbank.org/bitstream/handle/10986/36945/9781464818172.pdf?sequence=7&isAllowed=y'),
            'OKR',
            'World Bank Group Open Knowledge Repository',
            '9781464818172.pdf',
            'https://openknowledge.worldbank.org/handle/10986/36945',
            'https://openknowledge.worldbank.org/bitstream/handle/10986/36945/9781464818172.pdf?sequence=7&isAllowed=y',
            'Women, Business and the Law 2022',
            'Women, Business and the Law 2022 is the eighth in a series of annual studies measuring the laws and regulations that affect women\'s economic opportunity in 190 economies. The project presents eight indicators structured around women\'s interactions with the law as they move through their careers: Mobility, Workplace, Pay, Marriage, Parenthood, Entrepreneurship, Assets, and Pension.',
            date(2022, 3, 1)
        )
    ]
)


