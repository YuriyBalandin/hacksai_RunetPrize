import pandas as pd

def validate_data(path):
    """
    Функция для загрзуки и проверки структуры/корректности загруженного файла
    с данными регистраций претендентов
    """
    data = pd.read_excel(path)

    points = {}
    for i in data['Название_компании']:
        points[i] = 0

    na_values = pd.DataFrame(data[['Название_компании',
                                   'Сайт',
                                   'Вклад_в_развитие_Рунета',
                                   'PR_СМИ',
                                   'Интернет_проекты_сайты',
                                   'Общественный_вклад',
                                   'Взаимод_с_властью',
                                   'Технологии_решения',
                                   'Person']].isna().sum(axis=1))

    na_values.columns = ['na_values']
    na_values['company'] = data['Название_компании']
    na_values['len_less_then_100'] = data['Вклад_в_развитие_Рунета'].apply(
        lambda x: 1 if len(x) < 100 else 0)
    
    # TODO 
    # Добавить проверку на минимальное кол-во символов:
    
    #def check_len(x):
    #count = 0
    #for i in x:
    #    if len(i) < 10 :
    #        count += 1
    #return count 
    #df.apply(lambda x : check_len(x) , axis= 1)

    for comp in na_values.company:
        points[comp] -= 0.1 * na_values[na_values.company ==
                                        comp]['na_values'].values[0]
        points[comp] -= 0.1 * na_values[na_values.company ==
                                        comp]['len_less_then_100'].values[0]

    return points, list(data['Название_компании'])