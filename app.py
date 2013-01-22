#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding:utf-8
# http://en.wikipedia.org/wiki/Representational_state_transfer

import os
import sys

import tornado.ioloop
import tornado.httpserver

from tornado.web import RequestHandler
from tornado.web import HTTPError

import json, re, base64

def isempty(string):
  if string == '' or string == None:
    return True
  return False

class Main(RequestHandler):
  def get(self):
    self.render('canvas.html')

  def post(self, rid = None):

    image = self.get_argument('image', None)
    if isempty(image):
      print 'post: warning: empty image'
      raise HTTPError(500)

    open('client.png','wb').write(base64.b64decode(image))

    os.system('tesseract client.png o')
    self.write({'data': file('o.txt').read()})

routes = [
  (r'/', Main),
]

settings = {
  'debug': True,
  'static_path': './pub/media',
  'static_url_prefix': '/media/',
  'template_path': './tpl'
}

if __name__=='__main__':
  app = tornado.web.Application(routes, **settings)
  http_server = tornado.httpserver.HTTPServer(app)
  http_server.listen(8000)
  print 'http://localhost:' + str(8000)
  tornado.ioloop.IOLoop.instance().start()
