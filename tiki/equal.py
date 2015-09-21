#!/usr/bin/env python
import sqlite3


class Equal:
    """etc."""
    def abc(self):
        print('def')

    def command(self, command):
        conn = sqlite3.connect('tiki.db')
        c = conn.cursor()
        c.execute('SELECT response FROM messages WHERE command=?', (command,))
        message = c.fetchone()

        return message
