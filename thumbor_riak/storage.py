#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/dhardy92/thumbor_riak/

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2012 dhard92@github.com

from json import loads, dumps
from datetime import datetime, timedelta
from thumbor.storages import BaseStorage

from tornado.httputil import HTTPHeaders
import tornado.httpclient

import urllib

class Storage(BaseStorage):

    #HTTPRequest with general settings
    def _request(self, u, m="GET", h = None, b = None):
      rq = tornado.httpclient.HTTPRequest(
                                      url=u,
                                      method=m,
                                      headers = h,
                                      body = b,
                                      connect_timeout = self.connect_timeout,
                                      request_timeout = self.request_timeout,
                                      follow_redirects = self.follow_redirects,
                                      max_redirects = self.max_redirects 
                                    )
      return rq

    def __init__(self,context):
        self.context=context
        self.cryptobk = "cryptos"
        self.detectorbk = "detectors"
        self.imagebk = "images"
        self.baseurl = self.context.config.RIAK_STORAGE_BASEURL
        self.client = tornado.httpclient.HTTPClient()

        #default reuests values
        self.connect_timeout = 0.5
        self.request_timeout = 1
        self.follow_redirects = True
        self.max_redirects = 3

    def put(self, path, content):
	path = urllib.quote_plus(path)

        #magic number detection for Content-type
        if ( content[:4] == 'GIF8'):
            ct = {"Content-Type": "image/gif"}
        elif ( content[:8] == '\x89PNG\r\n\x1a\n'):
            ct = {"Content-Type": "image/png"}
        else:
            ct = {"Content-Type": "image/jpeg"}

        url = self.baseurl + "/" + self.imagebk + "/" + path
	rq = self._request(url, m='PUT', h=ct, b=content)
        try:
          resp = self.client.fetch(rq)
          return path
        except tornado.httpclient.HTTPError, e:
          return None

    def put_crypto(self, path):
      if not self.context.config.STORES_CRYPTO_KEY_FOR_EACH_IMAGE:
        return

      if not self.context.config.SECURITY_KEY:
        raise RuntimeError("STORES_CRYPTO_KEY_FOR_EACH_IMAGE can't be True if no SECURITY_KEY specified")

      path = urllib.quote_plus(path)
      url = self.baseurl + "/" + self.cryptobk + "/" + path
      rq = self._request(url, m='PUT', h={"Content-Type": "plain/text"}, b=self.context.config.SECURITY_KEY)
      resp = self.client.fetch(rq)
 
    def put_detector_data(self, path, data):
      path = urllib.quote_plus(path)
      url = self.baseurl + "/" + self.detectorbk + "/" + path
      rq = self._request(url, m='PUT', h={"Content-Type": "application/json"}, b=dumps(data))
      resp = self.client.fetch(rq)

    def get_crypto(self, path):
      if not self.context.config.STORES_CRYPTO_KEY_FOR_EACH_IMAGE:
        return None
      path = urllib.quote_plus(path)
      url = self.baseurl + "/" + self.cryptobk + "/" + path
      rq = self._request(url)
      try:
        resp = self.client.fetch(rq)
        return resp.body
      except tornado.httpclient.HTTPError, e:
        return None


    def get_detector_data(self, path):
      path = urllib.quote_plus(path)
      url = self.baseurl + "/" + self.detectorbk + "/" + path
      rq = self._request(url)
      try:
        resp = self.client.fetch(rq)
        return loads(resp.body)
      except tornado.httpclient.HTTPError, e:
        return None

    def get(self, path):
      path = urllib.quote_plus(path)
      url = self.baseurl + "/" + self.imagebk + "/" + path
      rq = self._request(url)
      try:
        resp = self.client.fetch(rq)
        return resp.body
      except tornado.httpclient.HTTPError, e:
        return None

    def exists(self, path):
      path = urllib.quote_plus(path)
      url = self.baseurl + "/" + self.imagebk + "/" + path
      rq = self._request(url)
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

      for u in urls:
        rq = self._request(u, m='DELETE')
        try:
          resp = self.client.fetch(rq)
        except tornado.httpclient.HTTPError, e:
          pass

    def resolve_original_photo_path(self,filename):
      return urllib.quote_plus(filename)
