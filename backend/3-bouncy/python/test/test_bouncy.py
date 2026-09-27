import pytest

from bouncy import least_number_with_bouncy_ratio

# El 50% de los números son bouncy.
# El primer número que alcanza exactamente esa proporción es 538.
def test_50_percent_returns_538():
    assert least_number_with_bouncy_ratio(50) == 538

# Verifica el segundo caso proporcionado por el enunciado.
# El primer número donde la proporción de bouncy alcanza el 90% es 21780.
def test_90_percent_returns_21780():
    assert least_number_with_bouncy_ratio(90) == 21780

# Verifica que no se acepten porcentajes menores al límite permitido.
def test_invalid_percent_below_1():
    with pytest.raises(ValueError):
        least_number_with_bouncy_ratio(0)

# Verifica que no se acepten porcentajes mayores al límite permitido.
def test_invalid_percent_above_99():
    with pytest.raises(ValueError):
        least_number_with_bouncy_ratio(100)

# El primer número cuya proporción de bouncy es exactamente 99% es 1587000.
def test_99_percent_returns_1587000():
    assert least_number_with_bouncy_ratio(99) == 1587000