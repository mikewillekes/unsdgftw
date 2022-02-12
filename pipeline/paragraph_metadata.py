from datetime import date
from serde import serialize, deserialize
from serde.json import from_json, to_json
from dataclasses import dataclass


@deserialize
@serialize
@dataclass
class ParagraphMetadata:
    organization: str
    local_filename: str
    about_url: str
    download_url: str
    title: str
    summary: str
    year: date
    page_number: int
    paragraph_number: int
    paragraph_len: int
    clean_text: str
    raw_text: str


def load_metadata(filename):
    # Deserialized from Jsonl file
    metadata = []
    with open(filename, 'r') as fp:
        for line in fp.readlines():
            metadata.append(from_json(ParagraphMetadata, line.strip()))
    return metadata


def save_metadata(filename, metadata):
    # Serialize to json string & append newline
    lines = []
    for m in metadata:
        lines.append(to_json(m) + '\n')
    # Save to Jsonl file
    open(filename, 'w').writelines(lines)