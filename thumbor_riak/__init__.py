#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/globocom/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license

# HBASE STORAGE OPTIONS
from thumbor.config import Config
Config.define('RIAK_STORAGE_BASEURL', 'http://localhost:8097/riak','HTTP Riak interface for Storage', 'Riak Storage')

__version__ = "0.2"
