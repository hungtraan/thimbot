#!/usr/bin/env python
#import sqlite3
from jinja2 import Template
import MySQLdb

class Equal:
    """etc."""
    def abc(self):
        print('def')

    def command(self, command, params):
        db=MySQLdb.connect(host="us-cdbr-iron-east-02.cleardb.net",user="b8f6b4fd2b4d9a", passwd="c8f62d56",db="heroku_e85d0d17ea44950",charset='utf8',use_unicode=True)

        # Process with list command in db
        c = db.cursor()
        c.execute("SELECT response FROM messages WHERE command=%s", [command])
        message = c.fetchone()
        print(message)
        # return row
        template = Template(message[0])
        result = template.render(firstname=params[0], lastname=params[1], userid=params[2]).encode('utf-8', 'ignore')
        print("result render:", result)

        return result
