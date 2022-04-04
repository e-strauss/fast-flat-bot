#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
from pprint import pprint
import time as t

url2 = 'https://www.immobilienscout24.de/Suche/de/berlin/berlin/wohnung-mieten?numberofrooms=-3.5&price=-950.0&exclusioncriteria=swapflat&pricetype=calculatedtotalrent&geocodes=1100000001,1100000003,110000000201&sorting=2'
url3 = 'https://www.gewobag.de/fuer-mieter-und-mietinteressenten/mietangebote/?bezirke%5B%5D=pankow&bezirke%5B%5D=pankow-prenzlauer-berg&nutzungsarten%5B%5D=wohnung&gesamtmiete_von=&gesamtmiete_bis=&gesamtflaeche_von=&gesamtflaeche_bis=&zimmer_von=&zimmer_bis=&sort-by=recent'
url4 = 'https://www.gesobau.de/mieten/wohnungssuche.html?id=2&tx_kesearch_pi1%5Bsword%5D=&tx_kesearch_pi1%5Bzimmer%5D=&tx_kesearch_pi1%5BflaecheMin%5D=&tx_kesearch_pi1%5BmieteMax%5D=&tx_kesearch_pi1%5Bregions%5D%5B%5D=16&tx_kesearch_pi1%5Bregions%5D%5B%5D=4&tx_kesearch_pi1%5Bregions%5D%5B%5D=43&tx_kesearch_pi1%5Bregions%5D%5B%5D=48&tx_kesearch_pi1%5Bregions%5D%5B%5D=42&tx_kesearch_pi1%5Bregions%5D%5B%5D=11&tx_kesearch_pi1%5Bregions%5D%5B%5D=36&tx_kesearch_pi1%5Bpage%5D=1&tx_kesearch_pi1%5BresetFilters%5D=0&tx_kesearch_pi1%5BsortByField%5D=&tx_kesearch_pi1%5BsortByDir%5D=asc#ergebnisliste-anker'

def load_html(url):
    c = False
    i = 0
    while i < 5 and not c:
        start = t.time()
        try:
            data = requests.get(url)
        except:
            print("not connecting")
            pass
        else:
            c = True
        end = t.time()
        print("request time: " + str(end - start))
        i += 1
    if not c:
        return None
    if data.status_code == 200:
        pass
    elif data.status_code == 405:
        print("captcha")
    else:
        pprint("Got response (%i): %s" % (data.status_code, data.content))
    return BeautifulSoup(data.text, 'html.parser')

def check_flat_id(dbt, id):
    dbt.reload()
    try:
        dbt.get_item(Key = {"id": str(id)})["Item"]
        return False
    except:
        return True

def crawl(url, dbt):
    html = load_html(url)
    if html == None:
        return None
    res = html.find("div",{"class":"empty-mietangebote"})
    if res == None:
        return []
    res = html.find("div",{"class":"sync-info"})
    str = res.strong.text
    str = ''.join(c for c in str if c.isdigit())

    res = html.find("div", {"class" : "filtered-elements filtered-mietangebote no-pagination"})
    props = res.find_all("article")
    new = []
    for p in props:
        p_id = p["id"]
        if check_flat_id(dbt, "gewobag" + str(p_id)):
            dbt.put_item(Item = {"id" : "gewobag" + str(p_id), "info" : {"data" : "gewobag" + str(p_id) }})
            info = p.find("a", {"class" : "angebot-header"})
            new.append(info["href"])
            print("*** found new Gewobag proposal ID: " + p_id + " ***")
    return new

def crawl2(url):
    tml = load_html(url)

def crawl3(url, dbt):
    html = load_html(url)
    html = html.find_all('div', {'class' : "tab-content"})
    props = html[1].find_all("div",{"class":"bs4-col-sm-6 bs4-col-lg-4"})
    new =  []
    for p in props:
        p_id = p.find('div', {'class' : 'list_item'})['id']
        if check_flat_id(dbt, "gesobau" + str(p_id)):
            dbt.put_item(Item = {"id" : "gesobau" + str(p_id), "info" : {"data" : "gesobau" + str(p_id) }})
            print("*** found new Gesobau proposal ID: " + p_id + " ***")
            new.append("https://www.gesobau.de" + p.find('a')['href'])
    return new
        

def main():
    for i in range(1):
        print("periodic crawling nr " + str(i))
        #crawl3(url4)
        #crawl5("https://www.ivd24immobilien.de/search-photon/?osm_id=407652&osm_key=place&osm_value=suburb&osm_postcode=13156&osm_lat=52.5858062&osm_long=13.401397&nutzungsart_id=&vermarktungsart_id=10000000010&6234518fa072d=Niedersch%C3%B6nhausen&search_term=Niedersch%C3%B6nhausen&objektart_id=2&anzahl_zimmer=&preis_bis=&groesse_ab=&radius=0")
        t.sleep(1)

if __name__ == "__main__":
    main()
