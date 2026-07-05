from graphs import generate_graph

def test_no_expression():
    assert generate_graph("") is None

def test_basic_plot():
    b64 = generate_graph("y=x^2")
    assert b64 is not None
    assert isinstance(b64, str)
    assert len(b64) > 100

def test_trig_plot():
    b64 = generate_graph("y=sin(x)")
    assert b64 is not None
