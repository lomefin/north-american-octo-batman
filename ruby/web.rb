require "rubygems"
require "sinatra/base"
load 'processor.rb'

class Epic < Sinatra::Base

  get '/' do
    'Hello, nginx and unicorn!'
  end
  post '/' do
    params.inspect

  end

  post '/to_redis' do
    processor = Processor.new
    processor.process_redis(params[:data]) 
  end

  post '/to_pg' do
    processor = Processor.new
    processor.process_postgres(params[:data])
  end

end
