"""Тесты для генерации синтетических наборов данных и нормализации импортируемых данных"""

import json

import pytest

from src.scripts import DataImporter, DataGenerator


def test_generated_dataset_meets_minimum_sizes_and_is_disjoint(tmp_path):
    counts = DataGenerator().generate_datasets(tmp_path)
    assert counts["knowledge_base_train"] >= 1000
    assert counts["knowledge_base_test"] >= 200
    assert counts["glossary"] >= 500

    train = json.loads((tmp_path / "knowledge_base_train.json").read_text(encoding="utf-8"))
    test = json.loads((tmp_path / "knowledge_base_test.json").read_text(encoding="utf-8"))
    glossary = json.loads((tmp_path / "glossary.json").read_text(encoding="utf-8"))
    assert {row["source_text"] for row in train}.isdisjoint({row["source_text"] for row in test})
    assert len({row["term"].casefold() for row in glossary}) == len(glossary)
    assert (tmp_path / "knowledge_base_train.csv").exists()
    assert (tmp_path / "knowledge_base_test.csv").exists()
    assert (tmp_path / "glossary.csv").exists()


def test_knowledge_records_are_deduplicated_case_insensitively():
    records = [
        {"source_text": "Profile A", "target_text": "Summary A", "category": "RPG"},
        {"source_text": " profile a ", "target_text": "Other summary", "category": "RPG"},
        {"source_text": "Profile B", "target_text": "Summary B"},
    ]
    result = DataImporter().normalize_knowledge_records(records)
    assert len(result) == 2
    assert result[0]["source_text"] == "Profile A"


def test_glossary_records_are_deduplicated_case_insensitively():
    records = [
        {"term": "MMR", "definition": "Rating"},
        {"term": "mmr", "definition": "Duplicate"},
    ]
    result = DataImporter().normalize_glossary_records(records)
    assert len(result) == 1
    assert result[0]["term"] == "MMR"


@pytest.mark.parametrize("records", [
    [{"source_text": "", "target_text": "summary"}],
    [{"source_text": "source", "target_text": "  "}],
])
def test_invalid_knowledge_records_raise(records):
    with pytest.raises(ValueError):
        DataImporter().normalize_knowledge_records(records)


def test_load_json_records_rejects_non_list(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text('{"not": "a list"}', encoding="utf-8")
    with pytest.raises(ValueError):
        DataImporter().load_json_records(path)


class _Scalars:
    def __init__(self, values):
        self._values = values

    def all(self):
        return self._values


class _Result:
    def __init__(self, values):
        self._values = values

    def scalars(self):
        return _Scalars(self._values)


class _FakeAsyncSession:
    def __init__(self, existing):
        self.existing = existing
        self.added = []
        self.commits = 0

    async def execute(self, _statement):
        return _Result(self.existing)

    def add_all(self, rows):
        self.added.extend(rows)

    async def commit(self):
        self.commits += 1


@pytest.mark.asyncio
async def test_import_knowledge_base_skips_existing_records():
    from src.backend.db import KnowledgeBase

    session = _FakeAsyncSession(["Already imported"])
    inserted = await DataImporter().import_knowledge_base(session, [
        {"source_text": "Already imported", "target_text": "Old summary"},
        {"source_text": "New profile", "target_text": "New summary"},
    ])
    assert inserted == 1
    assert len(session.added) == 1
    assert isinstance(session.added[0], KnowledgeBase)
    assert session.added[0].source_text == "New profile"
    assert session.commits == 1


@pytest.mark.asyncio
async def test_import_glossary_skips_existing_terms_case_insensitively():
    from src.backend.db import Glossary

    session = _FakeAsyncSession(["MMR"])
    inserted = await DataImporter().import_glossary(session, [
        {"term": "mmr", "definition": "Duplicate"},
        {"term": "Matchmaking", "definition": "Pair players"},
    ])
    assert inserted == 1
    assert len(session.added) == 1
    assert isinstance(session.added[0], Glossary)
    assert session.added[0].term == "Matchmaking"
    assert session.commits == 1
