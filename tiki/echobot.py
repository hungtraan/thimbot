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
import telegram
import time
import datetime
from tiki.equal import Equal
from tiki.inmessage import InMessage
from tiki.startswith import Startswith

LAST_UPDATE_ID = None


def main():
    global LAST_UPDATE_ID
    global startedPoint
    startedPoint = datetime.datetime.now().isoformat(' ')
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Telegram Bot Authorization Token
    bot = telegram.Bot('127546764:AAH2odfpjrrjTvcsKWbia2EIWdmvfWFIVZ0')

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
            # chat_id is required to reply any message
            first_name = update.message.from_user.first_name.encode('utf-8')
            last_name = update.message.from_user.last_name.encode('utf-8')
            chat_id = update.message.chat_id
            message = update.message.text.encode('utf-8')
            user_id = update.message.from_user.id

            # Define function to response message to telegram
            def response(message):
                bot.sendMessage(chat_id=chat_id, text=message)
                LAST_UPDATE_ID = update.update_id

            # Process with equall message
            libEqual = Equal()
            equalMethods = dir(libEqual)
            if message in equalMethods:
                result = getattr(libEqual, message)()
                response(result)

            # Process with startswith command
            if message.startswith('a'):
                libStartswith = Startswith()
                # Get command string
                command = message.split(' ')[0][1:]
                # Call function from lib depends on command
                try:
                    result = getattr(libStartswith, command)()
                    response(result)
                except Exception as e:
                    pass

            # Process with in message command
            libInMessage = InMessage()
            inMessageMethods = dir(libInMessage)
            for method in inMessageMethods:
                if method in message:
                    try:
                        result = getattr(libInMessage, method)()
                        response(result)
                    except Exception as e:
                        pass
            return

def alert(bot):
    global LAST_UPDATE_ID

if __name__ == '__main__':
    main()
