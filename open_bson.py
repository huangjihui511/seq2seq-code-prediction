'''
path = "/Users/huangjihui/Downloads/dump/github/events.bson"

import bson
bson_file = open(path,'rb')

bson_data = bson.loads(bson_file.read())

bson_data[0]

pass
'''

import sqlite3

sqlite_file = '/Users/huangjihui/Downloads/rxjs-ghtorrent.db'

conn = sqlite3.connect(sqlite_file)
c = conn.cursor()
pass