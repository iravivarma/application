import pandas as pd
from urllib.request import urlopen
import requests
import bs4
import csv
import pandas as pd
import time
import nltk

def data_extractor(url):
# ##making the request####
    req = requests.get(url)
    print(type(req))
    #print(req.text)

    data = bs4.BeautifulSoup(req.text, 'lxml')
    print(type(data))
    return data


def get_categorie_links(url): 
    web_data = data_extractor(url)
    #print(web_data)
    categorywrapper = web_data.find(class_ = 'page--body')
    category_names = categorywrapper.find_all('a')
    
    ##get the categoory names and there links#####
    category_links = []
    cat_names = []
    for cat_name in category_names:
        cat_names.append(cat_name.text.strip())
        category_links.append(cat_name.get('href'))
        # print(cat_names)
        # print(category_links)
    return category_links, cat_names

domain_links = ['https://hackr.io/data-science'
                ]


domain_name = {}
cat_names = {}
category_links = []

for domains in domain_links:
    #print(domains)
    domain=[]
    
    domain_text = domains.split('/')[-1]
    # domain.append(domain_text)
    # print(domain)
    # if 'domain' in domain_name.keys():
    #     domain_name['domain'].extend(domain)
    # else:
    #     domain_name['domain'] = domain
    category_links.extend(get_categorie_links(domains)[0])
    cat_names = {}
    for category in category_links:
        category_name = []
        temp_dict={}
        cat_text = category.split('/')[-1]
        category_name.append(cat_text)
        print(category_name)
        temp_dict['category_name'] = category_name
        if 'category_name' in cat_names.keys():
            cat_names['category_name'].extend(category_name)
        else:
            cat_names['category_name'] = category_name

            
    df = pd.DataFrame(cat_names)
    df.to_csv('{}-categories.csv'.format(domain_text))



            

    





