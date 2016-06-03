import MySQLdb
import sys

host = "localhost"
port = 3306
user = "banned_ips"
password = ""
database = "banned_ips"

def connect():
	db = MySQLdb.connect(host=host, port=port, user=user, passwd=password, db=database)
	cur = db.cursor()
	return (cur, db)
def insert(query, ip):
	try:
		cur, db = connect()
		cur.execute(query, (ip))
		db.commit()
		db.close()
	except Exception,e:
		print str(e)
		pass

ip = sys.argv[1]
query = """ INSERT INTO ip_list(ip, status) VALUES(%s, 'active') ON DUPLICATE KEY UPDATE hits=hits+1"""
insert(query, ip)
