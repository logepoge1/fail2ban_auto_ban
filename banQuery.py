import MySQLdb
import sys
import os
from email.MIMEText import MIMEText
from subprocess import Popen, PIPE, call

host = "localhost"
port = 3306
user = "banned_ips"
password = ""
database = "banned_ips"

from_email = "example@example.com"
to_email = "example@example.com"

def connect():
	db = MySQLdb.connect(host=host, port=port, user=user, passwd=password, db=database)
	cur = db.cursor()
	return (cur, db)
def select(query):
	try:
		cur, db = connect()
		result = cur.execute(query)
		db.commit()
		result = cur.fetchall()
		db.close()
		return result
	except Exception,e:
		pass

def ban(query, ip):
        try:
                cur, db = connect()
                result = cur.execute(query, (ip))
                db.commit()
                db.close()
        except Exception,e:
                pass

query = """SELECT ip FROM ip_list WHERE hits >= 6 AND status = 'active'"""
result = select(query)
for ip in result:
	query = """UPDATE ip_list SET status = 'banned' WHERE ip = %s"""	
	call("/sbin/iptables -I INPUT 1 -p tcp --dport ssh -s %s -j DROP" % (ip[0]), shell=True)
	ban(query, ip[0])
if str(result) != "()":
	msg = MIMEText("Here are the IP Addresses banned in the last 24 hours: %s" % str(result))
	msg["From"] = from_email
	msg["To"] = to_email
	msg["Subject"] = "Daily Banned IP Address Report"
	p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
	p.communicate(msg.as_string())
else:
	msg = MIMEText("There are no banned IP Addresses to report today :)")
	msg["From"] = from_email
	msg["To"] = to_email
	msg["Subject"] = "Daily Banned IP Address Report."
	p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
	p.communicate(msg.as_string())
