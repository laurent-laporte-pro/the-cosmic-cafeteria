from src.cli.__about__ import __version__


def test_version() -> None:
    parts = list(map(int, __version__.split('.', maxsplit=2)))
    assert len(parts) == 3
    assert all(part >= 0 for part in parts)
