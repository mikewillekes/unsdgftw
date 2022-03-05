from datetime import date

# Local application imports
from metadata.corpus_metadata import *
from config import config
from metadata.corpus_metadata import CorpusMetadata


save_corpus_metadata(config.get_corpus_metadata_filename(),
    [
        CorpusMetadata(
            'IPBES',
            'The Intergovernmental Science-Policy Platform on Biodiversity and Ecosystem Services',
            'https://ipbes.net',
            'An independent intergovernmental body established by States to strengthen the science-policy interface for biodiversity and ecosystem services for the conservation and sustainable use of biodiversity, long-term human well-being and sustainable development.'
        ),
        CorpusMetadata(
            'IPCC',
            'The Intergovernmental Panel on Climate Change',
            'https://ipcc.ch',
            'The Intergovernmental Panel on Climate Change (IPCC) is the United Nations body for assessing the science related to climate change.'
        ),
        CorpusMetadata(
            'IUCN',
            'International Union for Conservation of Nature',
            'https://www.iucn.org',
            'IUCN is a membership Union composed of both government and civil society organisations. It harnesses the experience, resources and reach of its more than 1,400 Member organisations and the input of more than 18,000 experts. This diversity and vast expertise makes IUCN the global authority on the status of the natural world and the measures needed to safeguard it.'
        ),
        CorpusMetadata(
            'MA',
            'Millennium Ecosystem Assessment',
            'https://www.millenniumassessment.org',
            'The Millennium Ecosystem Assessment assessed the consequences of ecosystem change for human well-being. From 2001 to 2005, the MA involved the work of more than 1,360 experts worldwide. Their findings provide a state-of-the-art scientific appraisal of the condition and trends in the world’s ecosystems and the services they provide, as well as the scientific basis for action to conserve and use them sustainably.'
        ),
        CorpusMetadata(
            'OKR',
            'World Bank Group Open Knowledge Repository',
            'https://openknowledge.worldbank.org/',
            'The World Bank is the largest single source of development knowledge. The World Bank Open Knowledge Repository (OKR) is The World Bank’s official open access repository for its research outputs and knowledge products.'
        ),
        CorpusMetadata(
            'UNICEF',
            'UNICEF',
            'https://www.unicef.org/',
            'UNICEF works in over 190 countries and territories to save children\'s lives, to defend their rights, and to help them fulfil their potential, from early childhood through adolescence. And we never give up.'
        )
    ]
)