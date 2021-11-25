from pygooglenews import GoogleNews
import feedparser
import csv
import pandas as pd
import re

from model_utils import predict

def get_google_news(company, model, tokenizer):
    """
    Функция для парсинга упоминаний о компании в Google News
    """
    gn = GoogleNews(lang='ru', country='RUS')
    news = gn.search(company, when='120d')
    counter = {0: 0,
               1: 0,
               2: 0}
    for i in range(len(news['entries'])):
        sentim = predict(news['entries'][i].title, model, tokenizer)
        if sentim == 0:
            counter[sentim] += 1
        elif sentim == 1:
            counter[sentim] += 2
        else:
            counter[sentim] += -1

    return counter


def get_news_from_smi(company, target, model, tokenizer):
    """
    Функция для парсинга публикаций о компании в значимых СМИ
    """
    def parseRSS(rss_url):
        """
        Функция получает ссылку на rss ленту, возвращает распаршенную 
        c помощью feedpaeser ленту
        """
        return feedparser.parse(rss_url)

    def getHeadlines(rss_url):
        """
        Функция для получения заголовка новости
        """
        headlines = []
        feed = parseRSS(rss_url)
        for newsitem in feed['items']:
            headlines.append(newsitem['title'])
        return headlines

    def getDescriptions(rss_url):
        """
        Функция для получения описания новости
        """
        descriptions = []
        feed = parseRSS(rss_url)
        for newsitem in feed['items']:
            descriptions.append(newsitem['description'])
        return descriptions

    def getLinks(rss_url):
        """
        Функция для получения ссылки на источник новости
        """
        links = []
        feed = parseRSS(rss_url)
        for newsitem in feed['items']:
            links.append(newsitem['link'])
        return links

    def getDates(rss_url):
        """
        Функция для получения даты публикации новости
        """
        dates = []
        feed = parseRSS(rss_url)
        for newsitem in feed['items']:
            dates.append(newsitem['published'])
        return dates

    def write_all_news(all_news_filepath):
        """
        Функция для записи всех новостей в .csv, возвращает полученный датасет
        """
        header = ['Title', 'Description', 'Links', 'Publication Date']
        with open(all_news_filepath, 'w', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(i for i in header)

            for a, b, c, d in zip(allheadlines, alldescriptions,
                                  alllinks, alldates):
                writer.writerow((a, b, c, d))
            df = pd.read_csv(all_news_filepath)
        return df

    def looking_for_certain_news(
            all_news_filepath,
            certain_news_filepath,
            target1,
            target2):
        """
        Функция для поиска новостей по ключевым словам 
        """
        df = pd.read_csv(all_news_filepath)
        result = df.apply(
            lambda x: x.str.contains(
                target1,
                na=False,
                flags=re.IGNORECASE,
                regex=True)).any(
            axis=1)
        result2 = df.apply(
            lambda x: x.str.contains(
                target2,
                na=False,
                flags=re.IGNORECASE,
                regex=True)).any(
            axis=1)
        new_df = df[result & result2]
        new_df.to_csv(certain_news_filepath, sep='\t', encoding='utf-8-sig')
        return new_df

    newsurls = {'Kommersant': 'https://www.kommersant.ru/RSS/news.xml',
                'Lenta.ru': 'https://lenta.ru/rss/',
                'Vesti': 'https://www.vesti.ru/vesti.rss',
                'Meduza': 'https://meduza.io/rss/all',
                'RBK': 'http://static.feed.rbc.ru/rbc/logical/footer/news.rss'
                }

    f_all_news = 'allnews.csv'
    f_certain_news = 'certainnews.csv'

    vector1 = f'{target}'
    vector2 = f'{company}'

    allheadlines = []
    alldescriptions = []
    alllinks = []
    alldates = []

    for key, url in newsurls.items():
        allheadlines.extend(getHeadlines(url))

    for key, url in newsurls.items():
        alldescriptions.extend(getDescriptions(url))

    for key, url in newsurls.items():
        alllinks.extend(getLinks(url))

    for key, url in newsurls.items():
        alldates.extend(getDates(url))

    df = write_all_news(f_all_news)
    new_df = looking_for_certain_news(
        f_all_news, f_certain_news, vector1, vector2)

    counter = {0: 0,
               1: 0,
               2: 0}

    for i in new_df.Description:

        sentim = predict(i, model, tokenizer)
        if sentim == 0:
            counter[sentim] += 1
        elif sentim == 1:
            counter[sentim] += 2
        else:
            counter[sentim] += -1

    return counter
