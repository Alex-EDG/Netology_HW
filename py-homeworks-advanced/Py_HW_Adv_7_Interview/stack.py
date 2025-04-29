from typing import List


class Stack:
    """
    Stack object as LIFO type
    """
    def __init__(self):
        self.stack_list: List = []

    def is_empty(self) -> bool:
        if self.stack_list:
            return False
        else:
            return True

    def push(self, item):
        """
        :param item: Item to add in stack
        """
        self.stack_list.append(item)

    def pop(self):
        """
        :return: Return last stack item and reduce stack, if stack empty return None
        """
        if self.stack_list:
            return self.stack_list.pop()
        else:
            return None

    def peek(self):
        """
        :return: Return last stack item not reduce stack, if stack empty return None
        """
        if self.stack_list:
            return self.stack_list[-1]
        else:
            return None

    def size(self):
        """
        :return: Return number of elements in stack
        """
        return len(self.stack_list)