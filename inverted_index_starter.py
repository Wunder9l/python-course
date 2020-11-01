from collections import namedtuple, defaultdict
from functools import reduce
import json

Document = namedtuple('Document', ['id', 'text'])


class InvertedIndex:
    def query(self, words: list) -> list:
        """Return the list of relevant documents for the given query"""
        results = []
        for word in words:
            results.append(self.index.get(word, set()))
        if not results:
            return list()
        return list(reduce(lambda x, y: x & y, results[1:], results[0]))

    def __init__(self, documents: [Document]):
        self.index = defaultdict(set)
        for doc_id, text in documents:
            doc_id = int(doc_id)
            for word in text.split():
                if not word:
                    continue
                self.index[word].add(doc_id)

    def dump(self, filepath: str):
        with open(filepath, 'w') as f:
            to_dump_obj = {k: list(v) for k, v in self.index.items()}
            f.write(json.dumps(to_dump_obj, indent=2))

    @classmethod
    def load(cls, filepath: str):
        with open(filepath, 'r') as f:
            loaded_obj = json.loads(f.read())
            index = InvertedIndex([])
            index.index = defaultdict()
            for k, v in loaded_obj.items():
                index.index[k] = set(v)
            return index


def load_documents(filepath: str) -> [Document]:
    with open(filepath) as f:
        documents = []
        for line in f.readlines():
            id, _, text = line.partition('\t')
            documents.append(Document(id, text))
        return documents


def build_inverted_index(documents: [Document]) -> InvertedIndex:
    return InvertedIndex(documents)


def main():
    documents = load_documents("/path/to/dataset")
    inverted_index = build_inverted_index(documents)
    inverted_index.dump("/path/to/inverted.index")
    inverted_index = InvertedIndex.load("/path/to/inverted.index")
    document_ids = inverted_index.query(["two", "words"])


if __name__ == "__main__":
    main()
