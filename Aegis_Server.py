#!/usr/bin/env python  
  
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer  
import os  
import cgi
import pandas
import random
  
#Create custom HTTPRequestHandler class  
class AegisHTTPRequestHandler(BaseHTTPRequestHandler):  

  def fetchHashTagAccToPersona(self,persona):

    print 'Fetching Random HashTag for: ' + persona

    rootdir = '/Users/ishaniGupta/Library/Mobile Documents/com~apple~CloudDocs/UCSB_4/Crypto/Project/Aegis/Tree_Data/' #file location  
    in_mem_dict = pandas.read_csv((rootdir + persona), index_col=0, squeeze=True, header= None).to_dict()
   
    alpha = 0.7
    #fetching random hashtags from in_mem_dict with values greater than alpha
    while 1 > 0:
    	hashtag, percent = random.choice(list(in_mem_dict.items()))
    	if percent < alpha :
    		continue
    	else:
    		break

    return hashtag,percent

  #handle GET command  
  def do_GET(self):  
    rootdir = '/Users/ishaniGupta/Library/Mobile Documents/com~apple~CloudDocs/UCSB_4/Crypto/Project/Aegis' #file location  
    print('GET Request Recieved...')
    try:  
      if self.path.endswith('.html'):  
        f = open(rootdir + self.path) #open requested file  
  
        #send code 200 response  
        self.send_response(200)  
  
        #send header first  
        self.send_header('Content-type','text-html')  
        self.end_headers()  
  
        #send file content to client  
        self.wfile.write(f.read())  
        f.close()  
        return  

    except IOError:  
      self.send_error(404, 'file not found')  
  

  #handle POST command  
  def do_POST(self):  
    global gender
    global ethnicity
    global location
    print('POST Request Recieved...')
    try:  
      # Parse the form data posted
      form = cgi.FieldStorage(
          fp=self.rfile, 
          headers=self.headers,
          environ={'REQUEST_METHOD':'POST',
                   'CONTENT_TYPE':self.headers['Content-Type'],
                   })

      # Begin the response
      self.send_response(200)
      self.end_headers()
      self.wfile.write('Client: %s\n' % str(self.client_address))
      self.wfile.write('User-agent: %s\n' % str(self.headers['user-agent']))
      self.wfile.write('Path: %s\n' % self.path)
      self.wfile.write('Hastag :')
      
      # Echo back information about what was posted in the form
      for attr in form.keys():
        attr_value = form[attr].value
        if(attr == 'gen'):
          gender = attr_value
        elif (attr == 'eth'):
          ethnicity = attr_value
        else:
          location = attr_value

      persona=gender+"#"+ethnicity+"#"+location+".csv"
      #print(persona)
      hashtag, percent = self.fetchHashTagAccToPersona(persona)
      self.wfile.write(hashtag)
      self.wfile.write('\nPercent : %s\n' % percent)
      return

    except:  
      self.send_error(404,'Not Correct Parameters')  

def run():  
  print('http server is starting...')  
  
  #ip and port of servr  
  #by default http server port is 80  
  server_address = ('127.0.0.1', 80)  
  httpd = HTTPServer(server_address, AegisHTTPRequestHandler)  
  print('http server is running...')  
  httpd.serve_forever()  

if __name__ == '__main__':  
  run()