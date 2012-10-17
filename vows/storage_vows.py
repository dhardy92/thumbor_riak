#se!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/globocom/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com timehome@corp.globo.com

from pyvows import Vows, expect

from fixtures.storage_fixture import IMAGE_URL, IMAGE_BYTES, get_server

from thumbor_riak.storage import Storage
from thumbor.context import Context
from thumbor.config import Config

from tornado.httputil import HTTPHeaders
import tornado.httpclient
import urllib

class RiakDBContext(Vows.Context):
  def setup(self):
    self.baseurl = "http://10.147.0.20:8097/riak"
    self.client = tornado.httpclient.HTTPClient()

@Vows.batch
class RiakStorageVows(RiakDBContext):
  class CanStoreImage(Vows.Context):
    def topic(self):
      config = Config(RIAK_STORAGE_BASEURL=self.parent.baseurl)
      storage = Storage(Context(config=config, server=get_server('ACME-SEC')))
      return (storage.put(IMAGE_URL % '1', IMAGE_BYTES) , self.parent.client.fetch(self.parent.baseurl + "/images/" + urllib.quote_plus(IMAGE_URL % '1')))

    def should_be_in_catalog(self, topic):
      expect(topic[0]).to_equal(urllib.quote_plus(IMAGE_URL % '1'))
      expect(topic[1].body).not_to_be_null()
      expect(topic[1]).not_to_be_an_error()

  class CanGetImage(Vows.Context):
        def topic(self):
            config = Config(RIAK_STORAGE_BASEURL=self.parent.baseurl)
            storage = Storage(Context(config=config, server=get_server('ACME-SEC')))

            storage.put(IMAGE_URL % '2', IMAGE_BYTES)
            return storage.get(IMAGE_URL % '2')

        def should_not_be_null(self, topic):
            expect(topic).not_to_be_null()
            expect(topic).not_to_be_an_error()

        def should_have_proper_bytes(self, topic):
            expect(topic).to_equal(IMAGE_BYTES)

  class CanGetImageExistance(Vows.Context):
        def topic(self):
            config = Config(RIAK_STORAGE_BASEURL=self.parent.baseurl)
            storage = Storage(Context(config=config, server=get_server('ACME-SEC')))

            storage.put(IMAGE_URL % '8', IMAGE_BYTES)
            return storage.exists(IMAGE_URL % '8')

        def should_exists(self, topic):
            expect(topic).to_equal(True)

  class CanGetImageInexistance(Vows.Context):
        def topic(self):
            config = Config(RIAK_STORAGE_BASEURL=self.parent.baseurl)
            storage = Storage(Context(config=config, server=get_server('ACME-SEC')))

            return storage.exists(IMAGE_URL % '9999')

        def should_not_exists(self, topic):
            expect(topic).to_equal(False)

  class CanRemoveImage(Vows.Context):
        def topic(self):
            config = Config(RIAK_STORAGE_BASEURL=self.parent.baseurl)
            storage = Storage(Context(config=config, server=get_server('ACME-SEC')))

            storage.put(IMAGE_URL % '9', IMAGE_BYTES)
            created = storage.exists(IMAGE_URL % '9')
            storage.remove(IMAGE_URL % '9')
            return storage.exists(IMAGE_URL % '9') != created

        def should_be_put_and_removed(self, topic):
            expect(topic).to_equal(True)

  class CanReturnPath(Vows.Context):
        def topic(self):
            config = Config(RIAK_STORAGE_BASEURL=self.parent.baseurl)
            storage = Storage(Context(config=config, server=get_server('ACME-SEC')))

            return storage.resolve_original_photo_path("toto")

        def should_return_the_same(self, topic):
            expect(topic).to_equal("toto")

  
