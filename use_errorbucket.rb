require 'rubygems'
require 'restclient'

url = ENV['ERRORBUCKET_URL']
secret_key = ENV['ERRORBUCKET_SECRET_KEY']
puts "POSTing to #{url}"

begin
  response = RestClient.post url, { :secret_key => secret_key, :message => 'An exception occurred...' }, :accept => :json
  puts response
rescue => e
  abort "Failed to POST: #{e.message}"
end
