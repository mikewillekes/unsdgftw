from datetime import date

# Local application imports
from metadata.document_metadata import *
from config import config


document_collection_name = 'IPBES'
filename = f'{config.CORPUS_DIR}/{document_collection_name}/{config.DOCUMENT_METADATA_FILENAME}'

save_document_metadata(filename, 
    [
        DocumentMetadata(
            'ipbes.net',
            'ipbes_assessment_report_ldra_EN.pdf',
            'https://zenodo.org/record/3237393',
            'https://zenodo.org/record/3237393/files/ipbes_assessment_report_ldra_EN.pdf?download=1',
            'The IPBES assessment report on land degradation and restoration',
            'The Assessment Report on Land Degradation and Restoration by the Intergovernmental Science-Policy Platform on Biodiversity and Ecosystem Services (IPBES) provides a critical analysis of the state of knowledge regarding the importance, drivers, status, and trends of terrestrial ecosystems. The Report recognizes that combatting land degradation, which is a pervasive, systemic phenomenon occurring in all parts of the world, is an urgent priority in order to protect the biodiversity and ecosystem services that are vital to all life on Earth and to ensure human well-being. The Report identifies a mix of governance options, policies and management practices that can help support stakeholders working at all levels to reduce the negative environmental, social and economic consequences of land degradation and to rehabilitate and restore degraded land. The Report encompasses all the terrestrial regions and biomes of the world, recognizing that land degradation drivers and processes can vary in severity within regions and countries as much as between them, and includes the full range of human-altered systems, including but not limited to drylands, agricultural and agroforestry systems, savannahs and forests and aquatic systems associated with these areas.',
            date(2018, 3, 24)
        ),
        DocumentMetadata(
            'ipbes.net',
            '202111_2020 IPBES GLOBAL REPORT_FULL_DIGITAL_NOV 2021.pdf',
            'https://zenodo.org/record/5657041',
            'https://zenodo.org/record/5657041/files/202111_2020%20IPBES%20GLOBAL%20REPORT_FULL_DIGITAL_NOV%202021.pdf?download=1',
            'Global assessment report on biodiversity and ecosystem services of the Intergovernmental Science-Policy Platform on Biodiversity and Ecosystem Services',
            'IPBES is to perform regular and timely assessments of knowledge on biodiversity and ecosystem services and their interlinkages at the global level. Also addressing an invitation by the Conference of the Parties of the Convention on Biological Diversity (CBD) to prepare a global assessment of biodiversity and ecosystem services building, inter alia, on its own and other relevant regional, subregional and thematic assessments, as well as on national reports.\nThe overall scope of the assessment is to assess the status and trends with regard to biodiversity and ecosystem services, the impact of biodiversity and ecosystem services on human well-being and the effectiveness of responses, including the Strategic Plan and its Aichi Biodiversity Targets. It is anticipated that this deliverable will contribute to the process for the evaluation and renewal of the Strategic Plan for Biodiversity and its Aichi Biodiversity Targets.\nThe IPBES Global Assessment on Biodiversity and Ecosystem Services is composed of 1) a Summary for Policymakers (SPM), approved by the IPBES Plenary at its 7th session in May 2019 in Paris, France (IPBES-7); and 2) a set of six Chapters, accepted by the IPBES Plenary.',
            date(2019, 5, 4)
        )
    ]
)


