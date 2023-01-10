import xml.etree.ElementTree as ET


def main():
    while True:
        try:
            start = input("Введите название файла или exit: ")
            if start == 'exit':
                break
            tree = ET.parse(f'{start}.xml')
            root = tree.getroot()
            print(classes(root))
        except FileNotFoundError:
            print('Что-то пошло не так. Попробуйте еще раз!')


def classes(root):
    classes_type = {}
    for child in root.findall('./image/'):
        if child.get('label') in classes_type:
            classes_type[child.get('label')] += 1
        else:
            classes_type[child.get('label')] = 1
    if len(classes_type) == 0:
        return 'В файле нет нужных данных '
    return classes_type






if __name__ == '__main__':
    main()