#!/usr/bin/python3
from crawltest import crawl, crawl3
import time
import requests
import random as r
import boto3

bot_token1 = '5123356978:AAHrY1PCU_-kMbxtErWgaya5Dk2-iBpVYds'
bot_token2 = '5229882542:AAFNrowB-fESDGB7Uk6d6XDIpnjls-ZQu6Q'

#curl https://api.telegram.org/bot5123356978:AAHrY1PCU_-kMbxtErWgaya5Dk2-iBpVYds/getUpdates
#curl https://api.telegram.org/bot5229882542:AAFNrowB-fESDGB7Uk6d6XDIpnjls-ZQu6Q/getUpdates
c_ids = ['402154439', '2091019492']
c_ids = ['402154439']
update_id = '402154439'
update_id_int = 402154439
url2 = 'https://www.immobilienscout24.de/Suche/de/berlin/berlin/wohnung-mieten?numberofrooms=-3.5&price=-950.0&exclusioncriteria=swapflat&pricetype=calculatedtotalrent&geocodes=1100000001,1100000003,110000000201&sorting=2'
url3 = 'https://www.gewobag.de/fuer-mieter-und-mietinteressenten/mietangebote/?bezirke%5B%5D=pankow&bezirke%5B%5D=pankow-prenzlauer-berg&nutzungsarten%5B%5D=wohnung&gesamtmiete_von=&gesamtmiete_bis=&gesamtflaeche_von=&gesamtflaeche_bis=&zimmer_von=&zimmer_bis=&sort-by=recent'
url4 = 'https://www.gesobau.de/mieten/wohnungssuche.html?id=2&tx_kesearch_pi1%5Bsword%5D=&tx_kesearch_pi1%5Bzimmer%5D=&tx_kesearch_pi1%5BflaecheMin%5D=&tx_kesearch_pi1%5BmieteMax%5D=&tx_kesearch_pi1%5Bregions%5D%5B%5D=16&tx_kesearch_pi1%5Bregions%5D%5B%5D=4&tx_kesearch_pi1%5Bregions%5D%5B%5D=43&tx_kesearch_pi1%5Bregions%5D%5B%5D=48&tx_kesearch_pi1%5Bregions%5D%5B%5D=42&tx_kesearch_pi1%5Bregions%5D%5B%5D=11&tx_kesearch_pi1%5Bregions%5D%5B%5D=36&tx_kesearch_pi1%5Bpage%5D=1&tx_kesearch_pi1%5BresetFilters%5D=0&tx_kesearch_pi1%5BsortByField%5D=&tx_kesearch_pi1%5BsortByDir%5D=asc#ergebnisliste-anker'
url5 = 'https://www.gewobag.de/fuer-mieter-und-mietinteressenten/mietangebote/?bezirke_all=1&bezirke%5B%5D=charlottenburg-wilmersdorf&bezirke%5B%5D=charlottenburg-wilmersdorf-charlottenburg&bezirke%5B%5D=charlottenburg-wilmersdorf-nord&bezirke%5B%5D=friedrichshain-kreuzberg&bezirke%5B%5D=friedrichshain-kreuzberg-friedrichshain&bezirke%5B%5D=friedrichshain-kreuzberg-kreuzberg&bezirke%5B%5D=lichtenberg&bezirke%5B%5D=lichtenberg-alt-hohenschoenhausen&bezirke%5B%5D=lichtenberg-falkenberg&bezirke%5B%5D=lichtenberg-fennpfuhl&bezirke%5B%5D=lichtenberg-friedrichsfelde&bezirke%5B%5D=marzahn-hellersdorf&bezirke%5B%5D=marzahn-hellersdorf-marzahn&bezirke%5B%5D=neukoelln&bezirke%5B%5D=neukoelln-britz&bezirke%5B%5D=neukoelln-buckow&bezirke%5B%5D=neukoelln-rudow&bezirke%5B%5D=pankow&bezirke%5B%5D=pankow-prenzlauer-berg&bezirke%5B%5D=reinickendorf&bezirke%5B%5D=reinickendorf-hermsdorf&bezirke%5B%5D=reinickendorf-tegel&bezirke%5B%5D=reinickendorf-waidmannslust&bezirke%5B%5D=spandau&bezirke%5B%5D=spandau-hakenfelde&bezirke%5B%5D=spandau-haselhorst&bezirke%5B%5D=spandau-staaken&bezirke%5B%5D=steglitz-zehlendorf&bezirke%5B%5D=steglitz-zehlendorf-lichterfelde&bezirke%5B%5D=tempelhof-schoeneberg&bezirke%5B%5D=tempelhof-schoeneberg-lichtenrade&bezirke%5B%5D=tempelhof-schoeneberg-mariendorf&bezirke%5B%5D=tempelhof-schoeneberg-marienfelde&bezirke%5B%5D=tempelhof-schoeneberg-schoeneberg&bezirke%5B%5D=treptow-koepenick&bezirke%5B%5D=treptow-koepenick-alt-treptow&nutzungsarten%5B%5D=wohnung&gesamtmiete_von=&gesamtmiete_bis=&gesamtflaeche_von=&gesamtflaeche_bis=&zimmer_von=&zimmer_bis=&sort-by=recent'
update_timer = 10
telegram_url = "https://api.telegram.org/bot"
reset = 0

crawling_active = True

def sendtext(bot_message, bot_chatID, bot_token):
    send_text = telegram_url + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()

def check_telegram_id(dbt, id):
    dbt.reload()
    try:
        dbt.get_item(Key = {"ID": str(id)})["Item"]
        return False
    except:
        return True

def pull_instructions(dbt):
    tmp_url = telegram_url + bot_token2 + "/getUpdates"
    res = requests.get(tmp_url).json()
    if res["ok"]:
        for update in res["result"]:
            if check_telegram_id(dbt, update["update_id"]):
                dbt.put_item(Item = {"ID" : str(update["update_id"]), "info" : {"data" : str(update["update_id"])}})
                message = update["message"]
                #pprint(message)
                if message["from"]["id"] == update_id_int:
                    evaluate_instruction(message["text"])

def evaluate_instruction(inst):
    if inst[0] == '/':
        print("received instruction")
        inst = inst.split()
        global crawling_active
        if inst[0] == '/start':
            print("starting crawling")
            crawling_active = True
            sendtext("set crawling to active", update_id, bot_token2)
            return
        if inst[0] == '/stop':
            print("stopping crawling")
            crawling_active = False
            sendtext("deactivated crawling", update_id, bot_token2)
            return
        if inst[0] == '/timeout':
            print("setting timout")
            if len(inst) != 3:
                sendtext("usage: timeout timeMin timeMax", update_id, bot_token2)
            global timeout_a 
            timeout_a = int(inst[1])
            global timeout_b 
            timeout_b = int(inst[2])
            sendtext("set timeouts to " + str(timeout_a) + " " + str(timeout_b), update_id, bot_token2)
            return
        if inst[0] == '/sleep':
            crawling_active = False
            global time_sleep
            if len(inst) != 2:
                sendtext("usage: sleep time", update_id, bot_token2)
            time_sleep = int(inst[1])*60
            sendtext("set sleep time to " + str(time_sleep) + "seconds", update_id, bot_token2)
            return
        if inst[0] == '/adduser':
            if len(inst) != 2:
                sendtext("usage: adduser ID", update_id, bot_token2)
            global c_ids
            c_ids.append(inst[1])
        print("couldn't decode instruction")

def evaluate_crawl_response(res, url):
    if res == None:
        sendtext("couldn't connect to the server: " + url, update_id, bot_token2)
        return
    if len(res) > 0:
        print("found something")
        for r in res:
            for chat in c_ids:
                res = sendtext(r, chat, bot_token1)
                print(res)
                sendtext(str(res), update_id, bot_token2)

timeout_a = 15
timeout_b = 45
time_sleep = 15
messages_on = 1

def main():
    dynamodb = boto3.resource('dynamodb',region_name='eu-central-1')
    db_table = dynamodb.Table('FastFlatBot-TelegramIDs')
    db_table2 = dynamodb.Table('FastFlatBot-FlatIDs')
    for chat in c_ids:
        if messages_on:
            print(sendtext("flat crawler initiated [Demo Version]", chat, bot_token1))
    i = 0
    k = 0
    while True:
        pull_instructions(db_table)
        if crawling_active:
            print("periodic crawling nr " + str(i))
            evaluate_crawl_response(crawl(url5, db_table2), url5)
            time.sleep(r.randint(timeout_a,timeout_b))
            evaluate_crawl_response(crawl3(url4, db_table2), url4)
            time.sleep(r.randint(timeout_a,timeout_b))
        else:
            print("not crawling")
            time.sleep(time_sleep)
        if i % update_timer == 0:
            i = 0
            if messages_on:
                sendtext("still running nr: " + str(k) + ", status : " + str(crawling_active), update_id, bot_token2)
            k += 1
        i+=1

if __name__ == "__main__":
    main()
    try:
        main()
    except Exception as e:
        sendtext(str(e), update_id, bot_token2)