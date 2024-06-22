import pytest

from src.processing import filter_by_state, sort_by_date


# Тесты для проверки работы функций фильтрации и сортировки
@pytest.mark.parametrize(
    "state, expected_result",
    [
        (
            "EXECUTED",
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            ],
        ),
        (
            "CANCELED",
            [
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
        ),
        ("EMPTY", []),
    ],
)
def test_filter_by_state(sample_data, state, expected_result):
    filtered_data = filter_by_state(sample_data, state)
    assert filtered_data == expected_result


def test_sort_by_date_asc(unsorted_data, sorted_data):
    sorted_result = sort_by_date(unsorted_data, reverse=False)
    assert sorted_result == sorted_data


def test_sort_by_date_desc(unsorted_data, sorted_data):
    sorted_result = sort_by_date(unsorted_data, reverse=True)
    assert sorted_result == list(reversed(sorted_data))
