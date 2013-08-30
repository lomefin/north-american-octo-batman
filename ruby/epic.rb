load "processor.rb"
require 'date'
require 'json'

MAX_DATA = 200000

def create_data(rows)
	data = []
	(0..rows).each do |x|
		data << JSON.dump({name: "element"+x.to_s, position: x.to_s+",2323", time_generated: DateTime.now})
	end
	data
end

def start
	file = File.open("results.csv", "a")
	file.print "Rows;pg_time;redis_time\n"
	file.close
	processor = Processor.new
	puts "TEST START"
	(1..100).each do |i|
		rows = i * 500
		puts "ROWS for this test " + rows.to_s
		data = create_data rows
		puts "Postgres START"
		postgres_start = DateTime.now
		data.each do |x|
			processor.process_postgres x
		end
		postgres_finish = DateTime.now
		puts "REDIS START"
		redis_start = DateTime.now
		data.each do |x|
			processor.process_redis x
		end
		redis_finish = DateTime.now

		pg_time = (postgres_finish - postgres_start).to_f
		puts "Postgres"
		puts pg_time
		puts (MAX_DATA / pg_time).to_s + " rows per sec"

		r_time = (redis_finish - redis_start).to_f
		puts "Redis"
		puts r_time
		puts (MAX_DATA / r_time).to_s + " rows per sec"	
		

		if pg_time > r_time
			puts "Redis wins over postgres" 
			
		else
			puts "Postgres wins over Redis" 
			puts "Ratio is " + (r_time/pg_time).to_s
		end
		file = File.open("results.csv", "a")
		file.print "#{rows};#{pg_time};#{r_time}\n"
		file.close

	end
end

start