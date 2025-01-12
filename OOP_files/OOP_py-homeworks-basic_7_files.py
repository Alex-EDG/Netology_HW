# Задание № 3.

class Merging:
    def __init__(self, files_names_list):
        self.files_names_list = files_names_list
        self.result_file_list = []

    def sort_files_list_as_rule(self):
        self.sorted_file_list = {}

        file_list = {}
        for file in self.files_names_list:
            with open(file, 'r', encoding='utf-8') as f:
                num_lines = sum(1 for line in f)
                file_list.update({file: num_lines})
        self.sorted_file_list = dict(sorted(file_list.items(), key=lambda kv: kv[1]))

    def output(self):

        for file in self.sorted_file_list:
            with open(file, 'r', encoding='utf-8') as f:
                file_data = f.read()
            with open('result.txt', 'a', encoding='utf-8') as output:
                output.write(file + '\n' + str(self.sorted_file_list[file]) + '\n' + file_data + '\n')

    def show_result(self):
        with open('result.txt', 'r', encoding='utf-8') as f:
            print('Resulting file (result.txt):', '\n' + f.read())

# Задание № 1

class CookBook:
    def __init__(self, file_name):
        self.file_name = file_name
        self.cook_book = {}

    def read_cb_file(self, file_name):
        self.file_name = file_name

        with open(file_name, 'r', encoding='utf-8') as file_cb:
            lines_file_cb = [line.strip() for line in file_cb]
            temp_list = []
            for line in lines_file_cb:
                if line != '':
                    temp_list.append(line)
                else :
                    temp_list = []
                dish_ingr_list = []
                for idx, ingredient in enumerate(temp_list):
                    if idx > 1:
                        temp_dict = {'ingredient_name': ingredient.split(' | ')[0],
                                     'quantity': int(ingredient.split(' | ')[1]),
                                     'measure': ingredient.split(' | ')[2]}
                        dish_ingr_list.append(temp_dict)
                        self.cook_book.update({temp_list[0]: dish_ingr_list})

# Задание № 1. Полевые испытания

cook_book = CookBook('recipes.txt')
cook_book.read_cb_file('recipes.txt')
print(cook_book.cook_book, '\n')

# Задание № 2

def get_shop_list_by_dishes(dishes, person_count):
    shop_list_by_dishes = {}
    if set(dishes).issubset(set(cook_book.cook_book.keys())):
        for dish in dishes:
            temp_list = cook_book.cook_book.get(dish)
            for ingredient in temp_list:
                if shop_list_by_dishes.get(ingredient.get('ingredient_name')) is None:
                    shop_list_by_dishes.update({ingredient.get('ingredient_name'): {
                                                              'measure': ingredient.get('measure'),
                                                              'quantity': ingredient.get('quantity') * person_count
                                                                                  }
                                               }
                                              )
                else :
                    prev_val = shop_list_by_dishes.get(ingredient.get('ingredient_name')).get('quantity')
                    shop_list_by_dishes.update({ingredient.get('ingredient_name'): {
                                                              'measure': ingredient.get('measure'),
                                                              'quantity': prev_val + ingredient.get('quantity') * person_count
                                                                                  }
                                              }
                                             )
    else :
        return 'Рецепт отсутствует в Cook Book'
    return shop_list_by_dishes

# Задание №2. Полевые испытания

print(get_shop_list_by_dishes(['Запеченный картофель', 'Омлет'], 2), '\n')

# Задание № 3. Полевые испытания

merge_files = Merging(('1.txt', '2.txt', '3.txt'))
merge_files.sort_files_list_as_rule()
merge_files.output()
merge_files.show_result()