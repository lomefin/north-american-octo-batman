require 'sinatra'
load 'processor.rb'



get '/' do
  puts params

end

get '/to_redis' do
  processor = Processor()
  processor.process_redis(params[:data]) 
end

get '/to_pg' do
  processor = Processor()
  processor.process_postgres(params[:data])
end

