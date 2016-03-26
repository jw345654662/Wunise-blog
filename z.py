import sqlite3,config,base64
conn = sqlite3.connect(config.path)
cursor = conn.execute("SELECT TITLE, TIME, CLASS,ID,MAKEDOWN_TEXT from BLOG order by id desc")
x = []

for row in cursor:
	print row[0]
	print row[1]
	print row[2]
	print row[3]
	print row[4]
	x.append([base64.b64decode(row[0]),row[1],base64.b64decode(row[2]),row[3],base64.b64decode(row[4])])


for row2 in x:
	print row2[0]
	print row2[1]
	print row2[2]
	print row2[3]
	print row2[4]
