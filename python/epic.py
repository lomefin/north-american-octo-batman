import time
import datetime
import random
import json
import os
import csv

import psycopg2
import redis
import pytz


PG_SERVER = os.environ['PG_SERVER']
PG_USER = os.environ['PG_USER']
PG_PASS = os.environ['PG_PASS']
PG_DB = os.environ['PG_DB']
PG_INSERT_QUERY = """INSERT INTO epic.incoming
(name, position, time_generated)
VALUES (%s, %s, CAST(%s as timestamp with time zone))"""
PG_CREATE_TABLE_QUERY = """CREATE TABLE epic.incoming (
name varchar(255) not null,
position varchar(255) not null,
time_generated timestamp with time zone not null,

primary key (name, position, time_generated)
)"""


REDIS_SERVER = os.environ['REDIS_SERVER']
REDIS_PORT = 6379 if 'REDIS_PORT' not in os.environ else os.environ['REDIS_PORT']
REDIS_DB = os.environ['REDIS_DB']
REDISQUEUE = 'incoming'


def init_pg():
	return psycopg2.connect(
		host=PG_SERVER,
		user=PG_USER, password=PG_PASS,
		database=PG_DB
	)


def init_redis():
	redispool = redis.ConnectionPool(
		host=REDIS_SERVER, port=REDIS_PORT, db=REDIS_DB
	)
	return redis.Redis(connection_pool=redispool)


def process_redis(data, p):
	p.lpush(REDISQUEUE, data)


def process_pg(data, p):
	data = json.loads(data)
	p.execute(PG_INSERT_QUERY, (data['name'], data['position'], data['time_generated']))


def attack(n):
	#pgconn = init_pg()
	#redisconn = init_redis()
	#pgcur = pgconn.cursor()

	time_acc_redis = 0
	time_acc_pg = 0

	for i in xrange(n):
		pgconn = init_pg()
		pgcur = pgconn.cursor()
		redisconn = init_redis()
		data = json.dumps(
			{
				'name': 'pablogps',
				'position': '{lon} {lat}'.format(lat=random.uniform(-90, 90), lon=random.uniform(-180, 180)),
				'time_generated': datetime.datetime.now(pytz.UTC).isoformat()
			}
		)
		t_before = time.time()
		process_redis(data, redisconn)
		t_after = time.time()
		t_redis = t_after - t_before
		time_acc_redis += t_redis

		t_before = time.time()
		process_pg(data, pgcur)
		pgconn.commit()
		t_after = time.time()
		t_pg = t_after - t_before
		time_acc_pg += t_pg

		pgconn.close()
	#pgconn.commit()
	#pgconn.close()

	print 'n={n}, redis={t_redis}, pg={t_pg}, diff={d} | {f}, champion={ch}'.format(
		n=n,
		t_redis=time_acc_redis, t_pg=time_acc_pg, d=time_acc_redis - time_acc_pg,
		f=time_acc_redis / time_acc_pg,
		ch='Redis' if time_acc_redis - time_acc_pg < 0 else 'PG'
	)
	return n, time_acc_redis, time_acc_pg, time_acc_redis - time_acc_pg, time_acc_redis/time_acc_pg

def stats_csv(filename='./epic.csv', start=500, inc=500, end=50000):
	print 'Beginning stats gathering... Filename is {fn}'.format(fn=filename)
	with open(filename, 'wb') as f:
		csvw = csv.writer(f)
		csvw.writerow(['Rows', 'pg_time', 'redis_time'])
		nn = xrange(start, end + inc, inc)
		for n in nn:
			r = attack(n)
			csvw.writerow([r[0], r[2], r[1]])


if __name__ == '__main__':
	stats_csv()
