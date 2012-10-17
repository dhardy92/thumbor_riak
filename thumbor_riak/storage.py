#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/dhardy92/thumbor_riak/

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license

from json import loads, dumps
from datetime import datetime, timedelta
from thumbor.storages import BaseStorage

from tornado.httputil import HTTPHeaders
import tornado.httpclient

import urllib

class Storage(BaseStorage):
    def __init__(self,context):
        self.context=context
        self.cryptobk = "cryptos"
        self.detectorbk = "detectors"
        self.imagebk = "images"
        self.baseurl = self.context.config.RIAK_STORAGE_BASEURL
        self.client = tornado.httpclient.HTTPClient()

        #default reuests values
        self.connect_timeout = 20
        self.request_timeout = 20
        self.follow_redirects = True
        self.max_redirects = 3

    def put(self, path, content):
	path = urllib.quote_plus(path)

        url = self.baseurl + "/" + self.imagebk + "/" + path
	rq = tornado.httpclient.HTTPRequest(
                                      url = url,
                                      method='PUT',
                                      headers = {"content-type": "image/jpeg"},
                                      body = content,
                                      connect_timeout = self.connect_timeout,
                                      request_timeout = self.request_timeout,
                                      follow_redirects = self.follow_redirects,
                                      max_redirects = self.max_redirects 
                                    )
        try:
          resp = self.client.fetch(rq)
          return path
        except tornado.httpclient.HTTPError, e:
          return None

    def put_crypto(self, path):
      path = urllib.quote_plus(path)
      url = self.baseurl + "/" + self.cryptobk + "/" + path
      rq = tornado.httpclient.HTTPRequest(
                                      url = url,
                                      method='PUT',
                                      headers = {"content-type": "plain/text"},
                                      body = content,
                                      connect_timeout = self.connect_timeout,
                                      request_timeout = self.request_timeout,
                                      follow_redirects = self.follow_redirects,
                                      max_redirects = self.max_redirects
                                    )
      resp = self.client.fetch(rq)
 
    def put_detector_data(self, path, data):
      path = urllib.quote_plus(path)
      url = self.baseurl + "/" + self.detectorbk + "/" + path
      rq = tornado.httpclient.HTTPRequest(
                                      url = url,
                                      method='PUT',
                                      headers = {"content-type": "plain/text"},
                                      body = content,
                                      connect_timeout = self.connect_timeout,
                                      request_timeout = self.request_timeout,
                                      follow_redirects = self.follow_redirects,
                                      max_redirects = self.max_redirects
                                    )
      resp = self.client.fetch(rq)

    def get_crypto(self, path):
      path = urllib.quote_plus(path)
      url = self.baseurl + "/" + self.cryptobk + "/" + path
      rq = tornado.httpclient.HTTPRequest(
                                      url = url,
                                      connect_timeout = self.connect_timeout,
                                      request_timeout = self.request_timeout,
                                      follow_redirects = self.follow_redirects,
                                      max_redirects = self.max_redirects
                                    )
      resp = self.client.fetch(rq)
      return resp.body

    def get_detector_data(self, path):
      path = urllib.quote_plus(path)
      url = self.baseurl + "/" + self.detectorbk + "/" + path
      rq = tornado.httpclient.HTTPRequest(
                                      url = url,
                                      connect_timeout = self.connect_timeout,
                                      request_timeout = self.request_timeout,
                                      follow_redirects = self.follow_redirects,
                                      max_redirects = self.max_redirects
                                    )
      resp = self.client.fetch(rq)
      return resp.body

    def get(self, path):
      path = urllib.quote_plus(path)
      url = self.baseurl + "/" + self.imagebk + "/" + path
      rq = tornado.httpclient.HTTPRequest(
                                      url = url,
                                      connect_timeout = self.connect_timeout,
                                      request_timeout = self.request_timeout,
                                      follow_redirects = self.follow_redirects,
                                      max_redirects = self.max_redirects
                                    )
      resp = self.client.fetch(rq)
      return resp.body

    def exists(self, path):
      path = urllib.quote_plus(path)
      url = self.baseurl + "/" + self.imagebk + "/" + path
      rq = tornado.httpclient.HTTPRequest(
                                      url = url,
                                      method = 'GET',
                                      connect_timeout = self.connect_timeout,
                                      request_timeout = self.request_timeout,
                                      follow_redirects = self.follow_redirects,
                                      max_redirects = self.max_redirects
                                    )
      try:
        resp = self.client.fetch(rq)
        return (resp.code in [200,302,304])
      except tornado.httpclient.HTTPError, e:
        return False

    def remove(self,path):
      path = urllib.quote_plus(path)
      urls = [ self.baseurl + "/" + self.imagebk + "/" + path , 
               self.baseurl + "/" + self.cryptobk + "/" + path,
               self.baseurl + "/" + self.detectorbk + "/" + path ]

      for  u in urls:
        rq = tornado.httpclient.HTTPRequest(
                                      url = u,
                                      method = 'DELETE',
                                      connect_timeout = self.connect_timeout,
                                      request_timeout = self.request_timeout,
                                      follow_redirects = self.follow_redirects,
                                      max_redirects = self.max_redirects
                                    )
      
        try:
          resp = self.client.fetch(rq)
        except tornado.httpclient.HTTPError, e:
          pass

    def resolve_original_photo_path(self,filename):
      return urllib.quote_plus(filename)
