#!/usr/bin/env python
import sqlite3
from jinja2 import Template


class Equal:
    """etc."""
    def abc(self):
        print('def')

    def command(self, command, params):
        conn = sqlite3.connect('tiki.db')
        c = conn.cursor()
        c.execute('SELECT response FROM messages WHERE command=?', (command,))
        message = c.fetchone()
        # return row
        template = Template(message[0])
        result = template.render(firstname=params[0], lastname=params[1], userid=params[2])

        return result
