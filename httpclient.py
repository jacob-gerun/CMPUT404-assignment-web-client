#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
import os
import platform
# you may use urllib to encode data appropriately
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        #return None
        #print("In get code")
        #print(data.split(' '))
        #print(data.split(' ')[0].split(' ')[1])
        return int(data.split(' ')[1])

    def get_headers(self,data):
        #print('get_headers: ',data)
        return None

    def get_body(self, data):
        #print('get_body: ',repr(data))
        #print(data.split('\r\n\r\n')[1])
        return data.split('\r\n\r\n')[1]
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        #print('In GET')
        #print("VERSION")
        #print(sys.version)
        code = 500
        body = ""
        parsedURL = urllib.parse.urlparse(url)
        host = parsedURL.hostname
        port = parsedURL.port if parsedURL.port else 80
        self.connect(host, port)
        path = parsedURL.path if parsedURL.path else "/"
        # print('Host:', host)
        # print('Port:', port)
        # print('Path:', path)
        # print('Os Name:', os.name)
        # print("platform:", platform.system())
        if args:
            self.sendall(f"GET {path}?{urllib.parse.urlencode(args)} HTTP/1.1\r\nHost: {host}\r\nUser-Agent: {platform.system()}\r\nConnection: close\r\n\r\n")
        else:
            self.sendall(f"GET {path} HTTP/1.1\r\nHost: {host}\r\nUser-Agent: {platform.system()}\r\nConnection: close\r\n\r\n")
        recv = self.recvall(self.socket)
        # print('recv', recv)
        # print(urllib.parse.urlparse(url))
        # print('url: ',url)
        # print('args: ',args)
        # print('get code:',self.get_code(recv))
        # print('get body:',self.get_body(recv))
        self.close()
        return HTTPResponse(self.get_code(recv), self.get_body(recv))

    def POST(self, url, args=None):
        # print('POST')
        parsedURL = urllib.parse.urlparse(url)
        host = parsedURL.hostname
        port = parsedURL.port if parsedURL.port else 80
        self.connect(host, port)
        path = parsedURL.path if parsedURL.path else "/"
        if args:
            body = urllib.parse.urlencode(args)
            # print('PARSED ARGS',body)
            self.sendall(f"POST {path} HTTP/1.1\r\nHost: {host}\r\nUser-Agent: {platform.system()}\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {len(body)}\r\nConnection: close\r\n\r\n{body}\r\n\r\n")
        else:
            self.sendall(f"POST {path} HTTP/1.1\r\nHost: {host}\r\nUser-Agent: {platform.system()}\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: 0\r\nConnection: close\r\n\r\n")
        #self.close()
        recv = self.recvall(self.socket)
        self.close()
        return HTTPResponse(self.get_code(recv), self.get_body(recv))

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
