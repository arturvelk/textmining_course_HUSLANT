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
    .loc[lambda _df: _df["ujsag"] == "telex", :]
    .iloc[:100,:]
    .url.to_list()
)

NUM_THREADS = 60
data = []
def get_telex_texts(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.content)
    try:
        title = soup.find(attrs={"class": "title-section__top"}).get_text().replace("\n", "").replace("  ", "")
    except:
        title = ""

    try:
        text = " ".join(
            [
                item.get_text().strip()
                for item in soup.find(attrs={"class": "article_body_"}).find_all("p")
                #itt minden telexes cikk végén van egy hintbox, hogy fizess nekik, ezt most nemtudom hogy hogyan lehet ksizedni.
            ]
        )
    except:
        text = ""
    data.append(
        {
            "title": title,
            "text": text,
            "url" : link,
            "ujsag": "telex"
        }
    )
if __name__ == "__main__":
        
    start_time = time.time() 

    with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        executor.map(get_telex_texts, linkek)

    total_time = time.time() - start_time

    print(total_time)

    pd.DataFrame(data).to_parquet("telex_data.parquet")