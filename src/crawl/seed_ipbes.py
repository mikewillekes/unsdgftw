from datetime import date

# Local application imports
from metadata.document_metadata import *
from config import config


document_collection_name = 'IPBES'
filename = f'{config.CORPUS_DIR}/{document_collection_name}/{config.DOCUMENT_METADATA_FILENAME}'

save_document_metadata(filename, 
    [
        DocumentMetadata(
            generate_document_id('https://zenodo.org/record/6417333/files/202206_IPBES%20GLOBAL%20REPORT_FULL_DIGITAL_MARCH%202022.pdf?download=1'),
            'IPBES',
            'ipbes.net',
            '202111_2020 IPBES GLOBAL REPORT_FULL_DIGITAL_NOV 2021.pdf',
            'https://ipbes.net/global-assessment',
            'https://zenodo.org/record/6417333/files/202206_IPBES%20GLOBAL%20REPORT_FULL_DIGITAL_MARCH%202022.pdf?download=1',
            'Global Assessment Report on Biodiversity and Ecosystem Services',
            'IPBES is to perform regular and timely assessments of knowledge on biodiversity and ecosystem services and their interlinkages at the global level. Also addressing an invitation by the Conference of the Parties of the Convention on Biological Diversity (CBD) to prepare a global assessment of biodiversity and ecosystem services building, inter alia, on its own and other relevant regional, subregional and thematic assessments, as well as on national reports. The overall scope of the assessment is to assess the status and trends with regard to biodiversity and ecosystem services, the impact of biodiversity and ecosystem services on human well-being and the effectiveness of responses, including the Strategic Plan and its Aichi Biodiversity Targets. It is anticipated that this deliverable will contribute to the process for the evaluation and renewal of the Strategic Plan for Biodiversity and its Aichi Biodiversity Targets. The IPBES Global Assessment on Biodiversity and Ecosystem Services is composed of 1) a Summary for Policymakers (SPM), approved by the IPBES Plenary at its 7th session in May 2019 in Paris, France (IPBES-7); and 2) a set of six Chapters, accepted by the IPBES Plenary.',
            datetime(2019, 5, 4)
        ),
        DocumentMetadata(
            generate_document_id('https://ipbes.net/sites/default/files/downloads/pdf/2016.methodological_assessment_report_scenarios_models.pdf'),
            'IPBES',
            'ipbes.net',
            '2016.methodological_assessment_report_scenarios_models.pdf',
            'https://ipbes.net/assessment-reports/scenarios',
            'https://ipbes.net/sites/default/files/downloads/pdf/2016.methodological_assessment_report_scenarios_models.pdf',
            'Scenarios and Models of Biodiversity and Ecosystem Services',
            'The Scenarios and Models Assessment, published in 2016, presents a best-practice "toolkit" for the use of scenarios and models in decision-making on biodiversity, human-nature relationships, and the quality of life. The "toolkit" helps governments, private sector, and civil society to anticipate change - such as the loss of habitats, invasive alien species, and climate shifts - to reduce the negative impacts on people and to make use of important opportunities.',
            datetime(2016, 2, 1)
        ),
        DocumentMetadata(
            generate_document_id('https://ipbes.net/sites/default/files/2018_americas_full_report_book_v5_pages_0.pdf'),
            'IPBES',
            'ipbes.net',
            '2018_americas_full_report_book_v5_pages_0.pdf',
            'https://ipbes.net/assessment-reports/americas',
            'https://ipbes.net/sites/default/files/2018_americas_full_report_book_v5_pages_0.pdf',
            'Regional Assessment Report on Biodiversity and Ecosystem Services for the Americas',
            'The region\'s rich biodiversity and its benefits to people provide essential contributions to the economy, livelihoods, the quality of life and the eradication of poverty. The region is also bioculturally diverse, with traditional knowledge of indigenous people and local communities promoting, among other things, the diversification and conservation of many varieties of cultivated plants and domestic animals that are the staple foods of many other regions of the world. The region has successful experiences in biodiversity conservation, restoration and sustainable use, including some carried out by indigenous people and local communities. On the other hand, climate change, population growth and the consequent increase in demand for food, biomass and energy continue to have a serious impact on biodiversity and ecosystem services and functions. These impacts are felt not only in terrestrial ecosystems, but also in wetlands, freshwater, coastal and marine ecosystems. In some areas of the Americas, the degree of these impacts on biodiversity and ecosystem services and functions is threatening the economy, livelihoods and quality of life.',
            datetime(2018, 3, 1)
        ),
        DocumentMetadata(
            generate_document_id('https://ipbes.net/sites/default/files/africa_assessment_report_20181219_0.pdf'),
            'IPBES',
            'ipbes.net',
            'africa_assessment_report_20181219_0.pdf',
            'https://ipbes.net/assessment-reports/africa',
            'https://ipbes.net/sites/default/files/africa_assessment_report_20181219_0.pdf',
            'Regional Assessment Report on Biodiversity and Ecosystem Services for Africa',
            'Within the generic scope for the Regional Assessments of Biodiversity and Ecosystem Services, the African assessment focusses on thematic priorities, including the food-energy-water-livelihood nexus; land degradation, including climate-related risks such as desertification and silting; catchment to coast; biodiversity conservation and sustainable use; and invasive alien species. The assessment also addresses a number of cross-cutting themes.',
            datetime(2018, 3, 1)
        ),
        DocumentMetadata(
            generate_document_id('https://ipbes.net/sites/default/files/2018_asia_pacific_full_report_book_v3_pages.pdf'),
            'IPBES',
            'ipbes.net',
            '2018_asia_pacific_full_report_book_v3_pages.pdf',
            'https://ipbes.net/assessment-reports/asia-pacific',
            'https://ipbes.net/sites/default/files/2018_asia_pacific_full_report_book_v3_pages.pdf',
            'Regional Assessment Report on Biodiversity and Ecosystem Services for Asia and the Pacific',
            'Within the generic scope of the Regional Assessments of Biodiversity and Ecosystem Services, particular challenges found across the Asia-Pacific region include climate change (particularly sea-level rise, increased intensity of extreme storm events, ocean acidification and glacier retreat), population growth, poverty, human consumption of natural resources, land degradation, deforestation, invasive alien species, the impact of trade (including the illegal trade in wildlife and non-timber forest products), rapid urbanization, coastal pollution, poor governance of natural resources and the impact of altered fire regimes. These factors, together with others that have an impact on biodiversity and ecosystem services, are considered in the Assessment. There are also positive trends, such as an increase in awareness, forest cover and protected areas and a reduction in the region\'s carbon footprint. Issues specific to particular Asia-Pacific subregions are also addressed, for example the interplay between food, water and energy security; biodiversity and livelihoods; waste management; and cooperative management of critical ecosystems shared by more than one country.',
            datetime(2018, 3, 1)
        ),
        DocumentMetadata(
            generate_document_id('https://ipbes.net/sites/default/files/2018_eca_full_report_book_v5_pages_0.pdf'),
            'IPBES',
            'ipbes.net',
            '2018_eca_full_report_book_v5_pages_0.pdf',
            'https://ipbes.net/assessment-reports/eca',
            'https://ipbes.net/sites/default/files/2018_eca_full_report_book_v5_pages_0.pdf',
            'Regional Assessment Report on Biodiversity and Ecosystem Services for Europe and Central Asia',
            'Within the generic scope of the Regional Assessments of Biodiversity and Ecosystem Services, the key policy-relevant questions of the Europe and Central Asia Assessment concern options and opportunities with regard to biodiversity and ecosystem services and their role for human well-being. The assessment examines the opportunities for sectoral policies and policy instruments; managing production, consumption and economic development; and ecological infrastructures and ecological technologies. It explores opportunities to promote food security, economic development and equality while avoiding land and aquatic degradation and conserving cultural landscapes.',
            datetime(2018, 3, 1)
        ),
        DocumentMetadata(
            generate_document_id('https://ipbes.net/sites/default/files/2018_ldr_full_report_book_v4_pages.pdf'),
            'IPBES',
            'ipbes.net',
            '2018_ldr_full_report_book_v4_pages.pdf',
            'https://ipbes.net/assessment-reports/ldr',
            'https://ipbes.net/sites/default/files/2018_ldr_full_report_book_v4_pages.pdf',
            'Assessment Report on Land Degradation and Restoration',
            'The assessment of land degradation and restoration covers the global status of and trends in land degradation, by region and land cover type; the effect of degradation on biodiversity values, ecosystem services and human well-being; and the state of knowledge, by region and land cover type, of ecosystem restoration extent and options. The assessment aims to enhance the knowledge base for policies for addressing land degradation, desertification and the restoration of degraded land.',
            datetime(2018, 3, 1)
        ),
        DocumentMetadata(
            generate_document_id('https://ipbes.net/sites/default/files/downloads/pdf/2017_pollination_full_report_book_v12_pages.pdf'),
            'IPBES',
            'ipbes.net',
            '2017_pollination_full_report_book_v12_pages.pdf',
            'https://ipbes.net/assessment-reports/pollinators',
            'https://ipbes.net/sites/default/files/downloads/pdf/2017_pollination_full_report_book_v12_pages.pdf',
            'Assessment Report on Pollinators, Pollination and Food Production',
            'The assessment of land degradation and restoration covers the global status of and trends in land degradation, by region and land cover type; the effect of degradation on biodiversity values, ecosystem services and human well-being; and the state of knowledge, by region and land cover type, of ecosystem restoration extent and options. The assessment aims to enhance the knowledge base for policies for addressing land degradation, desertification and the restoration of degraded land.',
            datetime(2016, 2, 1)
        )
    ]
)


