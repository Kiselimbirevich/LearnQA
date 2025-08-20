def test_input_lenght():
    phrase = input("Set a phrase: ")
    assert 0 < len(phrase) < 15, f"Условие не выполнено"