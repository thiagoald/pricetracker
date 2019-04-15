#!/usr/bin/python2
import argparse
import traceback
from os.path import exists
from selenium import webdriver
from selenium.webdriver.common.by import By
import ipdb
from time import sleep
from random import random
from telegram_send import send
import re
from datetime import datetime
import pickle


def update_price_history(urls, xpaths, driver, history):
    for url, xpath in reversed(zip(urls, xpaths)):
        driver.get(url)
        sleep(10 + random()*10)
        el = driver.find_element(By.XPATH, xpath)
        send(['URL: {}'.format(url.split('.com.br')[0] + '.com.br')])
        send(['Price: {}'.format(el.text)])
        now = datetime.now()
        history[url][now] = float(re.findall(
            r'((?:\d+\.)?\d+),(\d+)', el.text)[0][0])
        send(['Price (removing cents): {}'.format(
            history[url][now])])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=('Monitor prices'))
    parser.add_argument('--save', dest='price_path', type=str, required=True,
                        help=('path to pickle with price history'))
    args = parser.parse_args()

    driver = webdriver.Chrome()

    urls = ['https://www.submarino.com.br/produto/11110021/piano-casio-digital-cdp-130?WT.srch=1&acc=d47a04c6f99456bc289220d5d0ff208d&epar=bp_pl_00_go_g35175&gclid=Cj0KCQjw19DlBRCSARIsAOnfReg0oOYhB-Z9e5baR_6pmTsOGcqR5vo0dUsQtXVdKvBpF2Cw9ki8aA8aArZvEALw_wcB&i=561e51156ed24cafb531b545&o=57b79bcdeec3dfb1f86e55ea&opn=XMLGOOGLE&sellerId=9055134000184',
            'https://www.americanas.com.br/produto/11110021/piano-casio-digital-cdp-130?WT.srch=1&acc=e789ea56094489dffd798f86ff51c7a9&epar=bp_pl_00_go_im_todas_geral_gmv&gclid=Cj0KCQjw19DlBRCSARIsAOnfReiVThiS401KKXZCUl5B4hPwQfmY2gaSul4CQw0FPpkzPKQfi1R6RrAaAhugEALw_wcB&i=55ef647d6ed24cafb524af04&o=57b76ef4eec3dfb1f865ed0a&opn=YSMESP&sellerId=9055134000184',
            'https://www.shoptime.com.br/produto/11110021/piano-casio-digital-cdp-130?WT.srch=1&acc=a76c8289649a0bef0524c56c85e71570&epar=bp_pl_00_go_im_todas_geral_gmv&gclid=Cj0KCQjw19DlBRCSARIsAOnfRei-6JZrmz0zi-xklMxUUZbbnvZCFIBop2UjSS2cEfRAsnNyw8a_JjQaAnqFEALw_wcB&i=5616c63a6ed24cafb5401d32&o=57f3dd0aeec3dfb1f81374c5&opn=GOOGLEXML&sellerId=9055134000184',
            'https://www.girafa.com.br/teclas/Casio/piano-digital-casio-cdp-130bk-midi-preto-com-88-teclas.htm?gclid=Cj0KCQjw19DlBRCSARIsAOnfReiFVOVNghlymnhlW2NVgyJ0rlOhWCYutP4RGn6KnpZ2pZk5Ime28g4aAjSsEALw_wcB',
            'https://www.magazineluiza.com.br/piano-digital-cdp130-bk-casio-preto-88-teclas-sensitivas-/p/fc820a195j/im/ispi/?&utm_source=google&partner_id=17322&seller_id=supersonora&product_group_id=361752213757&ad_group_id=48543697915&aw_viq=pla&gclid=Cj0KCQjw19DlBRCSARIsAOnfRegT8tvF-Z-1gHp_p-ePfLxVU1xwpi0L3zQkIzJYy3u1cwY1PzbzrF4aAmutEALw_wcB']

    xpaths = ['//*[@id="content"]/div/div/section/div/div[2]/div[2]/section[2]/div/div[2]/div[1]/div[2]/p[3]/span',
              '//*[@id="offer-5b7d7e13172743a0f5bc9163"]/div/div[1]/div[2]/p[3]/span',
              '//*[@id="content"]/div/div/section/div/div[2]/div[2]/section[2]/div/div[2]/div[1]/div[2]/p[3]/span',
              '/html/body/article/div[3]/div[5]/div/div/div[2]/div[5]/div[2]/span[3]',
              '/html/body/div[3]/div[4]/div[1]/div[4]/div[2]/div[4]/div/div/div/span[2]']

    # TODO: Load from disk
    try:
        history = pickle.load(open(args.price_path, 'rb'))
    except:
        history = {}
        for url in urls:
            history[url] = {}

    while True:
        try:
            update_price_history(urls, xpaths, driver, history)
            pickle.dump(history, open(args.price_path, 'wb'))
            interval = 720 + 720*random()
            sleep(interval)
        except KeyboardInterrupt:
            traceback.print_exc()
            print('Saving price history in {}'.format(args.price_path))
            pickle.dump(history, open(args.price_path, 'wb'))
            print('Done!')
