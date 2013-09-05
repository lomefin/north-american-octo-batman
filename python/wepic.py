import bottle as btl

import epic


app = btl.Bottle()


@app.route('/gpsredis', method='POST')
def create_redis():
	redisconn = epic.init_redis()

	epic.process_redis(btl.request.body.read(), redisconn)


@app.route('/gpspg', method='POST')
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