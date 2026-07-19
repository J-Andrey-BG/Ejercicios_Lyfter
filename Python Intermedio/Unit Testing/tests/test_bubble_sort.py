import pytest

from exercises.bubble_sort import bubble_sort


def test_small_list():
    result = bubble_sort([5, 3, 8, 1])

    assert result == [1, 3, 5, 8]


def test_large_list():
    numbers = list(range(150, 0, -1))
    expected = list(range(1, 151))

    result = bubble_sort(numbers)

    assert result == expected


def test_empty_list():
    result = bubble_sort([])

    assert result == []


def test_invalid_parameter():
    with pytest.raises(TypeError):
        bubble_sort("not a list")