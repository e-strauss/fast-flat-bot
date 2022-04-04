import requests
from bs4 import BeautifulSoup

url1 = 'https://www.immonet.de/immobiliensuche/sel.do?pageoffset=1&listsize=26&objecttype=1&locationname=Prenzlauer+Berg%2C+Berlin&acid=&actype=&district=7899&ajaxIsRadiusActive=true&sortby=0&suchart=2&radius=0&pcatmtypes=1_2&pCatMTypeStoragefield=1_2&parentcat=1&marketingtype=2&fromprice=&toprice=800&fromarea=&toarea=&fromplotarea=&toplotarea=&fromrooms=&torooms=2%2C5&objectcat=-1&wbs=-1&fromyear=&toyear=&fulltext=&absenden=Ergebnisse+anzeigen'
url2 = 'https://www.wg-gesucht.de/1-zimmer-wohnungen-in-Berlin.8.1.1.0.html?offer_filter=1&city_id=8&noDeact=1&categories%5B%5D=1&rent_types%5B%5D=0&rMax=600'
url3 = 'https://www.gewobag.de/fuer-mieter-und-mietinteressenten/mietangebote/?bezirke%5B%5D=pankow&bezirke%5B%5D=pankow-prenzlauer-berg&nutzungsarten%5B%5D=wohnung&gesamtmiete_von=&gesamtmiete_bis=&gesamtflaeche_von=&gesamtflaeche_bis=&zimmer_von=&zimmer_bis=&sort-by=recent'
url4 = 'https://www.gewobag.de/fuer-mieter-und-mietinteressenten/mietangebote/?bezirke%5B%5D=reinickendorf-tegel&nutzungsarten%5B%5D=wohnung&gesamtmiete_von=&gesamtmiete_bis=&gesamtflaeche_von=&gesamtflaeche_bis=&zimmer_von=&zimmer_bis=&sort-by=recent'
html = requests.get(url3)
html = BeautifulSoup(html.text, 'html.parser')
res = html.find("div",{"class":"empty-mietangebote"})
if res != None:
    print(res)
else:
    print("gucci")

""" f = open("gewobag.html","x")
f.write(html.text)
f.close() """