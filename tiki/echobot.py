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
import inspect

import logging
#import sqlite3
import MySQLdb
import telegram
import time
import datetime
from tiki.equal import Equal
from tiki.inmessage import InMessage
from tiki.startswith import Startswith

LAST_UPDATE_ID = None
dict = {}


def main():
    global LAST_UPDATE_ID
    global startedPoint
    startedPoint = datetime.datetime.now().isoformat(' ')
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Telegram Bot Authorization Token
    bot = telegram.Bot('82438901:AAFgzYUb4pQ_1qabUqY7fLJpBd4Ne7vJfLk')


    global dict
    for i in dir(telegram.Emoji):
        if (i.startswith('_') == False):
            dict[i]= getattr(telegram.Emoji, i)

    #print dict['TWISTED_RIGHTWARDS_ARROWS']        
    # This will be our global variable to keep the latest update_id when requesting
    # for updates. It starts with the latest update_id if available.
    try:
        LAST_UPDATE_ID = bot.getUpdates()[-1].update_id
    except IndexError:
        LAST_UPDATE_ID = None

    while True:
        echo(bot)
        alert(bot)
        time.sleep(1)


def echo(bot):
    global LAST_UPDATE_ID
    # Request updates from last updated_id
    for update in bot.getUpdates(offset=LAST_UPDATE_ID):
        if LAST_UPDATE_ID < update.update_id:
            """
            Set LAST_UPDATE_ID for next request
            """
            LAST_UPDATE_ID = update.update_id
            # chat_id is required to reply any message
            first_name = update.message.from_user.first_name.encode('utf-8')
            last_name = update.message.from_user.last_name.encode('utf-8')
            chat_id = update.message.chat_id
            message = update.message.text.encode('utf-8')
            user_id = update.message.from_user.id

            #print(message)

            # Define function to response message to telegram
            def response(message):
                if (message):
                    bot.sendMessage(chat_id=chat_id, text=message)
                else:
                    pass


            libEqual = Equal()

            # Alternative connection to Heroku mysql db
            db=MySQLdb.connect(host="us-cdbr-iron-east-02.cleardb.net",user="b8f6b4fd2b4d9a", passwd="c8f62d56",db="heroku_e85d0d17ea44950",charset='utf8',use_unicode=True)

            # Process with list command in db
            c = db.cursor()
            c.execute('SELECT command FROM messages')
            commands = c.fetchall()

            for row in commands:
                if row[0].encode('utf-8') in message:
                    print('in')
                    print(row[0])
                    try:
                        global dict
                        dict['firstname'] = first_name
                        dict['lastname'] = last_name
                        dict['user_id'] = user_id
                        result = libEqual.command(row[0], dict)
                        print "result"
                        print result
                        response(result)

                        return
                    except Exception as e:
                        print(e)
                        pass

            # Process with equal message
            equalMethods = dir(libEqual)
            if message in equalMethods and message != 'command':
                try:
                    result = getattr(libEqual, message)()
                    response(result)

                    return
                except Exception as e:
                    pass

            # Process with startswith '/' => command with params
            if message.startswith('/'):
                libStartswith = Startswith(message)
                # Get command string
                command = message.split(' ')[0][1:]
                # Call function from lib depends on command
                try:
                    result = getattr(libStartswith, command)()
                    response(result)

                    return
                except Exception as e:
                    print(e)
                    pass

            # Process with in message command
            libInMessage = InMessage()
            inMessageMethods = dir(libInMessage)
            for method in inMessageMethods:
                if method in message:
                    try:
                        result = getattr(libInMessage, method)()
                        response(result)

                        return
                    except Exception as e:
                        pass


def alert(bot):
    global LAST_UPDATE_ID

if __name__ == '__main__':
    main()
