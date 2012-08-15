Database-performance-tests
==========================

This project is related to different databases performance comparison using python and tornado.

Databases
---------
For now, with this test script you can test performance of MySQL and MongoDB (synchronous and asychronous).
Also you can test Tornado for long polling and short polling operations.

Hardware configuration
----------------------
Intel Core i5 3200x4  
4Gb DDRIII RAM (1333Mhz)

Software configuration
----------------------
MySQL: Percona XtraDB Cluster 5.5  
MongoDB: version 2.0.7 

Pure MongoDB writing
--------------------
	Concurrency Level:      100
	Time taken for tests:   73.433 seconds
	Complete requests:      100000
	Failed requests:        0
	Write errors:           0
	Requests per second:    1361.78 [#/sec] (mean)
	Time per request:       73.433 [ms] (mean)
	Time per request:       0.734 [ms] (mean, across all concurrent requests)
	Transfer rate:          207.46 [Kbytes/sec] received

MySQL writing
-------------
	Concurrency Level:      100
	Time taken for tests:   5621.733 seconds
	Complete requests:      100000
	Failed requests:        0
	Write errors:           0
	Requests per second:    17.79 [#/sec] (mean)
	Time per request:       5621.733 [ms] (mean)
	Time per request:       56.217 [ms] (mean, across all concurrent requests)
	Transfer rate:          2.71 [Kbytes/sec] received

MongoDB writing with MongoEngine ORM
------------------------------------
	Concurrency Level:      100
	Time taken for tests:   321.135 seconds
	Complete requests:      100000
	Failed requests:        0
	Write errors:           0
	Requests per second:    311.40 [#/sec] (mean)
	Time per request:       321.135 [ms] (mean)
	Time per request:       3.211 [ms] (mean, across all concurrent requests)
	Transfer rate:          47.44 [Kbytes/sec] received

Async MongoDB writing with APyMongo library
-------------------------------------------
	Concurrency Level:      100
	Time taken for tests:   85.005 seconds
	Complete requests:      100000
	Failed requests:        0
	Write errors:           0
	Requests per second:    1176.41 [#/sec] (mean)
	Time per request:       85.005 [ms] (mean)
	Time per request:       0.850 [ms] (mean, across all concurrent requests)
	Transfer rate:          179.22 [Kbytes/sec] received
