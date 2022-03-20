#!/usr/bin/python3
from crawltest import crawl, crawl3
import telegram_send as tel
import time
import requests
import random as r
import json
from pprint import pprint
import numpy as np
""" import traceback
import sys """

bot_token1 = '5123356978:AAHrY1PCU_-kMbxtErWgaya5Dk2-iBpVYds'
bot_token2 = '5229882542:AAFNrowB-fESDGB7Uk6d6XDIpnjls-ZQu6Q'

#curl https://api.telegram.org/bot5123356978:AAHrY1PCU_-kMbxtErWgaya5Dk2-iBpVYds/getUpdates
#curl https://api.telegram.org/bot5229882542:AAFNrowB-fESDGB7Uk6d6XDIpnjls-ZQu6Q/getUpdates
#c_ids = ['402154439', '2091019492']
c_ids = ['402154439']
update_id = '402154439'
update_id_int = 402154439
url2 = 'https://www.immobilienscout24.de/Suche/de/berlin/berlin/wohnung-mieten?numberofrooms=-3.5&price=-950.0&exclusioncriteria=swapflat&pricetype=calculatedtotalrent&geocodes=1100000001,1100000003,110000000201&sorting=2'
url3 = 'https://www.gewobag.de/fuer-mieter-und-mietinteressenten/mietangebote/?bezirke%5B%5D=pankow&bezirke%5B%5D=pankow-prenzlauer-berg&nutzungsarten%5B%5D=wohnung&gesamtmiete_von=&gesamtmiete_bis=&gesamtflaeche_von=&gesamtflaeche_bis=&zimmer_von=&zimmer_bis=&sort-by=recent'
url4 = 'https://www.gesobau.de/mieten/wohnungssuche.html?id=2&tx_kesearch_pi1%5Bsword%5D=&tx_kesearch_pi1%5Bzimmer%5D=&tx_kesearch_pi1%5BflaecheMin%5D=&tx_kesearch_pi1%5BmieteMax%5D=&tx_kesearch_pi1%5Bregions%5D%5B%5D=16&tx_kesearch_pi1%5Bregions%5D%5B%5D=4&tx_kesearch_pi1%5Bregions%5D%5B%5D=43&tx_kesearch_pi1%5Bregions%5D%5B%5D=48&tx_kesearch_pi1%5Bregions%5D%5B%5D=42&tx_kesearch_pi1%5Bregions%5D%5B%5D=11&tx_kesearch_pi1%5Bregions%5D%5B%5D=36&tx_kesearch_pi1%5Bpage%5D=1&tx_kesearch_pi1%5BresetFilters%5D=0&tx_kesearch_pi1%5BsortByField%5D=&tx_kesearch_pi1%5BsortByDir%5D=asc#ergebnisliste-anker'
url5 = 'https://www.gewobag.de/fuer-mieter-und-mietinteressenten/mietangebote/?bezirke%5B%5D=pankow&bezirke%5B%5D=pankow-prenzlauer-berg&nutzungsarten%5B%5D=wohnung&gesamtmiete_von=&gesamtmiete_bis=&gesamtflaeche_von=&gesamtflaeche_bis=&zimmer_von=&zimmer_bis=&sort-by=recent'
update_timer = 10
telegram_url = "https://api.telegram.org/bot"
reset = 0

crawling_active = True

try:
    telegram_update_ids = np.load("telegram_update_ids.npy").tolist()
except:
    telegram_update_ids = []

if reset:
    telegram_update_ids = []

def sendtext(bot_message, bot_chatID, bot_token):
    send_text = telegram_url + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()

def pull_instructions():
    tmp_url = telegram_url + bot_token2 + "/getUpdates"
    res = requests.get(tmp_url).json()
    if res["ok"]:
        for update in res["result"]:
            if not update["update_id"] in telegram_update_ids:
                telegram_update_ids.append(update["update_id"])
                np.save("telegram_update_ids.npy", telegram_update_ids)
                message = update["message"]
                #pprint(message)
                if message["from"]["id"] == update_id_int:
                    evaluate_instruction(message["text"])

def evaluate_instruction(inst):
    if inst[0] == '/':
        print("received instruction")
        global crawling_active
        if inst == '/start':
            print("starting crawling")
            crawling_active = True
            sendtext("set crawling to active", update_id, bot_token2)
            return
        if inst == '/stop':
            print("stopping crawling")
            crawling_active = False
            res = sendtext("deactivated crawling", update_id, bot_token2)
            print(res)
        print("hi")

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

timeout_a = 5
timeout_b = 5
messages_on = 1

def main():
    for chat in c_ids:
        if messages_on:
            print(sendtext("flat crawler initiated [Demo Version]", chat, bot_token1))
    i = 0
    k = 0
    while True:
        pull_instructions()
        if crawling_active:
            print("periodic crawling nr " + str(i))
            evaluate_crawl_response(crawl(url3), url3)
            time.sleep(r.randint(timeout_a,timeout_b))
            evaluate_crawl_response(crawl3(url4), url4)
            time.sleep(r.randint(timeout_a,timeout_b))
            if i % update_timer == 0:
                i = 0
                if messages_on:
                    sendtext("still running nr: " + str(k), update_id, bot_token2)
                k += 1
            i+=1
        else:
            print("no")
            time.sleep(15)

if __name__ == "__main__":
    #main()
    try:
        main()
    except Exception as e:
        """ tb = sys.exc_info()[-1]
        stk = traceback.extract_tb(tb, 1)
        fname = stk[0][2] """
        sendtext(str(e), update_id, bot_token2)