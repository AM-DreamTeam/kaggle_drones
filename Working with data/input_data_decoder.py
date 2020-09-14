import json


def get_warehouses_products(type_products_count: int, current_warehouse_data: list, index: int) -> dict:
    ''' Словарь с товарами на складе
        
        Аргументы:
            types_products_count (int): количество типов товаров
            current_warehiuses_data (list): текущий (неотформатированный) список с количеством товаров кажодого типа
            index (int): идентификатор склада, с которым мы сейчас работаем
        
        Возвращает:
            dict: словарь с отформатированными значениями продуктов, которые содержатся на складе
    '''
    
    
    return {_: int(current_warehouse_data.split()[_]) for _ in range(type_products_count)}


def decoding_input_data(filename: str) -> dict:
    ''' Декодирование входных данных

        Аргументы:
            filename (str): имя файла, который необходимо декодировать

        Возвращает:
            dict: словарь с декодированными данными
    '''

    # Открывам файл
    with open(filename, 'r') as f:
        input_data = f.read().split('\n')

    # Базовые данные
    names = ['rows', 'columns', 'drones', 'turns', 'max_payload']
    basic_data = {names[_]: int(input_data[0].split()[_]) for _ in range(len(names))}

    # Данные о товарах
    types_products_count = int(input_data[1])
    types_products_data = input_data[2].split()
    weigh_of_types = {_: int(types_products_data[_]) for _ in range(types_products_count)}

    # Данные о складах
    warehouses_count = int(input_data[3])
    warehouses_input_data = input_data[4:(warehouses_count + 2) * 2]
    warehouse_coords = warehouses_input_data[::2]
    warehouse_products = warehouses_input_data[1::2]

    warehouses_data = {i:
                    {'coordinates': tuple(map(int, warehouse_coords[i].split())),
                     'products': get_warehouses_products(types_products_count, warehouse_products[i], i)}
    for i in range(warehouses_count)}

    # Данные о заказах
    orders_count = int(input_data[(warehouses_count + 2) * 2])
    orders_input_data = input_data[(warehouses_count + 2) * 2 + 1:]

    orders_coords = orders_input_data[::3]
    orders_product_count = orders_input_data[1::3]
    orders_product_types = orders_input_data[2::3]

    orders_data = {i:
               {'coords': tuple(map(int, orders_coords[i].split())),
                'count_products': int(orders_product_count[i]),
                'product_types': list(map(int, orders_product_types[i].split()))}
    for i in range(orders_count)}

    # Собираем все данные в один большой словарь
    field_names = ['basic_data',
                   'types_products_count',
                   'products_data',
                   'warehouses_count',
                   'warehouses_data',
                   'orders_count',
                   'orders_data']

    list_all_data = [basic_data,
                     types_products_count,
                     weigh_of_types,
                     warehouses_count,
                     warehouses_data,
                     orders_count,
                     orders_data]

    all_data = dict(zip(field_names, list_all_data))

    return all_data


filename = str(input('Введите файл, который необходимо декодировать: '))

try:
    with open('decoded_data.json', 'w') as f:
        json.dump(decoding_input_data(filename), f, indent = 4)
    print('\nФайл был успешно декодирован и сохранён (decoded_data.json)')
except:
    print('\nФайл не найден')
