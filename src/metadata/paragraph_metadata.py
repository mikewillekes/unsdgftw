from datetime import date
from serde import serialize, deserialize
from serde.json import from_json, to_json
from dataclasses import dataclass
from typing import List, Tuple

@deserialize
@serialize
@dataclass
class Entity:
    id: str
    text: str
    label: str


@deserialize
@serialize
@dataclass
class ParagraphMetadata:
    id: str
    document_id: str
    page_number: int
    paragraph_number: int
    paragraph_len: int
    clean_text: str
    raw_text: str
    sentences: List[str]
    entities: List[Entity]


def generate_paragraph_id(document_id, page_number, paragraph_number):
    """
        Generate a unique id for the paragraph.
    """
    return f'{document_id}.{page_number}.{paragraph_number}'


def load_paragraph_metadata(filename):
    # Deserialized from Jsonl file
    metadata = []
    with open(filename, 'r') as fp:
        for line in fp.readlines():
            metadata.append(from_json(ParagraphMetadata, line.strip()))
    return metadata


def save_paragraph_metadata(filename, metadata):
    # Serialize to json string & append newline
    lines = []
    for m in metadata:
        lines.append(to_json(m) + '\n')
    # Save to Jsonl file
    open(filename, 'w').writelines(lines)