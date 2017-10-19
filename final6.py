import os, sys, time, telepot, unicodedata, urllib3, wikiquote, random
from telepot.loop import MessageLoop
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as soup
from time import gmtime, strftime
from tabulate import tabulate

token = os.environ['TELEGRAM_TOKEN']
some_api_token = os.environ['SOME_API_TOKEN']
#BeautifulSoup 
def scrap():
    url = 'http://www.meteokav.gr/weather/'
    req = urlopen(url)
    page = req.read()
    req.close()
    page_soup = soup(page, "html.parser")
    values_list = [
    ['Θερμοκρασία:', page_soup.find("span", {"id":"ajaxtemp"}).text.strip()[0:6]],
    [page_soup.find_all("strong")[19].text.strip(), page_soup.find("span", {"id":"ajaxhumidity"}).text.strip()+"%"],
    ['Αίσθηση σαν: ' , page_soup.find("span", {"id":"ajaxfeelslike"}).text.strip()],
    ['Διαφορά 24ώρου: ', page_soup.find_all("strong")[0].text.strip()],
    [ 'Διαφορά ώρας: ', page_soup.find_all("strong")[1].text.strip()],
    ['Ανεμος: ' + page_soup.find("span", {"id":"ajaxwinddir"}).text.strip() + "@" + page_soup.find("span", {"id":"ajaxbeaufortnum"}).text.strip()+" Bft"], 
    [page_soup.find_all("strong")[21].text.strip() +' '+ page_soup.find("span", {"id":"ajaxbaro"}).text.strip() +" "+ page_soup.find("span", {"id":"ajaxbarotrendtext"}).text.strip()],
    ['Βροχή Σήμερα: ' +  page_soup.find("span", {"id":"ajaxrain"}).text.strip()],
     #[page_soup.find("td", {"colspan":"2"}).find_all("tr")[1].find_all("td")[0].text.strip() +
    ['Μέγιστη Σήμερα: '+ page_soup.find("table", {"class":"data1"}).find_all('tr')[1].find_all('td')[1].text.strip()[0:6] +'@'+ page_soup.find("table", {"class":"data1"}).find_all('tr')[1].find_all('td')[1].text.strip()[-6:]],
    #    [page_soup.find("td", {"colspan":"2"}).find_all("tr")[1].find_all("td")[0].text.strip() +
    ['Μέγιστη Χθες: '+ page_soup.find("table", {"class":"data1"}).find_all('tr')[1].find_all('td')[2].text.strip()[0:6] +'@'+ page_soup.find("table", {"class":"data1"}).find_all('tr')[1].find_all('td')[2].text.strip()[-6:]],
    ['Ελάχιστη Σήμερα: ' + page_soup.find("table", {"class":"data1"}).find_all('tr')[2].find_all('td')[1].text.strip()[0:4]+'@'+ page_soup.find("table", {"class":"data1"}).find_all('tr')[2].find_all('td')[1].text.strip()[-5:]],
    ['Ελάχιστη Χθες: ' + page_soup.find("table", {"class":"data1"}).find_all('td')[5].text.strip()[0:4] +'@'+ page_soup.find("table", {"class":"data1"}).find_all('td')[5].text.strip()[-5:]],
    [ page_soup.find_all("strong")[20].text.strip() +' '+ page_soup.find("span", {"id":"ajaxdew"}).text.strip()],
    ['MAX_'+ page_soup.find_all("strong")[19].text.strip() +' '+ page_soup.find("td", {"rowspan":"3"}).find_all('tr')[1].find_all('td')[1].text.strip()[0:3] +'@'+ page_soup.find("td", {"rowspan":"3"}).find_all('tr')[1].find_all('td')[1].text.strip()[-5:]], 
    ["MAX_Baro: " + page_soup.find("td", {"rowspan":"3"}).find_all('tr')[6].find_all('td')[1].text.strip()[0:10] +'@'  + page_soup.find("td", {"rowspan":"3"}).find_all('tr')[6].find_all('td')[1].text.strip()[-5:]],
    ["MIN_Baro: " + page_soup.find("td", {"rowspan":"3"}).find_all('tr')[7].find_all('td')[1].text.strip()[0:10]+'@'+ page_soup.find("td", {"rowspan":"3"}).find_all('tr')[7].find_all('td')[1].text.strip()[-5:]]
     ]
    return tabulate(values_list)

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(msg, content_type, chat_type, chat_id, strftime("%a, %d %b %Y %H:%M:%S +0000"))

    if content_type == 'text':
        bot.sendMessage(chat_id, scrap())

TOKEN = '465434046:AAHZLWGbW2WfCmx1AWi6sfjOMm_tNVrMkW4'

bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(1)

