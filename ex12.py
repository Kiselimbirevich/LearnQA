import requests

def test_header():
    req = requests.get('https://playground.learnqa.ru/api/homework_header')

    assert 'x-secret-homework-header' in req.headers, "Хедер x-secret-homework-header не передан"
    assert req.headers['x-secret-homework-header'] == 'Some secret value', "Значение хедера отлично от ожидаемого"