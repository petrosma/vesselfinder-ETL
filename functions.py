from bs4 import BeautifulSoup
from tqdm import tqdm
import grequests
import crud


USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 ' \
             'Safari/537.36'
headers = {'User-Agent': USER_AGENT}


def get_vessel_links(content, base_url):
    data =BeautifulSoup(content, 'html.parser')
    links = [base_url+a['href'] for a in data.find_all('a',class_="ship-link" ,href=True) if a.text]
    return list(set(links))


def get_all_vessel_links(flag="IR", pages=4, n1=20, n2=10):
    links=[]
    base_url='https://www.vesselfinder.com/'
    urls=["https://www.vesselfinder.com/vessels?page=%s&flag=%s"%(i, flag) for i in range(1,pages)]
    
    for i in tqdm(range(0, len(urls), n1)):
        rs=(grequests.get(url, headers=headers) for url in urls[i:i+n1])
        lst = grequests.map(rs)
        for item in lst:
            links.extend(get_vessel_links(item.content, base_url))
    links=list(set(links)) 
    for i in tqdm(range(0, len(links), n2)):
        rs = (grequests.get(url, headers=headers) for url in links[i:i+n2])
        lst = grequests.map(rs)
        for item in lst:
            if item:
                get_vessel_information(item.content)
    

def get_vessel_information(content):
    data =BeautifulSoup(content, 'html.parser')
    labels=[]
    values=[]
    if data.find('table', {'class':'aparams'}):
        labels = data.find('table', {'class':'aparams'}).find_all('td', {'class':'n3'})
        values = data.find('table', {'class':'aparams'}).find_all('td', {'class':'v3'})
        labels = [lbl.get_text(strip=True) for lbl in labels]
        values = [val.get_text(strip=True) for val in values]

        dic = dict(zip(labels, values))
        data_label=[]
        data_value=[]
        for key in dic.keys():
            key: str
            val:str = dic[key]
            if "ETA" in key:
                data_label.append("ETA")
                data_value.append(dic[key])
            if 'mmsi' in key.lower():
                data_label.append('vessel_mmsi')
                data_value.append(val.split('/')[0] if len(val.split('/')) == 2 else '')
            if "course" in key.lower():
                data_label.append("course")
                data_label.append("speed")
                data_value.append(val.split('/')[0] if len(val.split('/')) == 2 else '')
                data_value.append(val.split('/')[1] if len(val.split('/')) == 2 else '')
            if 'position received' in key.lower():
                data_label.append('pos_received')
                data_value.append(dic[key])

        vessel_dic = dict(zip(data_label, data_value))
        crud.insert_vessel(vessel_data=vessel_dic)
        #print(vessel_dic)
    
            

