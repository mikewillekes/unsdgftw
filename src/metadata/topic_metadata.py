from datetime import date
from serde import serialize, deserialize
from serde.json import from_json, to_json
from dataclasses import dataclass
from typing import List


@deserialize
@serialize
@dataclass
class TopicMetadata:
    id: str
    topic_number: int
    topic_probability: float
    terms: List[str]
    paragraph_id: str
    paragraph_clean_text: str


def load_topic_metadata(filename):
    # Deserialized from Jsonl file
    metadata = []
    with open(filename, 'r') as fp:
        for line in fp.readlines():
            metadata.append(from_json(TopicMetadata, line.strip()))
    return metadata


def save_topic_metadata(filename, metadata):
    # Serialize to json string & append newline
    lines = []
    for m in metadata:
        lines.append(to_json(m) + '\n')
    # Save to Jsonl file
    open(filename, 'w').writelines(lines)