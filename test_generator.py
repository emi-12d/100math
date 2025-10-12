from generator import get_numbers


def test_get_numbers():
    """問題生成関数のテスト
    """
    problem_list = get_numbers(2)
    # problem_listの要素数が10であること
    assert len(problem_list) == 10
    # problem_listの各要素が2桁の整数であること
    for num in problem_list:
        assert 10 <= num < 100
        assert isinstance(num, int)
    # problem_listの要素が重複していないこと
    assert len(set(problem_list)) == 10