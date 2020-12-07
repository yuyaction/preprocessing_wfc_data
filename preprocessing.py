import os,sys
import numpy as np
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
from password import *

def setup_digest_auth(base_uri, user, password):
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(
            realm=None,
            uri=base_uri,
            user=user,
            passwd=password)
    auth_handler = urllib.request.HTTPDigestAuthHandler(password_mgr)
    opener = urllib.request.build_opener(auth_handler)
    urllib.request.install_opener(opener)

def download(req,save_path):
    try:
        tmp = urllib.request.urlopen(req)
        data_mem = tmp.read()
        with open(save_path,mode='wb') as f:
            f.write(data_mem)
            print(save_path + ' is downloaded.')
    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.reason)

def get_URL(year,month,base_url):
    month_url = base_url+str(year)+'/'+str(month).zfill(2)+'/'
    html = urllib.request.urlopen(month_url) #get html 
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a')
    for dates in links:
        href= dates.attrs['href']
        string = dates.string
        if href != string:
            continue
        URL_list.append(month_url+href)
    

year = 2018
month = 3
save_dict = './cdf/'+str(year)+'/'+str(month).zfill(2)+'/'
os.makedirs(save_dict,exist_ok=True) #make directories to save
URL_list = []

#Authorization and download cdf files
setup_digest_auth(base_url,user,password) #digest auth
get_URL(year,month,base_url)
for url in URL_list:
    url_path = urllib.parse.urlparse(url).path #get path from URL
    file_name = os.path.basename(url_path) #get file name
    save_path = save_dict + file_name
    download(url,save_path)


