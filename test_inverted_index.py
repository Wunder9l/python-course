import inverted_index_starter as ins
import os


def test_simple_load_documents():
    docs = ins.load_documents('test_data/some_documents')
    assert isinstance(docs, list)
    assert len(docs) == 4
    assert all(isinstance(d, ins.Document) for d in docs)


def test_simple_build_inverted_index():
    docs = ins.load_documents('test_data/some_documents')
    index = ins.build_inverted_index(docs)
    assert isinstance(index, ins.InvertedIndex)


def test_oneword_query_of_inverted_index():
    docs = ins.load_documents('test_data/some_documents')
    index = ins.build_inverted_index(docs)
    assert index.query(['apple']) == [1]
    assert index.query(['orange']) == [1, 2]
    assert index.query(['are']) == [1, 7]
    assert index.query(['unpredicted']) == []


def test_multiword_query_of_inverted_index():
    docs = ins.load_documents('test_data/some_documents')
    index = ins.build_inverted_index(docs)
    assert index.query(['apple', 'banana']) == [1]
    assert index.query(['orange', 'monkey']) == []
    assert index.query(['are']) == [1, 7]
    assert index.query(['are', 'fruits']) == [1]
    assert index.query(['are', 'fruits', 'friends']) == []


def test_dump_load():
    docs = ins.load_documents('test_data/some_documents')
    index = ins.build_inverted_index(docs)
    dump_filename = 'test_data/tmp_test_dump_load'
    index.dump(dump_filename)
    index2 = ins.InvertedIndex.load(dump_filename)
    os.remove(dump_filename)
    assert index.query(['apple']) == index2.query(['apple'])
    assert index.query(['orange']) == index2.query(['orange'])
    assert index.query(['are']) == index2.query(['are'])
    assert index.query(['unpredicted']) == index2.query(['unpredicted'])
