from datetime import date
from serde import serialize, deserialize
from serde.json import from_json, to_json
from dataclasses import dataclass


@deserialize
@serialize
@dataclass
class DocumentMetadata:
    organization: str
    local_filename: str
    about_url: str
    download_url: str
    title: str
    summary: str
    year: date


def load_metadata(filename):
    # Deserialized from Jsonl file
    metadata = []
    with open(filename, 'r') as fp:
        for line in fp.readlines():
            metadata.append(from_json(DocumentMetadata, line.strip()))
    return metadata


def save_metadata(filename, metadata):
    # Serialize to json string & append newline
    lines = []
    for m in metadata:
        lines.append(to_json(m) + '\n')
    # Save to Jsonl file
    open(filename, 'w').writelines(lines)


docs = [
    DocumentMetadata(
        'iucn.org',
        'RL-267-001-En.pdf',
        'https://portals.iucn.org/library/node/49295',
        'https://portals.iucn.org/library/sites/library/files/documents/RL-267-001-En.pdf',
        'The conservation status of marine biodiversity of the Western Indian Ocean',
        'The Western Indian Ocean is comprised of productive and highly diverse marine ecosystems that are rich sources of food security, livelihoods, and natural wonder. The ecological services that species provide are vital to the productivity of these ecosystems and healthy biodiversity is essential for the continued support of economies and local users. The stability of these valuable resources, however, is being eroded by growing threats to marine life from overexploitation, habitat degradation and climate change, all of which are causing serious reductions in marine ecosystem services and the ability of these ecosystems to support human communities. Quantifying the impacts of these threats and understanding the conservation status of the region’s marine biodiversity is a critical step in applying informed management and conservation measures to mitigate loss and retain the ecological value of these systems. This report highlights trends in research needs for species in the region, including priorities for fundamental biological and ecological research and quantifying trends in the populations of species. The assessments and analyses submitted in this report should inform conservation decision-making processes and will be valuable to policymakers, natural resource managers, environmental planners and NGOs.',
        date(2021, 1, 1)
    ),
    DocumentMetadata(
        'iucn.org',
        'RL-267-001-En.pdf',
        'https://portals.iucn.org/library/node/49860',
        'https://portals.iucn.org/library/sites/library/files/documents/2021-043-En.pdf',
        'Gender and national climate planning',
        'This study aims to contribute to global and regional gender-climate policy data; enrich regional and national information to better target assistance to countries, their stakeholders and supporters; and inform more robust gender-responsive policymaking, knowledge and action at greater scales.',
        date(2021, 1, 1)
    ),
    DocumentMetadata(
        'iucn.org',
        '2021-034-En.pdf',
        'https://portals.iucn.org/library/node/49777',
        'https://portals.iucn.org/library/sites/library/files/documents/2021-034-En.pdf',
        'World Heritage forests : Carbon sinks under pressure',
        '',
        date(2021, 1, 1)
    ),
    DocumentMetadata(
        'iucn.org',
        '2021-035-En.pdf',
        'https://portals.iucn.org/library/node/49776',
        'https://portals.iucn.org/library/sites/library/files/documents/2021-035-En.pdf',
        'Acting on ocean risk : Documenting economic, social and environmental impacts on coastal communities',
        '',
        date(2021, 10, 29)
    ),

]


save_metadata('./corpus/IUCN/metadata.jsonl', docs)