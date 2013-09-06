import bottle as btl

import epic


app = btl.Bottle()


@app.route('/', method='GET')
def index():
	return 'Hello. My Name is Bottle and I am EPIC!!! because I run on Python'


@app.route('/to_redis', method='POST')
def create_redis():
	redisconn = epic.init_redis()

	epic.process_redis(btl.request.body.read(), redisconn)


@app.route('/to_pg', method='POST')
def create_pg():
	pgconn = epic.init_pg()
	pgcur = pgconn.cursor()
	epic.process_pg(btl.request.body.read(), pgcur)
	pgcur.close()
	pgconn.commit()
	pgconn.close()


if __name__ == "__main__":
	app.run(host='localhost', port=8080, debug=False, reloader=False)
else:
	application = app
