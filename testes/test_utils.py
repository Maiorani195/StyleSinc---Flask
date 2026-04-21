from app.utils import format_currency

def test_format_currency():
    input_value = 59.9
    result = format_currency(input_value)
    
    assert result == "R$ 59,90"


def test_format_currency_with_integer_value():
    assert format_currency(100) == "R$ 100,00"


def test_format_currency_with_zero_value():
    assert format_currency(0) == "R$ 0,00"

