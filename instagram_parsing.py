import requests
import pandas as pd
import json
import numpy as np
 
def get_stats_from_instagram(account):
    """
    Функция для парсинга информации о компании из Инстаграмма.
    """
    url = 'https://www.instagram.com/{}/?__a=1'.format(account)
    text = requests.get(url).text
    followers = json.loads(text)['graphql']['user']['edge_followed_by']['count']
    
    #publications = json.loads(text)['graphql']['user']['edge_owner_to_timeline_media']['count']
    
    #likes = []
    #comments = []
    
    #edges = json.loads(text)['graphql']['user']['edge_owner_to_timeline_media']['edges']
    
    #for i in range(len(edges)):
    #    likes.append(edges[i]['node']['edge_liked_by']['count'])
    #    comments.append(edges[i]['node']['edge_media_to_comment']['count'])
        
    #likes = round(np.mean(likes), 2)
    #comments = round(np.mean(comments), 2)
            
    #following = json.loads(text)['graphql']['user']['edge_follow']['count']
    #return [publications, likes, comments, followers, following]
    
    return followers
