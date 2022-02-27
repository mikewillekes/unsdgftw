from datetime import date

# Local application imports
from metadata.document_metadata import *
from config import config


document_collection_name = 'IUCN'
filename = f'{config.CORPUS_DIR}/{document_collection_name}/{config.DOCUMENT_METADATA_FILENAME}'

save_document_metadata(filename, 
    [
        DocumentMetadata(
            generate_document_id('https://portals.iucn.org/library/sites/library/files/documents/RL-267-001-En.pdf'),
            'IUCN',
            'iucn.org',
            'RL-267-001-En.pdf',
            'https://portals.iucn.org/library/node/49295',
            'https://portals.iucn.org/library/sites/library/files/documents/RL-267-001-En.pdf',
            'The conservation status of marine biodiversity of the Western Indian Ocean',
            'The Western Indian Ocean is comprised of productive and highly diverse marine ecosystems that are rich sources of food security, livelihoods, and natural wonder. The ecological services that species provide are vital to the productivity of these ecosystems and healthy biodiversity is essential for the continued support of economies and local users. The stability of these valuable resources, however, is being eroded by growing threats to marine life from overexploitation, habitat degradation and climate change, all of which are causing serious reductions in marine ecosystem services and the ability of these ecosystems to support human communities. Quantifying the impacts of these threats and understanding the conservation status of the region’s marine biodiversity is a critical step in applying informed management and conservation measures to mitigate loss and retain the ecological value of these systems. This report highlights trends in research needs for species in the region, including priorities for fundamental biological and ecological research and quantifying trends in the populations of species. The assessments and analyses submitted in this report should inform conservation decision-making processes and will be valuable to policymakers, natural resource managers, environmental planners and NGOs.',
            date(2021, 1, 1)
        ),
        DocumentMetadata(
            generate_document_id('https://portals.iucn.org/library/sites/library/files/documents/2021-043-En.pdf'),
            'IUCN',
            'iucn.org',
            '2021-043-En.pdf',
            'https://portals.iucn.org/library/node/49860',
            'https://portals.iucn.org/library/sites/library/files/documents/2021-043-En.pdf',
            'Gender and national climate planning',
            'This study aims to contribute to global and regional gender-climate policy data; enrich regional and national information to better target assistance to countries, their stakeholders and supporters; and inform more robust gender-responsive policymaking, knowledge and action at greater scales.',
            date(2021, 1, 1)
        ),
        DocumentMetadata(
            generate_document_id('https://portals.iucn.org/library/sites/library/files/documents/2021-034-En.pdf'),
            'IUCN',
            'iucn.org',
            '2021-034-En.pdf',
            'https://portals.iucn.org/library/node/49777',
            'https://portals.iucn.org/library/sites/library/files/documents/2021-034-En.pdf',
            'World Heritage forests : Carbon sinks under pressure',
            '',
            date(2021, 1, 1)
        ),
        DocumentMetadata(
            generate_document_id('https://portals.iucn.org/library/sites/library/files/documents/2021-035-En.pdf'),
            'IUCN',
            'iucn.org',
            '2021-035-En.pdf',
            'https://portals.iucn.org/library/node/49776',
            'https://portals.iucn.org/library/sites/library/files/documents/2021-035-En.pdf',
            'Acting on ocean risk : Documenting economic, social and environmental impacts on coastal communities',
            '',
            date(2021, 10, 29)
        ),
        DocumentMetadata(
            generate_document_id('https://portals.iucn.org/library/sites/library/files/documents/2020-002-En-Summ.pdf'),
            'IUCN',
            'iucn.org',
            '2020-002-En-Summ.pdf',
            'https://portals.iucn.org/library/node/49850',
            'https://portals.iucn.org/library/sites/library/files/documents/2020-002-En-Summ.pdf',
            'Gender-based violence and environment linkages : summary for policy makers',
            'This summary for policy makers synthesises key issues, findings and recommendations from IUCN\'s Gender-based violence and environment linkages: the violence of inequality (Castañeda et al., 2020). Bringing together existing and new evidence from across sectors and spheres, the publication serves as a robust reference for policy makers, researchers and programming and project practitioners at all levels to understand  interlinked issues and forge rights-based, gender-responsive interventions across environment-related contexts. It also informs environment-responsive gender equality interventions, especially those focused on eliminating gender-based violence.',
            date(2021, 12, 13)
        ),
        DocumentMetadata(
            generate_document_id('https://portals.iucn.org/library/sites/library/files/documents/2021-042-En.pdf'),
            'IUCN',
            'iucn.org',
            '2021-042-En.pdf',
            'https://portals.iucn.org/library/node/49846',
            'https://portals.iucn.org/library/sites/library/files/documents/2021-042-En.pdf',
            'Using ecosystem risk assessment science in ecosystem restoration : a guide to applying the Red List of Ecosystems to ecosystem restoration',
            'Recent global initiatives in ecosystem restoration offer an unprecedented opportunity to improve biodiversity conservation and human health and well-being. Ecosystems form a core component of biodiversity. They provide humans with multiple benefits - a stable climate and breathable air; water, food and materials; and protection from disaster and disease. Ecosystem restoration, as defined by the UN Decade on Ecosystem Restoration, includes a range of management interventions that aim to reduce impacts on and assist in the recovery of ecosystems that have been damaged, degraded or destroyed. This Guide promotes the application of the science of ecosystem risk assessment, which involves measuring the risk of ecosystem collapse, in ecosystem restoration. It explores how the IUCN Red List of Ecosystems and ecosystem restoration can be jointly deployed to reduce risk of ecosystem collapse.',
            date(2021, 12, 2)
        ),
        DocumentMetadata(
            generate_document_id('https://portals.iucn.org/library/sites/library/files/documents/2021-036-En.pdf'),
            'IUCN',
            'iucn.org',
            '2021-036-En.pdf',
            'https://portals.iucn.org/library/node/49779',
            'https://portals.iucn.org/library/sites/library/files/documents/2021-036-En.pdf',
            'Planning and delivering Nature-based Solutions in Mediterranean cities : First assessment of the IUCN NbS Global Standard in Mediterranean urban areas',
            '',
            date(2021, 11, 4)
        )
    ]
)


