from datetime import date
from serde import serialize, deserialize
from serde.json import from_json, to_json
from dataclasses import dataclass
import hashlib


@deserialize
@serialize
@dataclass
class DocumentMetadata:
    id: str
    corpus_id: str
    organization: str
    local_filename: str
    about_url: str
    download_url: str
    title: str
    summary: str
    year: date


def generate_document_id(download_url):
    """
        Generate a unique id for the document by normalizing and hashing 
        the download_url field. Of course since there is already a 
        DocumentMetadata class, there's probably a more pythonic
        way to do this with a class... but works for now.
    """
    s = download_url.lower()
    return hashlib.sha256(s.encode('utf-8')).hexdigest()


def load_document_metadata(filename):
    # Deserialized from Jsonl file
    metadata = []
    with open(filename, 'r') as fp:
        for line in fp.readlines():
            metadata.append(from_json(DocumentMetadata, line.strip()))
    return metadata


def save_document_metadata(filename, metadata):
    # Serialize to json string & append newline
    lines = []
    for m in metadata:
        lines.append(to_json(m) + '\n')
    # Save to Jsonl file
    open(filename, 'w').writelines(lines)
