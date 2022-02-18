from spacy.matcher import PhraseMatcher

# Local application imports
from config import config


def initialize_phrase_matcher(nlp):
    # Initialize the matcher
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    patterns  = [nlp(phrase) for phrase in load_phrases()]
    matcher.add("MATCH_PHRASES", patterns)
    return matcher


def load_phrases():
    with open(config.MATCH_PHRASES_FILENAME, 'r') as fp:
        for line in fp:
            line = line.strip()
            if line[0] != '#':
                yield line