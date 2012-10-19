#se!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/globocom/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2012 dhardy92@github.com

from pyvows import Vows, expect

from fixtures.storage_fixture import IMAGE_URL, IMAGE_BYTES, get_server, GIF_BYTES, PNG_BYTES, GIF_URL, PNG_URL

from thumbor_riak.storage import Storage
from thumbor.context import Context
from thumbor.config import Config

from tornado.httputil import HTTPHeaders
import tornado.httpclient
import urllib

class RiakDBContext(Vows.Context):
  def setup(self):
    #change for riak HTTP interface
    self.baseurl = "http://localhost:8098/riak" 
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

  class CanStoreGIF(Vows.Context):
    def topic(self):
      config = Config(RIAK_STORAGE_BASEURL=self.parent.baseurl)
      storage = Storage(Context(config=config, server=get_server('ACME-SEC')))
      return (storage.put(GIF_URL % '1', GIF_BYTES) , self.parent.client.fetch(self.parent.baseurl + "/images/" + urllib.quote_plus(GIF_URL % '1')))

    def should_be_in_catalog(self, topic):
      expect(topic[0]).to_equal(urllib.quote_plus(GIF_URL % '1'))
      expect(topic[1].body).not_to_be_null()
      expect(topic[1].headers['Content-Type']).to_equal('image/gif')
      expect(topic[1]).not_to_be_an_error()

  class CanStorePNG(Vows.Context):
    def topic(self):
      config = Config(RIAK_STORAGE_BASEURL=self.parent.baseurl)
      storage = Storage(Context(config=config, server=get_server('ACME-SEC')))
      return (storage.put(PNG_URL % '1', PNG_BYTES) , self.parent.client.fetch(self.parent.baseurl + "/images/" + urllib.quote_plus(PNG_URL % '1')))

    def should_be_in_catalog(self, topic):
      expect(topic[0]).to_equal(urllib.quote_plus(PNG_URL % '1'))
      expect(topic[1].body).not_to_be_null()
      expect(topic[1].headers['Content-Type']).to_equal('image/png')
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

  class CantGetImage(Vows.Context):
    def topic(self):
      config = Config(RIAK_STORAGE_BASEURL=self.parent.baseurl)
      storage = Storage(Context(config=config, server=get_server('ACME-SEC')))
      return storage.get(IMAGE_URL % '9999')

    def should_not_exists(self, topic):
      expect(topic).to_equal(None)

  class CantPutImage(Vows.Context):
    def topic(self):
      config = Config(RIAK_STORAGE_BASEURL=self.parent.baseurl+'/TOTO')
      storage = Storage(Context(config=config, server=get_server('ACME-SEC')))
      return storage.put(IMAGE_URL % '9999','TOTO')

    def should_not_exists(self, topic):
      expect(topic).to_equal(None)

@Vows.batch
class CryptoVows(RiakDBContext):
  class RaisesIfInvalidConfig(Vows.Context):
    def topic(self):
      config = Config(RIAK_STORAGE_BASEURL=self.parent.baseurl, SECURITY_KEY='', STORES_CRYPTO_KEY_FOR_EACH_IMAGE=True)
      storage = Storage(Context(config=config, server=get_server('')))
      storage.put(IMAGE_URL % '3', IMAGE_BYTES)
      storage.put_crypto(IMAGE_URL % '3')

    def should_be_an_error(self, topic):
      expect(topic).to_be_an_error_like(RuntimeError)
      expect(topic).to_have_an_error_message_of("STORES_CRYPTO_KEY_FOR_EACH_IMAGE can't be True if no SECURITY_KEY specified")

  class GettingCryptoForANewImageReturnsNone(Vows.Context):
    def topic(self):
      config = Config(RIAK_STORAGE_BASEURL=self.parent.baseurl, STORES_CRYPTO_KEY_FOR_EACH_IMAGE=True)
      storage = Storage(Context(config=config, server=get_server('ACME-SEC')))
      return storage.get_crypto(IMAGE_URL % '9999')

    def should_be_null(self, topic):
      expect(topic).to_be_null()

  class DoesNotStoreIfConfigSaysNotTo(Vows.Context):
    def topic(self):
      config = Config(RIAK_STORAGE_BASEURL=self.parent.baseurl)
      storage = Storage(Context(config=config, server=get_server('ACME-SEC')))
      storage.put(IMAGE_URL % '5', IMAGE_BYTES)
      storage.put_crypto(IMAGE_URL % '5')
      return storage.get_crypto(IMAGE_URL % '5')

    def should_be_null(self, topic):
      expect(topic).to_be_null()

  class CanStoreCrypto(Vows.Context):
    def topic(self):
      config = Config(RIAK_STORAGE_BASEURL=self.parent.baseurl, SECURITY_KEY='ACME-SEC', STORES_CRYPTO_KEY_FOR_EACH_IMAGE=True)
      storage = Storage(Context(config=config, server=get_server('ACME-SEC')))
      storage.put(IMAGE_URL % '6', IMAGE_BYTES)
      storage.put_crypto(IMAGE_URL % '6')
      return storage.get_crypto(IMAGE_URL % '6')

    def should_not_be_null(self, topic):
      expect(topic).not_to_be_null()
      expect(topic).not_to_be_an_error()

    def should_have_proper_key(self, topic):
      expect(topic).to_equal('ACME-SEC')

@Vows.batch
class DetectorVows(RiakDBContext):
  class CanStoreDetectorData(Vows.Context):
    def topic(self):
      config = Config(RIAK_STORAGE_BASEURL=self.parent.baseurl)
      storage = Storage(Context(config=config, server=get_server('ACME-SEC')))
      storage.put(IMAGE_URL % '7', IMAGE_BYTES)
      storage.put_detector_data(IMAGE_URL % '7', [{'origin': 'detection', 'height': 43, 'width': 43, 'y': 197, 'x': 276, 'z': 1849}])
      return storage.get_detector_data(IMAGE_URL % '7')

    def should_not_be_null(self, topic):
      expect(topic).not_to_be_null()
      expect(topic).not_to_be_an_error()

    def should_equal_some_data(self, topic):
      expect(topic).to_equal([{'origin': 'detection', 'height': 43, 'width': 43, 'y': 197, 'x': 276, 'z': 1849}])

  class ReturnsNoneIfNoDetectorData(Vows.Context):
    def topic(self):
      config = Config(RIAK_STORAGE_BASEURL=self.parent.baseurl)
      storage = Storage(Context(config=config, server=get_server('ACME-SEC')))
      return storage.get_detector_data(IMAGE_URL % '10000')

    def should_not_be_null(self, topic):
      expect(topic).to_be_null()
