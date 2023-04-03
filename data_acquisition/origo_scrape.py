import asyncio
import pandas as pd
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import concurrent.futures
import time
import json


linkek = (
    pd.read_parquet("osszes_link.parquet")
    .loc[lambda _df: _df["ujsag"] == "origo", :]
    .url.to_list()
)

NUM_THREADS = 60
data = []
def get_origo_texts(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.content)
    try:
        title = soup.find(attrs = {"id" : "article-head"}).get_text().replace("\n", "")
    except:
        title = soup.find(attrs={"class": "article-title"}).get_text().replace("\n", "")
    try:
        text1 = " ".join(
            [
                item.get_text().strip()
                for item in soup.find(attrs = {"class" : "article-lead"}).find_all("p")
            ]
        )
    except:
        text1 = ""
    try:
        text = " ".join(
            [
                item.get_text().strip()
                for item in soup.find(attrs={"class": "article-content"}).find_all("p")
            ]
        )
    except:
        text = ""

    data.append(
        {
            "title": title,
            "text": text1 + " " + text,
            "url" : link,
            "ujsag": "origo"
        }
    )
    
if __name__ == "__main__":

    start_time = time.time() 

    with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        executor.map(get_origo_texts, linkek)

    total_time = time.time() - start_time

    print(total_time)

    pd.DataFrame(data).to_parquet("origo_data.parquet")