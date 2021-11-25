from model_utils import *
from get_news import *
from validate_data import *
from instagram_parsing import *

def main(path):
    """
    Функция для определения победителя
    """
    # Обработка загруженных данных 
    comp_points, сompanies = validate_data(path)
    max_comp_points = max(comp_points.values())
    min_comp_points = min(comp_points.values())
    for key in comp_points.keys():
        comp_points[key] = (comp_points[key] - min_comp_points) / \
            (max_comp_points - min_comp_points)
    
    # Инициализация модели
    model, tokenizer = load_model_and_tokenizer()

    # Парсинг количества упоминаний о компании в новостях
    comp_points_news = {}
    for comp in сompanies:
        comp_points_news[comp] = get_google_news(comp, model, tokenizer)
    for key in comp_points_news.keys():
        comp_points_news[key] = sum(comp_points_news[key].values())
    max_comp_points_news = max(comp_points_news.values())
    min_comp_points_news = min(comp_points_news.values())
    for key in comp_points_news.keys():
        comp_points_news[key] = (
            comp_points_news[key] - min_comp_points_news) / (
            max_comp_points_news - min_comp_points_news)
    
    # Парсинг количесвта упоминаний о компании в важных СМИ
    comp_points_smi = {}
    for comp in сompanies:
        comp_points_smi[comp] = get_news_from_smi(comp, '', model, tokenizer)
    for key in comp_points_smi.keys():
        comp_points_smi[key] = sum(comp_points_smi[key].values())
    max_comp_points_smi = max(comp_points_smi.values())
    min_comp_points_smi = min(comp_points_smi.values())
    for key in comp_points_smi.keys():
        comp_points_smi[key] = (
            comp_points_smi[key] - min_comp_points_smi) / (
            max_comp_points_smi - min_comp_points_smi)
    
    # Парсинг инстаграмма
    nicks = list(pd.read_excel(path)['social_media'])
    comp_points_inst = {}
    for nick, comp in zip(nicks, сompanies):
        comp_points_inst[comp] = get_stats_from_instagram(nick)
    max_comp_points_inst = max(comp_points_inst.values())
    min_comp_points_inst = min(comp_points_inst.values())
    for key in comp_points_inst.keys():
        comp_points_inst[key] = (
            comp_points_inst[key] - min_comp_points_inst) / (
            max_comp_points_inst - min_comp_points_inst)
                
    # Определение финального победителя суммированием полученных баллов
    results = {}
    for key in comp_points.keys():
        results[key] = comp_points[key] + \
            comp_points_smi[key] + comp_points_news[key] + \
            comp_points_inst[key]

    print(f'ПОБЕДИТЕЛЬ - {max(results, key=results.get)}')
    return results


if __name__ == "__main__":
    print('Введите путь до файла с претендентами на премию:\n')
    path = input()
    main(path)

