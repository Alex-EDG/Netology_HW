import types

# 1 часть домашнего задания
class FlatIterator1:

    def __init__(self, list_of_list):
        self.list_of_list = list_of_list

    def __iter__(self):
        self.cursor = -1
        self.flat_list = self.get_flat_list(self.list_of_list)
        return self

    def __next__(self):
        self.cursor += 1
        if self.cursor == len(self.flat_list):
            raise StopIteration
        return self.flat_list[self.cursor]

    def get_flat_list(self, list_of_lst):
        return [item_l for item_l_o_l in list_of_lst for item_l in item_l_o_l]

def test_1():

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator1(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):

        assert flat_iterator_item == check_item

    assert list(FlatIterator1(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

# 2 часть домашнего задания
def flat_generator2(list_of_lists):
    cursor = -1
    for _ in list_of_lists:
        cursor += 1
        if cursor < len(list_of_lists):
            for item in list_of_lists[cursor]:
                yield item
        else:
            cursor = -1

def test_2():

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator2(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):

        assert flat_iterator_item == check_item

    assert list(flat_generator2(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

    assert isinstance(flat_generator2(list_of_lists_1), types.GeneratorType)

# 3 часть домашнего задания
class FlatIterator3:

    def __init__(self, list_of_list):
        self.list_of_list = list_of_list

    def __iter__(self):
        self.cursor = -1
        self.flat_list = self.get_flat_list(self.list_of_list)
        return self

    def __next__(self):
        self.cursor += 1
        if self.cursor == len(self.flat_list):
            raise StopIteration
        return self.flat_list[self.cursor]

    def get_flat_list(self, list_of_lst):
        result = []
        for item_l_o_l in list_of_lst:
            if not isinstance(item_l_o_l, list):
                result.append(item_l_o_l)
            else:
                result.extend(self.get_flat_list(item_l_o_l))
        return result

def test_3():
    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator3(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):
        assert flat_iterator_item == check_item

    assert list(FlatIterator3(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']

# 4 часть домашнего задания
def flat_generator4(list_of_list):
    def get_flat_list(list_of_lst):
        result = []
        for item_l_o_l in list_of_lst:
            if not isinstance(item_l_o_l, list):
                result.append(item_l_o_l)
            else:
                result.extend(get_flat_list(item_l_o_l))
        return result

    flat_list = get_flat_list(list_of_list)
    for item in flat_list:
        yield item

def test_4():

    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator4(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):

        assert flat_iterator_item == check_item

    assert list(flat_generator4(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']

    assert isinstance(flat_generator4(list_of_lists_2), types.GeneratorType)

if __name__ == '__main__':
    
    test_1()
    test_2()
    test_3()
    test_4()