require 'rubygems'
require 'restclient'

url = ENV['ERRORBUCKET_URL']

begin
  response = RestClient.post url, 'An exception occurred...', :content_type => 'text/plain', :accept => :json
  puts response
rescue => e
  abort "Failed to POST: #{e.message}"
end
