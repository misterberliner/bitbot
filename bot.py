# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 23:26:41 2017

@author: Aykut-pc
"""
import cfscrape
import requests
import json
import datetime
import time

class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=5):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, text):
        params = {'chat_id': -257842711, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = {u'message': {u'chat': {u'all_members_are_administrators': True,
   u'id': -257842711,
   u'title': u'Arbit',
   u'type': u'group'},
  u'date': 1514137735,
  u'entities': [{u'length': 9, u'offset': 0, u'type': u'bot_command'}],
  u'from': {u'first_name': u'Aykut',
   u'id': 277329448,
   u'is_bot': False,
   u'language_code': u'en',
   u'last_name': u'Isleyen'},
  u'message_id': 125,
  u'text': u'/hgarbitraj'},
 u'update_id': 843898961}

        return last_update

arbot = BotHandler("448035992:AAGKXknjD3DjwFlUFPMJjWV7FksQxtHH6cI")
now = datetime.datetime.now()

def databtcturk():
    #retrieve data from BTCTURK
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    sess = requests.session()
    sess = cfscrape.create_scraper(sess)
    btcturkresponse = sess.get("https://www.btcturk.com/api/ticker?pairSymbol=BTCTRY",headers=headers)
    btcturk_data = json.loads(btcturkresponse.text)
    
    if btcturkresponse.status_code == 200:
        btcturk = btcturk_data["bid"]
    else:
        btcturk = 0
    return btcturk

# Ddos protectiondan kaçmak için denediğim ilk yöntem
#def start_requests(url):
#    token,agent = cfscrape.get_tokens(url)
#    cf_requests= (scrapy.Request(url=url,
#                      cookies={'__cfduid': token['__cfduid']},
#                      headers={'User-Agent': agent}))
#    return cf_requests
#aa=start_requests("https://www.bitpanda.com/api/ticker")

def dataanycoin():
    #retrieve data from anycoindirect
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    sess = requests.session()
    sess = cfscrape.create_scraper(sess)
    anycoinresponse = sess.get("https://anycoindirect.eu/api/public/buyprices?CoinCode=BTC&FiatCode=EUR&CoinAmount=1", headers=headers)
    anycoinonay = anycoinresponse.status_code #200 olması lazım
    
    if anycoinonay == 200:    
        anycoin_data = json.loads(anycoinresponse.text)
        if anycoin_data["Data"][3]["Name"] == u'iDEAL' and anycoin_data["HasErrors"] == False:
            anycoin = anycoin_data["Data"][3]["FiatAmount"]
        else:
            anycoin = 0
    else:
        anycoin = 0
    return anycoin
        
def databitpanda():
    #data from bitpanda
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    bsess = requests.Session()
    bsess = cfscrape.create_scraper(bsess)
    bitpandaresponse = bsess.get("https://www.bitpanda.com/api/ticker", headers=headers)
    bitpandaonay = bitpandaresponse.status_code
    if bitpandaonay == 200:
        bitpandaresponse_data = json.loads(bitpandaresponse.text)
        bitpanda = 1
    else:
        bitpanda = 0
    return bitpanda

def databitonic():
    #retrieve data from bitonic.nl
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    sess = requests.Session()
    sess = cfscrape.create_scraper(sess)
    bitonicresponse = sess.get("https://bitonic.nl/api/buy?btc=1", headers=headers)
    bitoniconay = bitonicresponse.status_code
    if bitoniconay == 200:
        bitonic_data = json.loads(bitonicresponse.text)
        bitonic = bitonic_data["eur"]
    else:
        bitonic = 0
    return bitonic

def tryeur():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    sess = requests.Session()
    sess = cfscrape.create_scraper(sess)
    kurresponse = sess.get("https://www.doviz.com/api/v1/currencies/all/latest", headers=headers)
    kuronay = kurresponse.status_code
    if kuronay == 200:
        kur_data = json.loads(kurresponse.text)
        kur = kur_data[1]["selling"]
    else:
        kur = 0
    return kur


def main():  
    new_offset = None
    ticks=1

    ep = time.time()
    while True:
        
        arbot.get_updates(new_offset)
        last_update = arbot.get_last_update()
        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        
        
        btcturk = databtcturk()
        bitonic = databitonic()
        bitpanda=databitpanda()
        anycoin= dataanycoin()
        kur = tryeur()
        if last_chat_text == "/arbitraj":
            btcturkeuro = int(btcturk / kur)
            arbot.send_message("Euro kuru:\n " + str(kur))
            arbot.send_message("BtcTurk:\n 1 BTC: " + str(btcturk) + " TL\n 1 BTC: " + str(btcturkeuro) + " €")
            arbot.send_message("Bitonic:\n 1 BTC: " + str(bitonic) + " €\n Arbitraj:\n " + str(-bitonic+btcturkeuro) + " €")
            arbot.send_message("Anycoin:\n 1 BTC: " + str(anycoin) + " €\n Arbitraj:\n " + str(-anycoin+btcturkeuro) + " €")
            arbot.send_message("Bitpanda:\n 1 BTC: " + str(bitpanda) + " €\n Arbitraj:\n " + str(-bitpanda+btcturkeuro) + " €")
        
        
        if time.time()-ep > 60*60*6*ticks:
            ticks +=1
            btcturkeuro = int(btcturk / kur)
            arbot.send_message("Euro kuru:\n " + str(kur))
            arbot.send_message("BtcTurk:\n 1 BTC: " + str(btcturk) + " TL\n 1 BTC: " + str(btcturkeuro) + " €")
            arbot.send_message("Bitonic:\n 1 BTC: " + str(bitonic) + " €\n Arbitraj:\n " + str(-bitonic+btcturkeuro) + " €")
            arbot.send_message("Anycoin:\n 1 BTC: " + str(anycoin) + " €\n Arbitraj:\n " + str(-anycoin+btcturkeuro) + " €")
            arbot.send_message("Bitpanda:\n 1 BTC: " + str(bitpanda) + " €\n Arbitraj:\n " + str(-bitpanda+btcturkeuro) + " €")    
        
        new_offset = last_update_id + 1
        time.sleep(1)
        

if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()
