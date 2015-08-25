#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Simple Bot to reply Telegram messages
# Copyright (C) 2015 Leandro Toledo de Souza <leandrotoeldodesouza@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].


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



LAST_UPDATE_ID = None


def main():
    global LAST_UPDATE_ID
    global startedPoint
    startedPoint = datetime.datetime.now().isoformat(' ')
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Telegram Bot Authorization Token
    bot = telegram.Bot('82438901:AAFgzYUb4pQ_1qabUqY7fLJpBd4Ne7vJfLk')

    # This will be our global variable to keep the latest update_id when requesting
    # for updates. It starts with the latest update_id if available.
    try:
        LAST_UPDATE_ID = bot.getUpdates()[-1].update_id
    except IndexError:
        LAST_UPDATE_ID = None

    global helloed
    global byed
    helloed = []
    byed = []
    global thimRanking
    thimRanking = {}
    global thimDict
    thimDict = {}
    while True:
        echo(bot)
        time.sleep(1)


def echo(bot):
    global LAST_UPDATE_ID
    replies =["Thôi đi thím ","Lộn xộn quá thím ", "Mệt quá nha thím ", "Nhìu chiệng quá nha thím "]
    byes = ["Biến được rồi, níu kéo không hạnh phúc đâu thím ", "Mời! Không tiễn đâu thím ", "Đi thì đi đi, đợi đuổi hả thím "]
    # Request updates from last updated_id
    for update in bot.getUpdates(offset=LAST_UPDATE_ID):
        if LAST_UPDATE_ID < update.update_id:
            # chat_id is required to reply any message
            first_name = update.message.from_user.first_name.encode('utf-8')
            last_name = update.message.from_user.last_name.encode('utf-8')
            chat_id = update.message.chat_id
            message = update.message.text.encode('utf-8')
            user_id = update.message.from_user.id

            # Remove all @ThimBot from message
            if '@ThimBot' in message:
                message.replace('@ThimBot','')

            # Count thim call times
            if user_id not in thimRanking:
                thimDict[user_id] = first_name + " " + last_name

            # Record "thim" calling leaderboard
            if "thím" in message:
                if user_id in thimRanking:
                    thimRanking[user_id] += 1
                else:
                    thimRanking[user_id] = 1

            if message == '/thim' or message == '/thim@ThimBot':
                if len(thimRanking) == 0:
                    bot.sendMessage(chat_id=chat_id,text="Các thím ít gọi thím quá, làm sao ta trả lời ai 'thím' nhất Tiki được " + telegram.Emoji.PILE_OF_POO)
                    LAST_UPDATE_ID = update.update_id
                    return

                user_id_most = max(thimRanking.iteritems(), key=operator.itemgetter(1))[0]
                
                if len(thimRanking) < 3:
                    numtoPrint = len(thimRanking)
                else:
                    numtoPrint = 3

                leaderBoard = sorted(thimRanking.iteritems(), key=operator.itemgetter(1), reverse=True)[:numtoPrint]

                leaderBoardStr = "Tính từ lúc ta sống tới giờ (" + startedPoint+ "):\n\nGọi 'thím' nhiều nhất chỉ có thể là:\n"

                for user in leaderBoard:
                    leaderBoardStr += ">> " + str(thimRanking[user[0]]) + " lần - " + thimDict[user[0]]  + "\n"

                bot.sendMessage(chat_id=chat_id,text=leaderBoardStr)
                #LAST_UPDATE_ID = update.update_id
                #thimDict[user_id_most]

            if message == '/help':
                helpText = "Xin chào, ta là Thánh Thím Tiki. Ta có thể làm các việc sau:\n/chaothim - Chào thím, thím chào lại\n/byethim - Bai thím, thím bai luôn\n/thimwiki từ khoá --lang - thím tìm ra bài wiki gần với từ khoá nhứt\n\nCác thứ khác tự mò mới vui ;):\n\n /thimui\n/thimsanmoi hoặc 'thím săn mồi'\n/omg\n/whereisthim\n/det\n/fthim\n"
                bot.sendMessage(chat_id=chat_id,text=helpText + telegram.Emoji.RELIEVED_FACE)
                #LAST_UPDATE_ID = update.update_id

            if message == "/chaothim":
                if user_id not in helloed:
                    # Reply the message
                    bot.sendMessage(chat_id=chat_id,text="Chào thím "+ first_name + " " + telegram.Emoji.PILE_OF_POO)
                    helloed.append(update.message.from_user.id)
                else:
                    #bot.sendMessage(chat_id=chat_id, text=message)
                    bot.sendMessage(chat_id=chat_id, text= replies[random.randrange(len(replies))]+ first_name +", làm gì chào quài zậy.")

                # Updates global offset to get the new updates
                #LAST_UPDATE_ID = update.update_id

            if message == "/byethim":
                if user_id not in byed:
                    bot.sendMessage(chat_id=chat_id,text="Bái bai thím "+ first_name + " " + telegram.Emoji.PILE_OF_POO)
                    byed.append(update.message.from_user.id)
                else:
                    bot.sendMessage(chat_id=chat_id, text= byes[random.randrange(len(replies))]+ first_name)

                #LAST_UPDATE_ID = update.update_id

            if message == "/omg":
                bot.sendMessage(chat_id=chat_id,text="Con cứ bình tĩnh, mọi việc sẽ ổn cả thôi "+ telegram.Emoji.RELIEVED_FACE)

                #LAST_UPDATE_ID = update.update_id

            if message == "/whereisthim":
                bot.sendMessage(chat_id=chat_id,text="Ta đây, con cần gì, "+ first_name + "? " +telegram.Emoji.RELIEVED_FACE)

                #LAST_UPDATE_ID = update.update_id

            if "thím ơi" in message:
                oiReplies = ["Ta đây, con cần gì, ","Wểi... ","Ai gọi ta đó, có ta đâyyyyy "]
                bot.sendMessage(chat_id=chat_id,text= oiReplies[random.randrange(len(oiReplies))]+ first_name + "? " +telegram.Emoji.RELIEVED_FACE)

                #LAST_UPDATE_ID = update.update_id
            if message == '/det':
                bot.sendMessage(chat_id=chat_id,text="Đột...")
                #LAST_UPDATE_ID = update.update_id

            if ":(" in message:
                bot.sendMessage(chat_id=chat_id,text=first_name + " ơi, con đừng buồn..." +telegram.Emoji.RELIEVED_FACE)

                #LAST_UPDATE_ID = update.update_id

            if message == '/fthim':
                bot.sendMessage(chat_id=chat_id,text="Lượn đi cho nước nó trong "+ first_name + " à " +telegram.Emoji.RELIEVED_FACE)

                #LAST_UPDATE_ID = update.update_id

            if message == '/thimui':
                bot.sendMessage(chat_id=chat_id,text="http://uimovement.com/ui/"+str(random.randrange(1,170)))
                #LAST_UPDATE_ID = update.update_id

            if message == '/thimsanmoi' or message == 'thím săn mồi':
                bot.sendMessage(chat_id=chat_id,text="http://www.producthunt.com/tech/"+str(random.randrange(1,31396)))
                #LAST_UPDATE_ID = update.update_id

            if message == '/thimdaudo' or 'đậu đỏ' in message:
                daudoPhotos = {'aotuong':'../assets/img/aotuong.jpg',
                                'dethuong':'../assets/img/aotuong.jpg',
                                'nhiemmau':'../assets/img/nhiemmau.jpg',
                                'khomau':'../assets/img/khomau.jpg',
                                'gian':'../assets/img/gian.jpg',
                                'ghenha':'../assets/img/ghenha.jpg'
                                }
                listDau = ""
                if len(message.split()) == 1:
                    #Error handling
                    try:
                        bot.sendPhoto(chat_id=chat_id, photo=random.choice(daudoPhotos.values()))
                    except: # catch *all* exceptions
                        e = sys.exc_info()[0]
                        write_to_page( "<p>Error: %s</p>" % e )
                    
                else:
                    whichDau = message.split()[1]
                    if whichDau == 'help':
                        for key in daudoPhotos.keys():
                            listDau += key + "\n"
                    elif whichDau in daudoPhotos:
                        try:
                            bot.sendPhoto(chat_id=chat_id, photo=daudoPhotos[whichDau])
                        except: # catch *all* exceptions
                        e = sys.exc_info()[0]
                        write_to_page( "<p>Error: %s</p>" % e )
                    else:
                        try:
                            bot.sendPhoto(chat_id=chat_id, photo=random.choice(daudoPhotos.values()))
                        except: # catch *all* exceptions
                        e = sys.exc_info()[0]
                        write_to_page( "<p>Error: %s</p>" % e )

            if '/thimwiki' in message:
                if len(message.split()) < 2 :
                    bot.sendMessage(chat_id=chat_id,text="Cú pháp để hỏi ta là: /thimwiki từ-muốn-hỏi --lang=en/vi")
                    LAST_UPDATE_ID = update.update_id
                    return

                lang = 'en'
                if '--lang' in message:
                    langIdx = message.find('--lang')+7
                    lang = message[langIdx:]
                    message = messagep[:landIdx-7]

                query = message.replace('/thimwiki ','')
                
                url = "http://"+lang+".wikipedia.org/w/index.php?title=Special%3ASearch&profile=default&search="+query+"&fulltext=Search"
                resultPage = urllib.urlopen(url).read()

                if "There were no results matching the query." in resultPage:
                    bot.sendMessage(chat_id=chat_id,text="Thím hổng tìm ra gì trên Wiki cho cái này :(")
                    LAST_UPDATE_ID = update.update_id
                    return

                # build the DOM Tree
                tree = lxml.html.fromstring(resultPage)

                # construct a CSS Selector
                sel = CSSSelector('.mw-search-results>li:nth-child(1)')

                # Apply the selector to the DOM tree.
                results = sel(tree)
                # print the HTML for the first result.
                firstResult = results[0]
                sel2 = CSSSelector('li>div>a')

                a = sel2(firstResult)
                astr = lxml.html.tostring(a[0])

                href = re.search("(\"\/wiki\/)(.*?)\"",astr)
                gotoUrl = "http://"+lang+".wikipedia.org"+ href.group(0)[1:-1]
                
                #wikiPage = urllib.urlopen(gotoUrl).read()

                # build the DOM Tree
                #wtree = lxml.html.fromstring(wikiPage)

                # construct a CSS Selector
                #wsel = CSSSelector('#mw-content-text > p:nth-child(4)')

                # Apply the selector to the DOM tree.
                #firstParagraph = lxml.html.tostring(wsel(wtree)[0])
                #firstParagraph = re.sub("<.*?>", " ", firstParagraph).encode('utf-8')
                #print firstParagraph
                
                bot.sendMessage(chat_id=chat_id,text="Kết quả đầu tiên: " + gotoUrl)
            
            if '/thimgoogle' in message:
                if len(message.split()) < 2 :
                    bot.sendMessage(chat_id=chat_id,text="Cú pháp để hỏi ta là: /thimgoogle từ muốn kiếm")
                    LAST_UPDATE_ID = update.update_id
                    return

                query = ' '.join(message.split()[1:])
                q = {'q':query}
                url = "https://www.google.com/search?"+urllib.urlencode(q)
                resultPage = urllib.urlopen(url).read()

                if "did not match any documents" in resultPage:
                    bot.sendMessage(chat_id=chat_id,text="Thím hổng tìm ra gì trên Google cho cái này :(")
                    LAST_UPDATE_ID = update.update_id
                    return

                # build the DOM Tree
                tree = lxml.html.fromstring(resultPage)

                # construct a CSS Selector
                sel = CSSSelector('.r > a')

                # Apply the selector to the DOM tree.
                results = sel(tree)
                # print the HTML for the first result.
                firstResult = results[0]
                sel2 = CSSSelector('li>div>a')

                a = sel2(firstResult)
                astr = lxml.html.tostring(a[0])

                href = re.search("(\"\/wiki\/)(.*?)\"",astr)
                gotoUrl = "http://"+lang+".wikipedia.org"+ href.group(0)[1:-1]
                
                #wikiPage = urllib.urlopen(gotoUrl).read()

                # build the DOM Tree
                #wtree = lxml.html.fromstring(wikiPage)

                # construct a CSS Selector
                #wsel = CSSSelector('#mw-content-text > p:nth-child(4)')

                # Apply the selector to the DOM tree.
                #firstParagraph = lxml.html.tostring(wsel(wtree)[0])
                #firstParagraph = re.sub("<.*?>", " ", firstParagraph).encode('utf-8')
                #print firstParagraph
                
                bot.sendMessage(chat_id=chat_id,text="Kết quả đầu tiên: " + gotoUrl)

            LAST_UPDATE_ID = update.update_id

if __name__ == '__main__':
    main()
