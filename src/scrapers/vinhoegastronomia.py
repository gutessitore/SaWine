import pandas as pd
from tqdm import tqdm
from trafilatura.sitemaps import sitemap_search
from trafilatura import fetch_url, extract
import time

def url_site(resource_url: str) -> list:

    urls = sitemap_search(resource_url)
    return urls


def extrator_artigos(url: str) -> dict:
    download = fetch_url(url)
    time.sleep(25)
    artigos = extract(download, favor_precision=True)
    
    return artigos


def criador_dataset(linkSites: list) -> pd.DataFrame:

    data = []
    for sites in tqdm(linkSites, desc="sites"):
        urls =url_site(sites)
        for url in tqdm(urls, desc="URLs"):
            d = {
                'url': url,
                "texto": extrator_artigos(url)
            }
            data.append(d)
            time.sleep(0.5)

    df = pd.DataFrame(data)
    df = df.drop_duplicates()
    df = df.dropna()

    return df


if __name__ == "__main__":
    
    linkSites = [
        "https://www.vinhoegastronomia.com.br/"

    ]

    df = criador_dataset(linkSites)

# Salvando o dataframe em um arquivo csv
df.to_csv("../data/vinhoegastronomia.csv", index=False)