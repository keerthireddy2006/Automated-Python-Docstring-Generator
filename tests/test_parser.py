import pytest
from pathlib import Path
from autodocstring.parser import parse_file  # Direct import (no subprocess needed)


def test_empty_file(tmp_path):
    f = tmp_path / "empty.py"
    f.write_text("")
    result = parse_file(str(f))
    assert result["functions"] == []
    assert result["classes"] == []


def test_syntax_error(tmp_path):
    f = tmp_path / "bad.py"
    f.write_text("def invalid syntax")
    with pytest.raises(SyntaxError):
        parse_file(str(f))
