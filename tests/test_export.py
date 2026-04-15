"""Tests for the export APIs added in 0.2.0 (issue #1)."""
import os
import pytest

from tmdlparser import TMLDParser
from tmdlparser.data_model import TMDL


SAMPLE_TMDL = """\
/// Sample table description
table SampleTable
\tlineageTag: 00000000-0000-0000-0000-000000000001
\t/// First column description
\tcolumn Amount
\t\tlineageTag: 00000000-0000-0000-0000-000000000002
\t\tsummarizeBy: sum
\t\tsourceColumn: amount
\t/// Second column description
\tcolumn Label
\t\tlineageTag: 00000000-0000-0000-0000-000000000003
\t\tsummarizeBy: none
\t\tsourceColumn: label
"""


@pytest.fixture(scope="module")
def synthetic_pbip(tmp_path_factory):
    """Build a minimal synthetic .pbip project tree in a tmp dir.

    The parser does not open the .pbip file itself; it only uses its name
    to derive the adjacent ``<name>.SemanticModel/definition/tables``
    directory. So we just need that directory populated with at least one
    .tmdl file.
    """
    root = tmp_path_factory.mktemp("pbip_project")
    (root / "sample.pbip").write_text("", encoding="utf-8")
    tables_dir = root / "sample.SemanticModel" / "definition" / "tables"
    tables_dir.mkdir(parents=True)
    (tables_dir / "SampleTable.tmdl").write_text(SAMPLE_TMDL, encoding="utf-8")
    return str(root / "sample.pbip")


@pytest.fixture(scope="module")
def parser(synthetic_pbip):
    p = TMLDParser(synthetic_pbip)
    p.parse_all_tables()
    return p


def test_tmdl_to_dict_recursive():
    inner = TMDL.create(description="d2", element="e2", properties=["p"], calculation="c2")
    outer = TMDL.create(description="d1", element="e1", properties=[inner], calculation="c1")

    result = outer.to_dict()

    assert result["element"] == "e1"
    assert result["description"] == "d1"
    assert result["calculation"] == "c1"
    assert isinstance(result["properties"], list)
    assert result["properties"][0]["element"] == "e2"
    assert result["properties"][0]["properties"] == ["p"]


def test_parser_to_dict_shape(parser):
    data = parser.to_dict()

    assert isinstance(data, dict)
    assert "SampleTable.tmdl" in data
    entries = data["SampleTable.tmdl"]
    assert isinstance(entries, list)
    assert {"description", "element", "calculation", "properties"} <= set(entries[0].keys())


def test_parser_to_dict_is_json_serializable(parser, tmp_path):
    import json
    data = parser.to_dict()
    path = tmp_path / "out.json"
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    reloaded = json.loads(path.read_text(encoding="utf-8"))
    assert reloaded.keys() == data.keys()


def test_to_dataframe_flattened(parser):
    pd = pytest.importorskip("pandas")
    df = parser.to_dataframe()

    assert list(df.columns) == [
        "table", "parent_element", "element",
        "description", "calculation", "properties",
    ]
    assert len(df) > 0
    assert df["table"].nunique() == len(parser.tables)
    top_level_rows = df[df["parent_element"] == ""]
    assert len(top_level_rows) >= len(parser.tables)


def test_to_dataframe_non_flattened(parser):
    pd = pytest.importorskip("pandas")
    df = parser.to_dataframe(flatten=False)

    assert (df["parent_element"] == "").all()
    assert len(df) >= len(parser.tables)


def test_to_dataframe_missing_pandas(parser, monkeypatch):
    import builtins
    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "pandas":
            raise ImportError("no pandas here")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    with pytest.raises(ImportError, match="pandas is required"):
        parser.to_dataframe()
