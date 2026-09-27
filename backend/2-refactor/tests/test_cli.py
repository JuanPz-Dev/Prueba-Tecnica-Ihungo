import sys

from sentiment_analysis import cli


def test_parse_arguments(monkeypatch):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "cli.py",
            "--input",
            "input.xlsx",
            "--output",
            "output.xlsx",
            "--sheet",
            "Sheet1",
            "--text-column",
            "3",
        ],
    )

    args = cli.parse_arguments()

    assert args.input == "input.xlsx"
    assert args.output == "output.xlsx"
    assert args.sheet == "Sheet1"
    assert args.text_column == 3