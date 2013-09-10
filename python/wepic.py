import bottle as btl

import epic


app = btl.Bottle()
application = app

redisconn = epic.init_redis()

@app.route('/', method='GET')
def index():
	return 'Hello. My Name is Bottle and I am EPIC!!! because I run on Python'

@app.route('/to_redis', method='POST')
def create_redis():
	epic.process_redis(btl.request.body.read(), redisconn)
