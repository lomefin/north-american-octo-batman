require 'json'
require 'pg'
require 'redis'



class Processor
  attr_accessor :conn
  def initialize
  end
  def process_redis(json)
    @redis = Redis.new
    @redis.lpush 'incomming', json
    @redis.quit
  end

  def process_postgres(json)
    @conn = PG::Connection.open({dbname: ENV['DBNAME'],user:ENV['DBUSER'],password:ENV['DBPASS'],host:ENV['DBHOST']})
    data = JSON.parse(json)
    sql = "INSERT INTO info(
            \"name\", \"position\", \"time_generated\")
          VALUES ('#{data["name"]}', '#{data["position"]}', '#{data["time_generated"]}');"
    @conn.exec sql
    @conn.close
  end

end
