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
import urllib2
import urllib
import re
import operator
import datetime
import sys
import feedparser
import os

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

    global newRelicFeed
    newRelicFeed = feedparser.parse('https://rpm.newrelic.com/accounts/857072/applications/9351884/incidents.rss?data_access_key=b5e5145b73b9a5c571843470b1c87ddad1aa11ae0b724a5')
    global currAlert
    currAlert = newRelicFeed.entries[0]['link']

    while True:
        echo(bot)
        alert(bot)
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
                message = message.replace('@ThimBot','')

            # Almighty New Relic Alert ====================================
            
            if message == '/getAlert':
                newRelicFeed = feedparser.parse('https://rpm.newrelic.com/accounts/857072/applications/9351884/incidents.rss?data_access_key=b5e5145b73b9a5c571843470b1c87ddad1aa11ae0b724a5')
                
                fullAlert = newRelicFeed.entries[0]
                alertText = '================= NewRelic Alert =================\n\n' + fullAlert['title'] + "\n" + fullAlert['description'] + '\n\n'
                bot.sendMessage(chat_id=chat_id,text=alertText)

            # End almighty New Relic Alert ====================================


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

            if ('ai đẹp' in message or 'Ai đẹp' in message) and ('trai' in message or 'zai' in message) and ('team tech' in message or 'team Tech' in message or 'team' in message):
                trai = ['Thông','Tùng','Phong','Đức',"Hoà Lê",'Hoà Nguyễn','Hoàng','Hạt','Duy','Tân','Đông','Trung']
                
                bot.sendMessage(chat_id=chat_id,text="Hẳn là thím... "+ trai[random.randrange(len(trai)-1)] + " " + telegram.Emoji.PILE_OF_POO)
                time.sleep(3)
                bot.sendMessage(chat_id=chat_id,text="À không, ta nghĩ lại... Đẹp nhất phải là thím "+ trai[random.randrange(len(trai)-1)] + " " + telegram.Emoji.PILE_OF_POO)
                time.sleep(3)
                bot.sendMessage(chat_id=chat_id,text="À vẫn không! ĐẸP TRAI NHẤT PHẢI LÀ THÍM "+ trai[random.randrange(len(trai)-1)] + " " + telegram.Emoji.PILE_OF_POO)

            if ('ai đẹp gái nhất' in message or 'ai xinh gái nhất' in message or 'Ai đẹp gái nhất' in message or 'Ai xinh gái nhất' in message) and ('team tech' in message or 'team Tech' in message or 'team' in message):
                gai = ['Bích',"Vi",'Giàu','Khanh']
                bot.sendMessage(chat_id=chat_id,text="Thím kia ngươi ở trên server... Người đẹp nhất trần hẳn là... "+ gai[random.randrange(len(gai)-1)] + " " + telegram.Emoji.WINKING_FACE)
                time.sleep(5)
                bot.sendMessage(chat_id=chat_id,text="Ta nói giỡn, chứ nữ team Tech ai cũng xinh đẹp rạng ngời "+ telegram.Emoji.WINKING_FACE)

            if 'đẹp' in message and 'hông' in message:
                bot.sendMessage(chat_id=chat_id,text="Nghĩ sao ai mà đẹp được bằng thím "+ telegram.Emoji.WINKING_FACE)

            if message == "/chaothim" or message =="Chào thím":
                ways = ['Annyeong haseyooooo',"Hếlôôôôôôô", "Bông giuaaa",'Sawadikaaaapppp','Konnichiwaaaaa ']
                if user_id not in helloed:
                    # Reply the message
                    bot.sendMessage(chat_id=chat_id,text= ways[random.randrange(len(ways)-1)]+ " thím "+ first_name + " " + telegram.Emoji.PILE_OF_POO)
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
                bot.sendMessage(chat_id=chat_id,text="Con cứ bình tĩnh "+first_name+" à, mọi việc sẽ ổn cả thôi "+ telegram.Emoji.RELIEVED_FACE)

            if message == "/whereisthim":
                bot.sendMessage(chat_id=chat_id,text="Ta đây, con cần gì, "+ first_name + "? " +telegram.Emoji.RELIEVED_FACE)
            
            if message == "ê thím":
                bot.sendMessage(chat_id=chat_id,text="Tên "+ first_name + "kia, sao dám gọi Thánh Thím ta như dzậy hả? " +telegram.Emoji.ANGRY_FACE)

            if message == "/whereisthim":
                bot.sendMessage(chat_id=chat_id,text="Ta đây, con cần gì, "+ first_name + "? " +telegram.Emoji.RELIEVED_FACE)

            if "thím ơi" in message or "Thím ơi" in message:
                oiReplies = ["Ta đây, con cần gì, ","Wểi... ","Ai gọi ta đó, có ta đâyyyyy ",'Annyeong haseyooooo ',"Hếlôôôôôôô ", "Bông giuaaa ",'Sawadikaaaapppp ','Konnichiwaaaaa ']
                bot.sendMessage(chat_id=chat_id,text= oiReplies[random.randrange(len(oiReplies))]+ first_name + "? " +telegram.Emoji.RELIEVED_FACE)

                #LAST_UPDATE_ID = update.update_id
            if message == '/det':
                bot.sendMessage(chat_id=chat_id,text="Đột...")
                #LAST_UPDATE_ID = update.update_id

            if ":(" in message or "buồn quá" in message:
                bot.sendMessage(chat_id=chat_id,text=first_name + " ơi, con đừng buồn..." +telegram.Emoji.RELIEVED_FACE)

            if ":)" in message and ':))' not in message:
                sass = ["Thôi đi thím "+first_name + ", bày đặt cười hiền... ", "Có vẻ giả tạo nha thím "+first_name + " :) ",":) :) :) :) "+first_name + " :) :) :) ", "Có đẹp bằng Thánh Thím ta không mà đòi cười hiền hả "+first_name + " :) ",":) cái wừng... "]
                bot.sendMessage(chat_id=chat_id,text=sass[random.randrange(0,len(sass)-1)] + telegram.Emoji.PILE_OF_POO)

            if ":-s" in message:
                bot.sendMessage(chat_id=chat_id,text="Bình tĩnh nào " + first_name + " ơi " +telegram.Emoji.VICTORY_HAND)

            if b'\xF0\x9F\x91\x8D' in message or "(y)" in message:
                bot.sendMessage(chat_id=chat_id,text="Ohh yeahhh thím cũng đồng ý với con đó " + first_name + " " +telegram.Emoji.THUMBS_UP_SIGN+telegram.Emoji.THUMBS_UP_SIGN+telegram.Emoji.THUMBS_UP_SIGN)

            if "bai" in message or "bye" in message:
                bot.sendMessage(chat_id=chat_id,text="Thím cho mi lui đó " + first_name + " " +telegram.Emoji.UNAMUSED_FACE+telegram.Emoji.SMIRKING_FACE)

            if "thím Thông" in message:
                bot.sendMessage(chat_id=chat_id,text="Ai nhắc đến người thanh niên bụng bự mong manh dễ vỡ đó đó đó đó?? Chọc thím ấy là Thánh Thím ta không tha cho đâu nhaaa " +telegram.Emoji.UNAMUSED_FACE)
            
            if "bình tĩnh" in message:
                bot.sendMessage(chat_id=chat_id,text="Đúng rồi, làm cái wừng gì mà rần rần lên dzậy hà? Mợt quá nhaaa " +telegram.Emoji.UNAMUSED_FACE)

            if telegram.Emoji.UNAMUSED_FACE in message:
                bot.sendMessage(chat_id=chat_id,text="Thôi đuê, đừng có ở đó bày đặt làm mặt ngầu như ta " +telegram.Emoji.UNAMUSED_FACE)

            if message == '/fthim':
                bot.sendMessage(chat_id=chat_id,text="Lượn đi cho nước nó trong "+ first_name + " à " +telegram.Emoji.RELIEVED_FACE)

            if message == '/thimui':
                bot.sendMessage(chat_id=chat_id,text="http://uimovement.com/ui/"+str(random.randrange(1,170)))
                #LAST_UPDATE_ID = update.update_id

            if message == '/thimsanmoi' or message == 'thím săn mồi':
                bot.sendMessage(chat_id=chat_id,text="http://www.producthunt.com/tech/"+str(random.randrange(1,31396)))
                #LAST_UPDATE_ID = update.update_id

            if '/thimdaudo' in message or 'đậu đỏ' in message:
                script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
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
                        bot.sendPhoto(chat_id=chat_id, photo=open(os.path.join(script_dir, random.choice(daudoPhotos.values())),'rb'))
                    except Exception as e: # catch *all* exceptions
                        print e
                        pass
                else:
                    whichDau = message.split()[1]
                    if whichDau == 'help':
                        for key in daudoPhotos.keys():
                            listDau += key+"\n"
                        bot.sendMessage(chat_id=chat_id,
                            text="Thím có các bạn đậu đỏ sau đâu:\n"+listDau)
                    elif whichDau in daudoPhotos:
                        try:
                            bot.sendPhoto(chat_id=chat_id, photo=open(os.path.join(script_dir,daudoPhotos[whichDau]),'rb'))
                        except Exception as e: # catch *all* exceptions
                            print e
                            pass
                    else:
                        try:
                            bot.sendPhoto(chat_id=chat_id, photo=open(os.path.join(script_dir,random.choice(daudoPhotos.values())),'rb'))
                        except Exception as e: # catch *all* exceptions
                            print e
                            pass

            if '/thimwiki' in message:
                if len(message.split()) < 2 :
                    bot.sendMessage(chat_id=chat_id,text="Cú pháp để hỏi ta là: /thimwiki từ-muốn-hỏi --lang=en/vi")
                    LAST_UPDATE_ID = update.update_id
                    return

                lang = 'vi'
                if '--lang' in message:
                    langIdx = message.find('--lang')+7
                    lang = message[langIdx:]
                    message = message[:langIdx-7]

                query = message.replace('/thimwiki ','')
                query = urllib.quote(query)
                
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
            
            if '/thimnghenhac' in message:
                if len(message.split()) < 2 :
                    bot.sendMessage(chat_id=chat_id,text="Cú pháp để hỏi ta là: /thimnghenhac từ muốn kiếm")
                    LAST_UPDATE_ID = update.update_id
                    return

                query = ' '.join(message.split()[1:])
                opener = urllib2.build_opener()
                opener.addheaders = [('User-agent', 'Chrome/41.0.2228.0')]

                url = "https://www.google.com/search?es_th=1&q="+urllib.quote(query)+"&rct=j&qscrl=1"
                # resultPage = urllib.urlopen(url).read()
                resultPage = opener.open(url).read()

                if "did not match any documents" in resultPage:
                    bot.sendMessage(chat_id=chat_id,text="Thím hổng tìm ra gì trên Google cho cái này :(")
                    LAST_UPDATE_ID = update.update_id
                    return

                # build the DOM Tree
                tree = lxml.html.fromstring(resultPage)

                # construct a CSS Selector
                sel = CSSSelector('h3.r > a')

                # Apply the selector to the DOM tree.
                results = sel(tree)
                firstResult = results[1]
                astr = lxml.html.tostring(firstResult)

                href = re.search("(q\=.*?\&)",astr)
                gotoUrl = href.group(0)[2:-1]
                unEscaper = {'%20':' ','%3C':'<','%3E':'>','%23':'#', '%25':'%','%7B':'{','%7D':'}','%7C':'|', '%5C':"\\",'%5E':'^','%7E':'~' ,'%5B':'[' ,'%5D':']', '%60':'`','%3B':';','%2F':'/','%3F':'?' ,'%3A':':' ,'%40':'@','%3D':'=', '%26':'&','%24':'$'}
                for key, value in unEscaper.iteritems():
                    if key in gotoUrl:
                        gotoUrl = gotoUrl.replace(key, value)
                
                print gotoUrl
                
                bot.sendMessage(chat_id=chat_id,text="Đây hẳn là... " + gotoUrl)
                
            LAST_UPDATE_ID = update.update_id

def alert(bot):
    global LAST_UPDATE_ID
    # chat_id is required to reply any message
    chat_id = -9146500 #All Stars
    #chat_id = -39735091 #Test bot
    # Almighty New Relic Alert ====================================
    newRelicFeed = feedparser.parse('https://rpm.newrelic.com/accounts/857072/applications/9351884/incidents.rss?data_access_key=b5e5145b73b9a5c571843470b1c87ddad1aa11ae0b724a5')
    
    latestAlert = newRelicFeed.entries[0]['link']
    global currAlert
    isUpdated = (currAlert != latestAlert)

    if isUpdated:
        # Send alert
        fullAlert = newRelicFeed.entries[0]
        alertText = '================= NewRelic Alert =================\n\n' + fullAlert['title'] + "\n" + fullAlert['description']  + '\n\n'
        bot.sendMessage(chat_id=chat_id,text=alertText)

        # Update latest alert
        currAlert = latestAlert

if __name__ == '__main__':
    main()
