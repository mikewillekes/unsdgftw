from datetime import date

# Local application imports
from metadata.document_metadata import *
from config import config


document_collection_name = 'IPCC'
filename = f'{config.CORPUS_DIR}/{document_collection_name}/{config.DOCUMENT_METADATA_FILENAME}'

save_document_metadata(filename, 
    [
        DocumentMetadata(
            generate_document_id('https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_Full_Report.pdf'),
            'ipcc.ch',
            'IPCC_AR6_WGI_Full_Report.pdf',
            'https://www.ipcc.ch/report/ar6/wg1/',
            'https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_Full_Report.pdf',
            'Climate Change 2021 The Physical Science Basis',
            'The Working Group I contribution to the Sixth Assessment Report addresses the most up-to-date physical understanding of the climate system and climate change, bringing together the latest advances in climate science, and combining multiple lines of evidence from paleoclimate, observations, process understanding, and global and regional climate simulations.',
            date(2021, 1, 1)
        )
    ]
)


