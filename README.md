Riak Storage Module for Thumbor
===================================

![Travis-CI status](https://secure.travis-ci.org/dhardy92/thumbor_riak.png?branch=master)
Some problems now on Travis-CI with riak support.

Introduction
------------

[Thumbor](https://github.com/globocom/thumbor/wiki) is a smart imaging service. It enables on-demand crop, resizing and flipping of images.

  
[Riak](http://wiki.basho.com/) is a distributed document oriented database implementing the consistent hashing algorythm from the Dynanmo publication by Amazon.
  

This module provide support for Riak as a large auto replicant key/value backend storage for images in Thumbor.


Installation
------------

The current version of the module is **0.2**.

In order to install the Riak Storage Module for Thumbor, you have to install a riak service first.

## Riak installation

The Riak Storage Module for Thumbor was originally developed and tested on a Riak 1.2.0 on Debian system. 

You can follow the [Riak Installation Guide](http://docs.basho.com/riak/latest/tutorials/fast-track/Building-a-Development-Environment/) 


## Thumbor installation

You have to install [Thumbor](https://github.com/globocom/thumbor) following the [Thumbor Installation Guide](https://github.com/globocom/thumbor/wiki/Installing)...


## Riak Storage Module installation

... and finally the Riak Storage Module :

	pip install thumbor_riak


Testing
-------

In order to execute [pyvows](http://heynemann.github.com/pyvows/) tests, you have to install pyvows :

	pip install pyvows 

and run tests with :

	pyvows
	

License
-------

	Licensed under the MIT license:
	http://www.opensource.org/licenses/mit-license
	Copyright (c) 2012 dhardy92@github.com
