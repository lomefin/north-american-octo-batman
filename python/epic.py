import time
import datetime
import random
import os

import redis
import pytz




REDISQUEUE = 'incoming'

def init_redis():
	redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
	redis = redis.from_url(redis_url)
	return redis


def process_redis(data, p):
	p.lpush(REDISQUEUE, data)
