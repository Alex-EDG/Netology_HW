import unittest.mock
from unittest.mock import patch
import src.app as app
import pytest

# 1 часть домашнего задания
class MockInput:
    def __init__(self, values):
        self.values = values
        self.index = 0
    def __call__(self, prompt):
        value = self.values[self.index]
        self.index += 1
        return value

class TestApp(unittest.TestCase):
    def setUp(self):
        self.documents = [
            {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
            {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
            {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
        ]
    def tearDown(self):
        del self.documents

    def test_add_new_doc(self):
        with patch('builtins.input', MockInput(['2222 222222', 'passport', 'Иван Иванов', '3'])):
            self.assertEqual(app.add_new_doc(),'3')

    def test_delete_doc(self):
        input_values = [doc['number'] for doc in self.documents]
        for item in input_values:
            with patch('builtins.input', return_value=item):
                self.assertEqual(app.delete_doc(), (item, True), f'документ {item} не удалён')

def generate_test_data():
    documents = [
        {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
        {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
        {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
    ]
    for doc in documents:
        yield doc, '{} "{}" "{}"'.format(doc['type'],
                                               doc['number'],
                                               doc['name'])

@pytest.mark.parametrize('document,result', generate_test_data())
def test_show_document_info_with_params(document,result):
    assert app.show_document_info(document) == result, f'Должны выводиться элементы словаря'

if __name__ == '__main__':

    test_app = TestApp()
    test_app.test_add_new_doc()
    test_app.test_delete_doc()
    test_show_document_info_with_params()