from datetime import date

# Local application imports
from metadata.document_metadata import *
from config import config


document_collection_name = 'MA'
filename = f'{config.CORPUS_DIR}/{document_collection_name}/{config.DOCUMENT_METADATA_FILENAME}'

save_document_metadata(filename, 
    [
        DocumentMetadata(
            generate_document_id('https://www.millenniumassessment.org/documents/document.429.aspx.pdf'),
            'MA',
            'Millennium Ecosystem Assessment (MA)',
            'document.429.aspx.pdf',
            'https://www.millenniumassessment.org/en/BoardStatement.html',
            'https://www.millenniumassessment.org/documents/document.429.aspx.pdf',
            'Living Beyond Our Means: Natural Assets and Human Well-being',
            'This statement was developed by the Board governing the MA process, whose membership includes representatives from U.N. organizations, governments through a number of international conventions, nongovernmental organizations, academia, business, and indigenous peoples.',
            date(2005, 1, 1)
        ),
        DocumentMetadata(
            generate_document_id('https://www.millenniumassessment.org/documents/document.356.aspx.pdf'),
            'MA',
            'Millennium Ecosystem Assessment (MA)',
            'document.356.aspx.pdf',
            'https://www.millenniumassessment.org/en/Synthesis.html',
            'https://www.millenniumassessment.org/documents/document.356.aspx.pdf',
            'Ecosystems and Human Well-being: General Synthesis',
            'This report presents a synthesis and integration of the findings of the four MA Working Groups along with more detailed findings for selected ecosystem services concerning condition and trends and scenarios, and response options.',
            date(2005, 1, 1)
        ),
        DocumentMetadata(
            generate_document_id('https://www.millenniumassessment.org/documents/document.354.aspx.pdf'),
            'MA',
            'Millennium Ecosystem Assessment (MA)',
            'document.354.aspx.pdf',
            'https://www.millenniumassessment.org/en/Synthesis.html',
            'https://www.millenniumassessment.org/documents/document.354.aspx.pdf',
            'Ecosystems and Human Well-being: Biodiversity Synthesis',
            'Prepared for the CBD, this report provides an overview of biodiversity across the assessment, organized around a set of 6 questions which were initially posed by the CBD to the MA.',
            date(2005, 1, 1)
        ),
        DocumentMetadata(
            generate_document_id('https://www.millenniumassessment.org/documents/document.282.aspx.pdf'),
            'MA',
            'Millennium Ecosystem Assessment (MA)',
            'document.282.aspx.pdf',
            'https://www.millenniumassessment.org/en/Condition.html',
            'https://www.millenniumassessment.org/documents/document.282.aspx.pdf',
            'Global Assessment Reports: Volume 1: Current State & Trends; Chapter 13. Air Quality and Climate',
            'The MA synthesized information from the scientific literature and relevant peer-reviewed datasets and models. It incorporated knowledge held by the private sector, practitioners, local communities, and indigenous peoples. The MA did not aim to generate new primary knowledge, but instead sought to add value to existing information by collating, evaluating, summarizing, interpreting, and communicating it in a useful form.',
            date(2005, 1, 1)
        )
    ]
)


