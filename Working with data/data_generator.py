from random import randint, sample
from json import dump


def generate_data(input_params: dict) -> dict:
    ''' Создание входных данных
        
        Аргументы:
            input_params (dict): словарь со всеми необходимыми атрибутами
                Поля input_params:
                    rows - количество строк,
                    columns - количество столбцов,
                    drones - количество дронов,
                    turns - количество ходов,
                    max_payload - максимальная загруженность дронов,
                    types_products_count - количество типов продуктов,
                    weight_interval - интервал значений весов товаров,
                    warehouses_count - количество складов,
                    interval_products_on_warehouse_count - интервал значений количества товаров,
                    orders_count - количество заказов,
                    max_items_in_order - максимальное количество товаров в заказах
        
        Возвращает:
            dict: словарь с псевдо-данными
    '''
    # Базовые данные
    rows = input_params['rows']                    # количество строк
    columns = input_params['columns']              # количество столбцов
    drones = input_params['drones']                # количество дронов
    turns = input_params['turns']                  # количество ходов
    max_payload = input_params['max_payload']      # максимальная загруженность дронов
    
    names = ['rows', 'columns', 'drones', 'turns', 'max_payload']
    basic_data = dict(zip(names, [rows, columns, drones, turns, max_payload]))
    
    # Данные о товарах 
    types_products_count = input_params['types_products_count']  # количество типов продуктов
    weight_interval = input_params['weight_interval']            # интервал значений весов товаров
    product_data = [randint(*weight_interval) for _ in range(types_products_count)]  # список весов товаров
    
    weigh_of_types = {_: product_data[_] for _ in range(types_products_count)}
    
    # Данные о складах
    warehouses_count = input_params['warehouses_count']                                             # количество складов
    warehouses_coords = [(randint(0, rows), randint(0, columns)) for _ in range(warehouses_count)]  # раположение складов
    interval_products_on_warehouse_count = input_params['interval_products_on_warehouse_count']     # интервал значений количества товаров
    warehouses_products_count = [[randint(*interval_products_on_warehouse_count)  # количество товаров на складе
                             for _ in range(types_products_count)]
                             for _ in range(warehouses_count)]
    
    warehouses_data = {_: {
                          'coordinates': warehouses_coords[_],
                          'products': warehouses_products_count[_]}
    for _ in range(warehouses_count)}
    
    # Данные о заказах
    orders_count = input_params['orders_count']                 # количество заказов
    max_items_in_order = input_params['max_items_in_order']     # максимальное количество товаров в заказах
    interval_items_in_order = (1, min(max_items_in_order, types_products_count)) # интервал количества товаров в заказах
    orders_coords = [(randint(0, rows), randint(0, columns)) for _ in range(orders_count)]  # раположение заказов
    product_types_in_order = [sample(range(types_products_count), randint(*interval_items_in_order))
                          for _ in range(orders_count)]         # типы товаров, которые находятся в заказах
    count_products_in_order = list(map(len, product_types_in_order))  # количество товаров в заказах
    
    orders_data = {_: {
                      'coordinates': orders_coords[_],
                      'count_products': count_products_in_order[_],
                      'product_types': product_types_in_order[_]}
    for _ in range(orders_count)}
    
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


fields_names = ['rows', 'columns', 'drones', 'turns', 'max_payload', 'types_products_count', 'weight_interval', 'warehouses_count', 'interval_products_on_warehouse_count', 'orders_count', 'max_items_in_order']

input_params = {_: eval(input(f'{_}: ')) for _ in fields_names}

try:
    with open('generated_data.json', 'w') as f:
        dump(generate_data(input_params), f, indent = 4)
        print('\nФайл был успешно создан и сохранён (generated_data.json)')
except:
    print('\nЧто-то пошло не так...')
