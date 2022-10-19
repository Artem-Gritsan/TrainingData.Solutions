import xml.etree.ElementTree as ET




def classes_statistic(root):
    tag_types = {}
    for child in root.findall('./image/'):
        if child.tag in tag_types:
            tag_types[child.tag] += 1
        else:
            tag_types[child.tag] = 1
    if len(tag_types) == 0:
        return 'В файле нет нужных данных'
    return tag_types



def main():
    while True:
        try:
            start = input("Введите название файла или exit: ")
            if start == 'exit':
                break
            tree = ET.parse(f'{start}.xml')
            root = tree.getroot()
            print(classes_statistic(root))
        except FileNotFoundError:
            print('Что-то пошло не так. Попробуйте еще раз!')











if __name__ == '__main__':
    main()