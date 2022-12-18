from evaluator import EVHelp


def test_help(ev, capsys):
    ev.ev('help')
    output = capsys.readouterr().out
    assert "Reverse Polish Notation" in output


def test_overview(capsys):
    topic = None
    EVHelp(topic)
    output = capsys.readouterr().out
    assert "OVERVIEW:" in output


def test_topics(capsys):
    topic = "topics"
    EVHelp(topic)
    output = capsys.readouterr().out
    assert "Stack functions:" in output


def test_cos(capsys):
    topic = "cos"
    EVHelp(topic)
    output = capsys.readouterr().out
    assert "cos:" in output


def test_not_found(capsys):
    topic = "bogus"
    EVHelp(topic)
    output = capsys.readouterr().out
    assert "bogus" in output
