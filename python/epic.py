import time
import datetime
import random
import json

import psycopg2
import redis
import pytz


pgconn = None
pgcur = None
PG_INSERT_QUERY = """INSERT INTO epic.incoming
(name, position, time_generated)
VALUES (%s, %s, CAST(%s as timestamp with time zone))"""
PG_CREATE_TABLE_QUERY = """CREATE TABLE epic.incoming (
name varchar(255) not null,
position varchar(255) not null,
time_generated timestamp with time zone not null,

primary key (name, position, time_generated)
)"""

redisconn = None
REDISQUEUE = 'incoming'

EXAMPLE_DATA = json.dumps(
	{'name': 'pablogps', 'position': '666, -666', 'time_generated': '2013-08-30T22:33:44-0400'}
)


def initialize():
	pgconn = psycopg2.connect(
		host='localhost',
		user='epic', password='test',
		database='testdb'
	)
	redispool = redis.ConnectionPool(
		host='localhost', db=13
	)
	redisconn = redis.Redis(connection_pool=redispool)
	return pgconn, redisconn


def process_redis(data):
	redisconn.lpush(REDISQUEUE, data)


def process_pg(data):
	data = json.loads(data)
	pgcur.execute(PG_INSERT_QUERY, (data['name'], data['position'], data['time_generated']))


def example():
	pgconn, redisconn = initialize()
	pgcur = pgconn.cursor()

	t_before = time.time()
	process_redis(EXAMPLE_DATA)
	t_after = time.time()
	t_redis = t_after - t_before

	t_before = time.time()
	process_pg(EXAMPLE_DATA)
	t_after = time.time()
	t_pg = t_after - t_before

	print t_redis, t_pg


def attack(n):
	global pgconn, redisconn, pgcur
	#pgconn, redisconn = initialize()
	#pgcur = pgconn.cursor()

	time_acc_redis = 0
	time_acc_pg = 0

	for i in xrange(n):
		pgconn, redisconn = initialize()
		pgcur = pgconn.cursor()
		data = json.dumps(
			{
				'name': 'pablogps',
				'position': '{lon} {lat}'.format(lat=random.uniform(-90, 90), lon=random.uniform(-180, 180)),
				'time_generated': datetime.datetime.now(pytz.UTC).isoformat()
			}
		)
		t_before = time.time()
		process_redis(data)
		t_after = time.time()
		t_redis = t_after - t_before
		time_acc_redis += t_redis

		t_before = time.time()
		process_pg(data)
		pgconn.commit()
		t_after = time.time()
		t_pg = t_after - t_before
		time_acc_pg += t_pg

		pgconn.close()
	#pgconn.commit()
	#pgconn.close()

	print 'n={n}, redis={t_redis}, pg={t_pg}, diff={d}/{f}, champion={ch}'.format(
		n=n,
		t_redis=time_acc_redis, t_pg=time_acc_pg, d=time_acc_redis - time_acc_pg,
		f=time_acc_redis / time_acc_pg,
		ch='Redis' if time_acc_redis - time_acc_pg < 0 else 'PG'
	)
