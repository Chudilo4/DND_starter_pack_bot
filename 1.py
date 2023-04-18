# import re
# import sqlite3
#
#
# con = sqlite3.connect("dnd.db")
# cur = con.cursor()
# s = ''
# f = open('123.txt', 'r')
# txt = f.read()
# txt2 = txt.split('\n')
# for i in txt2:
#     r = re.findall(r'\d{1,} зм|\d{1,} мм|\d{1,} см', i)
#     if r:
#         s = i.split(r[0])
#         s.insert(1, r[0])
#         cur.execute("INSERT INTO room_tavern (title, money) VALUES (?, ?)", (s[0], s[1]))
#         con.commit()

import re
import sqlite3


con = sqlite3.connect("dnd.db")
cur = con.cursor()
s = ''
f = open('123.txt', 'r')
txt = f.read()
txt2 = txt.split('\n\n')
for i in txt2:
    r = i.splitlines()
    cur.execute("INSERT INTO magic (title, type_magic, casting_time, distance, components, duration, description) VALUES (?, ?, ?, ?, ?, ?, ?) ", (r[0], r[1], r[2], r[3], r[4], r[5], '\n'.join(r[6:])))
    con.commit()
