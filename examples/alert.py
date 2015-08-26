import logging
import telegram
import time
import random
import lxml.html
from lxml.cssselect import CSSSelector
import urllib
import re
import operator
import datetime
import sys
import feedparser

LAST_UPDATE_ID = None


def main():
    global LAST_UPDATE_ID
    global startedPoint
    startedPoint = datetime.datetime.now().isoformat(' ')
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Telegram Bot Authorization Token
    bot = telegram.Bot('113159405:AAEj45hKxELGRWADLQ7YYO01fgSWbTLP4G0')

    # This will be our global variable to keep the latest update_id when requesting
    # for updates. It starts with the latest update_id if available.
    try:
        LAST_UPDATE_ID = bot.getUpdates()[-1].update_id
    except IndexError:
        LAST_UPDATE_ID = None

    global newRelicFeed
    newRelicFeed = feedparser.parse('https://rpm.newrelic.com/accounts/857072/applications/9351884/incidents.rss?data_access_key=b5e5145b73b9a5c571843470b1c87ddad1aa11ae0b724a5')
    global currAlert
    currAlert = newRelicFeed.entries[0]['link']
    while True:
        echo(bot)
        time.sleep(20)


def echo(bot):
    global LAST_UPDATE_ID
    
    # Request updates from last updated_id
    for update in bot.getUpdates(offset=LAST_UPDATE_ID):
        if LAST_UPDATE_ID < update.update_id:
            # chat_id is required to reply any message
            first_name = update.message.from_user.first_name.encode('utf-8')
            last_name = update.message.from_user.last_name.encode('utf-8')
            chat_id = update.message.chat_id
            message = update.message.text.encode('utf-8')
            user_id = update.message.from_user.id

            newRelicFeed = feedparser.parse('https://rpm.newrelic.com/accounts/857072/applications/9351884/incidents.rss?data_access_key=b5e5145b73b9a5c571843470b1c87ddad1aa11ae0b724a5')
            
            latestAlert = newRelicFeed.entries[0]['link']
            global currAlert
            isUpdated = (currAlert != latestAlert)
            
            if message == '/getAlert':
                fullAlert = newRelicFeed.entries[0]
                alertText = '================= NewRelic Alert =================\n\n' + fullAlert['title'] + "\n" + fullAlert['description'] 
                bot.sendMessage(chat_id=chat_id,text=alertText)

            if isUpdated:
                # Send alert
                fullAlert = newRelicFeed.entries[0]
                alertText = '================= NewRelic Alert =================\n\n' + fullAlert['title'] + "\n" + fullAlert['description'] 
                bot.sendMessage(chat_id=chat_id,text=alertText)

                # Update latest alert
                currAlert = latestAlert
 
            LAST_UPDATE_ID = update.update_id

if __name__ == '__main__':
    main()
