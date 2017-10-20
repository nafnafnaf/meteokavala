import os, sys, time, telepot, unicodedata, urllib3, random
from telepot.loop import MessageLoop
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as soup
from time import gmtime, strftime
from tabulate import tabulate

TOKEN= os.environ['TELEGRAM_TOKEN']
#some_api_token = os.environ['SOME_API_TOKEN']

PORT = int(os.environ.get('PORT', '5000'))
updater = Updater(TOKEN)
# add handlers
updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN)
updater.bot.set_webhook("https://meteokavgr.herokuapp.com/" + TOKEN)
updater.idle()

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

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('Hi!')


def help(bot, update):
    update.message.reply_text('Help!')


def echo(bot, update):
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("TOKEN")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

