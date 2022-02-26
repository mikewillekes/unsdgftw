from datetime import date

# Local application imports
from metadata.corpus_metadata import *
from config import config
from metadata.corpus_metadata import CorpusMetadata


filename = f'{config.CORPUS_DIR}/{config.CORPUS_METADATA_FILENAME}'

save_corpus_metadata(filename, 
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
            'Millennium Ecosystem Assessment ',
            'https://www.millenniumassessment.org',
            'The Millennium Ecosystem Assessment assessed the consequences of ecosystem change for human well-being. From 2001 to 2005, the MA involved the work of more than 1,360 experts worldwide. Their findings provide a state-of-the-art scientific appraisal of the condition and trends in the world’s ecosystems and the services they provide, as well as the scientific basis for action to conserve and use them sustainably.'
        ),

    ]
)