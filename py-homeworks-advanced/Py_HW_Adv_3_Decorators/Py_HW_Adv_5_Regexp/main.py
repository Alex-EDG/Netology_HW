import csv
import re

# читаем адресную книгу в формате CSV в список contacts_list
def read_file(file_name, delimiter = ",", encoding="utf-8"):
    """
    :param file_name: CSV file name for processing,
           with column (lastname,firstname,surname,organization,position,phone,email) <Str>
    :param delimiter: Delimiter <Str>
    :param encoding: Encoding file <Str>
    :return: Contacts list from CSV file <List>
    """
    with open(file_name, encoding = encoding) as f:
        rows = csv.reader(f, delimiter = delimiter)
        contacts_list = list(rows)
    return contacts_list

def write_file(input_list, file_name, delimiter = ",", encoding="utf-8"):
    """
    :param input_list: List with data for write in file <List>
    :param file_name: CSV file name for write processed data <Str>
    :param delimiter: Delimiter <Str>
    :param encoding: Encoding file <Str>
    :return:
    """
    with open(file_name, "w", encoding = encoding, newline = '') as f:
      datawriter = csv.writer(f, delimiter = delimiter)
      datawriter.writerows(input_list)

def row_process(input_list):
    """
    :param input_list: Input contact list for processing <List>
    :return: Processed contact list <List>
    """
    temp_list = []
    for file in input_list:
        new_file = " ".join(file[:3]).strip().split(" ")
        if len(new_file) == 3 and new_file[2] != '':
            new_file.extend(file[3:])
        elif len(new_file) == 4 and new_file[2] == '':
            new_file.pop(2)
            new_file.extend(file[3:])
        else:
            new_file.extend([''] + file[3:])
        new_file[5] = formating_phone_number(new_file[5])
        temp_list.append(new_file)
    return temp_list

def formating_phone_number(input_phone_number):
    """
    :param input_phone_number: Phone number for processing <Str>
    :return: Output phone number formated as "+7(999)999-99-99" + (" доб.9999" if exist)
    """
    pattern = r"(\+7|8)\s*\(*(\d{3})\)*[-\s]*(\d{3})[-\s]*(\d{2})[-\s]*(\d{2})(\s*)\(*(доб\.)*\s*(\d+)*\)*"
    result = re.sub(pattern, r"+7(\2)\3-\4-\5\6\7\8", input_phone_number)
    return result

def grouping_data(input_list):
    """
    :param input_list: Input list for grouping data by [1:3] list elements <List>
    :return: Output list with grouped data <List>
    """
    groups = {}
    for lastname, firstname, surname, *others in input_list:
        groups.setdefault((lastname, firstname, surname), [""] * len(others))
        for idx, val in enumerate(others):
            if groups[(lastname, firstname, surname)][idx] != val:
                groups[(lastname, firstname, surname)][idx] += val
    result = [[*key, *value] for key, value in groups.items()]
    return result

if __name__ == '__main__':

    # TODO 1: выполнение пунктов 1-3 ДЗ
    input_data = read_file("phonebook_raw.csv")
    processed_data = row_process(input_data)
    data_for_write = grouping_data(processed_data)

    # TODO 2: сохранение получившиеся данные в другой файл
    write_file(data_for_write, "phonebook.csv")