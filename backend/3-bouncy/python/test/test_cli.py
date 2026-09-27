from cli import main


def test_cli_returns_538(capsys):
    main(["50"])

    captured = capsys.readouterr()

    assert captured.out.strip() == "538"


def test_cli_returns_21780(capsys):
    main(["90"])

    captured = capsys.readouterr()

    assert captured.out.strip() == "21780"


def test_cli_rejects_invalid_percent(capsys):
    main(["100"])

    captured = capsys.readouterr()

    assert "entre 1 y 99" in captured.out