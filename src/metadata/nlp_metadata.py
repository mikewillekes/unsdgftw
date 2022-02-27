from datetime import date
from serde import serialize, deserialize
from serde.json import from_json, to_json
from dataclasses import dataclass


@deserialize
@serialize
@dataclass
class NLPMetadata:
    sdg_id: str
    sdg_query: str
    similarity: float
    sentence: str
    sentence_id: str


def load_nlp_metadata(filename):
    # Deserialized from Jsonl file
    metadata = []
    with open(filename, 'r') as fp:
        for line in fp.readlines():
            metadata.append(from_json(NLPMetadata, line.strip()))
    return metadata


def save_nlp_metadata(filename, metadata):
    # Serialize to json string & append newline
    lines = []
    for m in metadata:
        lines.append(to_json(m) + '\n')
    # Save to Jsonl file
    open(filename, 'w').writelines(lines)