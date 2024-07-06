import pytest

from src.decorators import log


def test_log_file():
    filename = "mylog.txt"

    @log(filename=filename)
    def my_function(x, y):
        return x + y

    result = my_function(1, 2)

    assert result == 3

    with open(filename, "r") as f:
        content = f.read().strip()

    assert "my_function ok" in content


def test_log_error():
    filename = "mylog.txt"

    @log(filename=filename)
    def my_function(x, y):
        return x / y

    with pytest.raises(ZeroDivisionError):
        my_function(1, 0)

    error_message = "my_function error: ZeroDivisionError. Inputs: (1, 0), {}"

    with open(filename, "r") as f:
        content = f.read().strip()

    assert error_message in content
