from exercises.function_exercises import (
    sum_of_elements,
    reverse_string,
    count_upper_and_lower_cases,
    sort_hyphen_separated_words,
    create_prime_number_list
)


def test_sum_of_elements_with_multiple_numbers():
    result = sum_of_elements([4, 6, 2, 29])

    assert result == 41


def test_sum_of_elements_with_small_list():
    result = sum_of_elements([1, 2, 3])

    assert result == 6


def test_sum_of_elements_with_empty_list():
    result = sum_of_elements([])

    assert result == 0


def test_reverse_string_with_sentence():
    result = reverse_string("Hello world")

    assert result == "dlrow olleH"


def test_reverse_string_with_word():
    result = reverse_string("Python")

    assert result == "nohtyP"


def test_reverse_string_with_empty_string():
    result = reverse_string("")

    assert result == ""


def test_count_upper_and_lower_cases_with_sentence(capsys):
    count_upper_and_lower_cases("I love Nation Sushi")

    captured = capsys.readouterr()

    assert captured.out.strip() == "There's 3 upper cases and 13 lower cases"


def test_count_upper_and_lower_cases_with_only_uppercase(capsys):
    count_upper_and_lower_cases("ABC")

    captured = capsys.readouterr()

    assert captured.out.strip() == "There's 3 upper cases and 0 lower cases"


def test_count_upper_and_lower_cases_with_only_lowercase(capsys):
    count_upper_and_lower_cases("abc")

    captured = capsys.readouterr()

    assert captured.out.strip() == "There's 0 upper cases and 3 lower cases"


def test_sort_hyphen_separated_words_with_multiple_words():
    result = sort_hyphen_separated_words("python-variable-function-computer-monitor")

    assert result == "computer-function-monitor-python-variable"


def test_sort_hyphen_separated_words_with_three_words():
    result = sort_hyphen_separated_words("zebra-tree-house")

    assert result == "house-tree-zebra"


def test_sort_hyphen_separated_words_with_one_word():
    result = sort_hyphen_separated_words("one")

    assert result == "one"


def test_create_prime_number_list_with_mixed_numbers():
    result = create_prime_number_list([1, 4, 6, 7, 13, 9, 67])

    assert result == [7, 13, 67]


def test_create_prime_number_list_with_only_prime_numbers():
    result = create_prime_number_list([2, 3, 5, 11])

    assert result == [2, 3, 5, 11]


def test_create_prime_number_list_with_no_prime_numbers():
    result = create_prime_number_list([4, 6, 8, 9, 10])

    assert result == []